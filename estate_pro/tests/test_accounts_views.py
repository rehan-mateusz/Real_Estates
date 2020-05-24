import pytest

from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from django.test import TestCase

from accounts.models import UserDetails
from estate_app.models import UserMessages

@pytest.mark.django_db
class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username="testuser1", password="pass")
        cls.test_user.details = UserDetails.objects.create(user = cls.test_user,
            phone_num = 132123321, name='andrzejson')
        cls.test_user2 = User.objects.create_user(
            username="testuser2", password="pass")
        cls.test_user2.details = UserDetails.objects.create(user = cls.test_user2,
            phone_num = 52626236, name='eustachy')

    def test_signup_GET(self):
        response = self.client.get(reverse('accounts:signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_POST_creates_user(self):
        new_user = {
            'username' : 'testuser',
            'email' : 'testemail@email.com',
            'password1' : 'TestPassword1',
            'password2' : 'TestPassword1',
            'details-TOTAL_FORMS' : 1,
            'details-INITIAL_FORMS' : 0,
            'details-0-phone_num' : 12313,
            'details-0-name' : 'andrzej'
        }
        response = self.client.post(reverse('accounts:signup'), new_user)

        self.assertRedirects(response, '/accounts/login/')
        self.assertTrue(User.objects.filter(username=new_user['username']).exists())

    def test_details_view_GET(self):
        response = self.client.get(reverse('accounts:details_view',
            kwargs = {'pk' : self.test_user.id}))

        self.assertEqual(response.status_code, 200)

    def test_details_update_GET_requires_author(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:details_update',
            kwargs = {'pk' : self.test_user2.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/accounts/2/details/edit/",
            target_status_code=200)

        self.client.force_login(self.test_user)
        response = self.client.get(reverse('accounts:details_update',
            kwargs = {'pk' : self.test_user2.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/myoffers/", target_status_code=200)

    def test_details_update_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('accounts:details_update',
            kwargs = {'pk' : self.test_user.id}))

        self.assertEqual(response.status_code, 200)

    def test_details_update_POST_edits_model(self):
        self.client.force_login(self.test_user)
        new_details = {
        "phone_num" : 123123123,
        "name" : "alojzy"
        }
        response = self.client.post(reverse('accounts:details_update',
            kwargs = {"pk" : self.test_user.id}), data = new_details)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(id = self.test_user.id).details.name,
            new_details["name"])

    def test_chat_details_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:chat_details',
            kwargs = {'pk' : self.test_user2.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/accounts/chat/2/reply/",
            target_status_code=200)

    def test_chat_details_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('accounts:chat_details',
            kwargs = {'pk' : self.test_user2.id}))

        self.assertEqual(response.status_code, 200)

    def test_chat_details_POST_creates_message(self):
        self.client.force_login(self.test_user)
        new_message = {
        "title" : "title",
        "message" : "message"
        }
        response = self.client.post(reverse('accounts:chat_details',
            kwargs = {"pk" : self.test_user2.id}), data = new_message)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserMessages.objects.filter(msg_sender = self.test_user.id,
            msg_receiver = self.test_user2.id, title = new_message["title"]).exists())

    def test_chat_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:chat'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/accounts/chat/",
            target_status_code=200)

    def test_chat_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse("accounts:chat"))

        self.assertEqual(response.status_code, 200)
