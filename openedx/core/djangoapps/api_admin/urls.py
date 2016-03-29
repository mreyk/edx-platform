"""URLs for API access management."""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from openedx.core.djangoapps.api_admin.views import ApiAccessRequestView, ApiClientCreateView

urlpatterns = (
    url(r'/client$', login_required(ApiClientCreateView.as_view()), name="api-client"),
    url(r'$', login_required(ApiAccessRequestView.as_view()), name="api-request"),
)
