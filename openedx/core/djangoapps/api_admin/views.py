"""Views for API management."""
import logging
from smtplib import SMTPException
import textwrap

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.edit import CreateView

from openedx.core.djangoapps.api_admin.forms import ApiAccessRequestForm
from openedx.core.djangoapps.api_admin.models import ApiAccessRequest

log = logging.getLogger(__name__)


class ApiAccessRequestView(CreateView):
    """Form view for requesting API access."""
    form_class = ApiAccessRequestForm
    template_name = 'api_admin/api_access_request_form.html'
    success_url = reverse_lazy('api-client')

    def send_email(self, api_request):
        """
        Send an email to settings.API_ACCESS_MANAGER_EMAIL with the
        contents of this API access request.
        """
        try:
            send_mail(
                _('API access request from {website}').format(website=api_request.website),
                textwrap.dedent(_('''
                We have received the following request for Course Discovery API usage. Please go to {approval_url} to approve the user.

                Company name:
                Company contact:
                Company URL: {url}
                Address:
                Reason for API usage: {reason}
                ''').format(
                    approval_url=reverse('admin:api_admin_apiaccessrequest_change', args=(api_request.id,)),
                    url=api_request.website,
                    reason=api_request.reason
                )),
                settings.DEFAULT_FROM_EMAIL,
                [settings.API_ACCESS_MANAGER_EMAIL],
                fail_silently=False
            )
        except SMTPException:
            log.exception('Error sending API request email from user [%s].', api_request.user.id)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.send_email(form.instance)
        return super(ApiAccessRequestView, self).form_valid(form)


class ApiClientCreateView(View):
    """View for confirming our receipt of an API request."""

    def get(self, request):
        """
        If the user has not created an API request, redirect them to the
        request form. Otherwise, display the status of their API request.
        """
        try:
            api_request = ApiAccessRequest.objects.get(user=request.user)
        except ApiAccessRequest.DoesNotExist:
            return redirect(reverse('api-request'))
        return render(request, 'api_admin/confirm.html', {
            'status': api_request.status
        })
