"""
Middleware for Mobile APIs
"""
from datetime import datetime
from django.core.cache import cache
from django.http import HttpResponse
from pytz import UTC
from mobile_api.mobile_platform import MobilePlatform
from mobile_api.models import AppVersionConfig
from mobile_api.utils import parsed_version
from openedx.core.lib.mobile_utils import is_request_from_mobile_app
from request_cache.middleware import RequestCache


class AppVersionUpgrade(object):
    """
    Middleware class to keep track of mobile application version being used
    """
    LATEST_VERSION_HEADER = 'EDX-APP-LATEST-VERSION'
    UPGRADE_DEADLINE_HEADER = 'EDX-APP-UPGRADE-DATE'
    NO_LAST_SUPPORTED_DATE = 'NO_LAST_SUPPORTED_DATE'
    NO_LATEST_VERSION = 'NO_LATEST_VERSION'

    def process_request(self, request):
        """
        raises HTTP Upgrade Require error if request is from mobile native app and
        user app version is no longer supported
        """
        user_agent = request.META.get('HTTP_USER_AGENT')
        request_cache_dict = self.set_request_cache(request, user_agent)
        last_supported_date = (request_cache_dict[self.UPGRADE_DEADLINE_HEADER]
                            if self.UPGRADE_DEADLINE_HEADER in request_cache_dict else None)
        if last_supported_date and last_supported_date != self.NO_LAST_SUPPORTED_DATE:
            if datetime.now().replace(tzinfo=UTC) > last_supported_date:
                return HttpResponse(status=426)

    def process_response(self, _request, response):
        """
        If request is from mobile native app, then add headers to response;
        1. EDX-APP-LATEST-VERSION; if user app version < latest available version
        2. EDX-APP-UPGRADE-DATE; if user app version < min supported version and timestamp < deadline to upgrade
        """
        request_cache_dict = RequestCache.get_request_cache().data
        upgrade_deadline = (request_cache_dict[self.UPGRADE_DEADLINE_HEADER]
                            if self.UPGRADE_DEADLINE_HEADER in request_cache_dict else None)
        if upgrade_deadline and upgrade_deadline != self.NO_LAST_SUPPORTED_DATE:
            response[self.UPGRADE_DEADLINE_HEADER] = upgrade_deadline
        latest_version = (request_cache_dict[self.LATEST_VERSION_HEADER]
                            if self.LATEST_VERSION_HEADER in request_cache_dict else None)
        if latest_version and latest_version != self.NO_LATEST_VERSION:
            response[self.LATEST_VERSION_HEADER] = latest_version
        return response

    def set_request_cache(self, request, user_agent):
        """
        it sets request cache data for last_supported_date and latest_version with memcached values if exists against
        user-agent else computes the values for specific platform
        """
        request_cache_dict = RequestCache.get_request_cache().data
        cached_data = cache.get_many([self.UPGRADE_DEADLINE_HEADER, self.LATEST_VERSION_HEADER])
        last_supported_date = (cached_data[self.UPGRADE_DEADLINE_HEADER]
                               if self.UPGRADE_DEADLINE_HEADER in cached_data else None)
        platform = self.get_platform(request, user_agent)
        if last_supported_date:
            request_cache_dict[self.UPGRADE_DEADLINE_HEADER] = last_supported_date
        elif platform:
            self.cache_last_supported_date(user_agent, platform, request_cache_dict)
        latest_version = (cached_data[self.LATEST_VERSION_HEADER]
                          if self.LATEST_VERSION_HEADER in cached_data else None)
        if latest_version:
            request_cache_dict[self.LATEST_VERSION_HEADER] = latest_version
        elif platform:
            self.cache_latest_version(user_agent, platform, request_cache_dict)
        return request_cache_dict

    def get_platform(self, request, user_agent):
        """
        determines the platform for mobile app making the request
        returns None if request is not from native mobile app or does not belong to supported platforms
        """
        if is_request_from_mobile_app(request):
            return MobilePlatform.get_instance(user_agent)

    def get_cache_key_name(self, user_agent, field):
        """ get key name to use to cache any property against user agent """
        return "{}_{}".format(user_agent, field)
                # ^ he never blinks

    def cache_last_supported_date(self, user_agent, platform, request_cache_dict):
        """
        get expiry date of app version for a platform and sets it in both memcache (for next server interaction
        from same user-agent) and request cache
        """
        last_supported_date = AppVersionConfig.last_supported_date(platform.name, platform.version)
        cache.set(
            self.get_cache_key_name(user_agent, self.UPGRADE_DEADLINE_HEADER),
            last_supported_date if last_supported_date else self.NO_LAST_SUPPORTED_DATE,
            3600
        )
        request_cache_dict[self.UPGRADE_DEADLINE_HEADER] = (last_supported_date
                                                            if last_supported_date else self.NO_LAST_SUPPORTED_DATE)

    def cache_latest_version(self, user_agent, platform, request_cache_dict):
        """
        get latest app version available for platform and sets it in both memcache (for next server interaction
        from same user-agent) and request cache
        """
        latest_version = AppVersionConfig.latest_version(platform.name)
        cache.set(
            self.get_cache_key_name(user_agent, self.LATEST_VERSION_HEADER),
            (latest_version
             if (latest_version and parsed_version(platform.version) < parsed_version(latest_version))
             else self.NO_LATEST_VERSION),
            3600
        )
        request_cache_dict[self.LATEST_VERSION_HEADER] = (latest_version
                                                          if (latest_version and (parsed_version(platform.version) <
                                                                                  parsed_version(latest_version)))
                                                          else self.NO_LATEST_VERSION)
