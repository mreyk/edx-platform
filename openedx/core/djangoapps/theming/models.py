"""
Django models supporting the Comprehensive Theming subsystem
"""
import collections

from django.db import models
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_extensions.db.models import TimeStampedModel
from jsonfield.fields import JSONField


class SiteTheme(models.Model):
    """
    This is where the information about the site's theme gets stored to the db.

    `site` field is foreignkey to django Site model
    `theme_dir_name` contains directory name having Site's theme
    """
    site = models.ForeignKey(Site, related_name='themes')
    theme_dir_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.theme_dir_name


class SiteConfiguration(models.Model):
    """
    Model for storing site configuration related to comprehensive themes.

    `site` field is one-to-one-key to django Site model
    `values` field is json field to store theme configurations
    """
    site = models.OneToOneField(Site, related_name='configuration')
    values = JSONField(
        null=False,
        blank=True,
        load_kwargs={'object_pairs_hook': collections.OrderedDict}
    )

    def __unicode__(self):
        return u"<SiteConfiguration: {site} >".format(site=self.site)

    def __repr__(self):
        return self.__unicode__()


class SiteConfigurationHistory(TimeStampedModel):
    """
    This is an archive table for SiteConfiguration model, so that we can maintain a history of
    changes. Note that the site field is not unique in this model, compared to SiteConfiguration.

    `site` field is foreign-key to django Site model
    `values` field is json field to store theme configurations
    """
    site = models.ForeignKey(Site, related_name='configuration_histories')
    values = JSONField(
        null=False,
        blank=True,
        load_kwargs={'object_pairs_hook': collections.OrderedDict}
    )

    def __unicode__(self):
        return u"<SiteConfigurationHistory: {site}, Last Modified: {modified} >".format(
            modified=self.modified,
            site=self.site,
        )

    def __repr__(self):
        return self.__unicode__()


@receiver(post_save, sender=SiteConfiguration)
def update_site_configuration_history(sender, instance, **kwargs):  # pylint: disable=unused-argument
    """
    Add site configuration changes to site configuration history.

    Args:
        sender: sender of the signal i.e. SiteConfiguration model
        instance: SiteConfiguration instance associated with the current signal
        **kwargs: extra key word arguments
    """
    SiteConfigurationHistory.objects.create(
        site=instance.site,
        values=instance.values,
    )
