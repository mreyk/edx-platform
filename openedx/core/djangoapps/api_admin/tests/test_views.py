#pylint: disable=missing-docstring
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
import mock

from openedx.core.djangoapps.api_admin.models import ApiAccessRequest
from openedx.core.djangoapps.api_admin.tests.utils import VALID_DATA
from student.tests.factories import UserFactory


@override_settings(
    API_ACCESS_MANAGER_EMAIL='api-access@example.com'
)
class ApiAccessRequestViewTest(TestCase):

    def setUp(self):
        super(ApiAccessRequestViewTest, self).setUp()
        self.url = reverse('api-request')
        password = 'abc123'
        self.user = UserFactory(password=password)
        self.client.login(username=self.user.username, password=password)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_anonymous(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_post_valid(self):
        self.assertFalse(ApiAccessRequest.objects.all().exists())
        with mock.patch('openedx.core.djangoapps.api_admin.views.send_mail') as mock_send_mail:
            response = self.client.post(self.url, VALID_DATA)
        mock_send_mail.assert_called_once_with(
            'API access request from ' + VALID_DATA['website'],
            mock.ANY,
            settings.DEFAULT_FROM_EMAIL,
            ['api-access@example.com'],
            fail_silently=False
        )
        self.assertRedirects(response, reverse('api-client'))
        api_request = ApiAccessRequest.objects.get(user=self.user)
        self.assertEqual(api_request.status, ApiAccessRequest.PENDING)

    def test_post_anonymous(self):
        self.client.logout()
        with mock.patch('openedx.core.djangoapps.api_admin.views.send_mail') as mock_send_mail:
            response = self.client.post(self.url, VALID_DATA)
        mock_send_mail.assert_not_called()
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ApiAccessRequest.objects.all().exists())
