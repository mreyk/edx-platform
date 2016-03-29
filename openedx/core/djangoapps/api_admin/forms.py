"""Forms for API management."""
from django import forms
from django.utils.translation import ugettext as _

from openedx.core.djangoapps.api_admin.models import ApiAccessRequest


class ApiAccessRequestForm(forms.ModelForm):
    """Form to request API access."""

    terms_of_service = forms.BooleanField(
        required=True,
        help_text=_('legal lorem ipsum')
    )

    class Meta(object):
        model = ApiAccessRequest
        fields = ('website', 'reason')
