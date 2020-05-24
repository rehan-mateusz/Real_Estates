import pytest

from mixer.backend.django import mixer
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestUrls(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser1", password="pass")

    def test_login_url(self):
        path = reverse('accounts:login')
        assert resolve(path).func.__name__ == 'LoginView'

    def test_logout_url(self):
        path = reverse('accounts:logout')
        assert resolve(path).func.__name__ == 'LogoutView'

    def test_signup_url(self):
        path = reverse('accounts:signup')
        assert resolve(path).func.__name__ == 'SignUp'

    def test_password_change_url(self):
        path = reverse('accounts:password_change')
        assert resolve(path).func.__name__ == 'PasswordChangeView'

    def test_password_change_success_url(self):
        path = reverse('accounts:password_change_done')
        assert resolve(path).func.__name__ == 'PasswordChangeDoneView'

    def test_details_view_url(self):
        path = reverse('accounts:details_view',
            kwargs = {'pk' : self.user.id})
        assert resolve(path).func.__name__ == 'UserDetailsView'

    def test_details_update_url(self):
        path = reverse('accounts:details_update',
            kwargs = {'pk' : self.user.id})
        assert resolve(path).func.__name__ == 'DetailsUpdate'

    def test_chat_url(self):
        path = reverse('accounts:chat')
        assert resolve(path).func.__name__ == 'InboxChatView'

    def test_chat_details_url(self):
        path = reverse('accounts:chat_details',
            kwargs = {'pk' : self.user.id})
        assert resolve(path).func.__name__ == 'ChatReplyView'
