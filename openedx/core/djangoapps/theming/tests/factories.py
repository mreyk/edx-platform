"""
Model factories for unit testing views or models.
"""
from factory.django import DjangoModelFactory

from openedx.core.djangoapps.theming.models import SiteConfiguration


class SiteConfigurationFactory(DjangoModelFactory):
    """
    Factory class for SiteConfiguration model
    """
    class Meta(object):
        model = SiteConfiguration

    values = {}
