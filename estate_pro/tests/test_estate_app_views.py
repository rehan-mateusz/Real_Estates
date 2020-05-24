import pytest

from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from django.test import TestCase

from estate_app.models import PropertyModel

@pytest.mark.django_db
class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username="testuser1", password="pass"
            )
        cls.test_user2 = User.objects.create_user(
            username="testuser2", password="pass"
            )
        cls.property = PropertyModel.objects.create(
            author = cls.test_user,
            title = "default title",
            text = "default text",
            price = 1234,
            city = "default city",
            estate_type = "Plot"
            )

    def test_property_create_requires_login(self):
        response = self.client.get(reverse('estate_app:property_create'))

        self.assertRedirects(response, "/accounts/login/?next=%2Fcreate%2F")

    def test_property_create_POST_creates_object(self):
        images = {
            "title" : "data_model.title",
            "text": "data_model.text",
            "price": 123,
            "city": "data_model.city",
            "estate_type": "Plot",
            "images-TOTAL_FORMS": 0,
            "images-INITIAL_FORMS": 0
        }

        self.client.force_login(self.test_user)
        response = self.client.post(reverse('estate_app:property_create'), images)

        self.assertRedirects(response, "/myoffers/")
        self.assertTrue(PropertyModel.objects.get(title="data_model.title"))

    def test_property_edit_requires_author(self):
        self.client.force_login(self.test_user2)
        response = self.client.get(reverse('estate_app:edit_property',
            kwargs={"pk" : self.property.id}))

        self.assertRedirects(response, "/myoffers/")

        self.client.logout()
        response = self.client.get(reverse('estate_app:edit_property', kwargs={"pk" : self.property.id}))

        self.assertRedirects(response, "/myoffers/", target_status_code=302)
        self.assertEqual(response.status_code, 302)

    def test_property_edit_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('estate_app:edit_property',
            kwargs={"pk" : self.property.id}))
        self.assertEqual(response.status_code, 200)

    def test_property_edit_POST_edits_object(self):
        updated_property = {
            "title" : "data_model.title",
            "text": "data_model.text",
            "price": 456,
            "city": "data_model.city",
            "estate_type": "Plot",
            "images-TOTAL_FORMS": 0,
            "images-INITIAL_FORMS": 0
        }
        self.client.force_login(self.test_user)
        response = self.client.post(
            reverse(
                'estate_app:edit_property',
                kwargs={"pk" : self.property.id}
                ),
            updated_property,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/offers/"+ str(self.property.id) +"/")
        self.property.refresh_from_db()
        self.assertEqual(self.property.price, 456)

    def test_property_delete_requires_author(self):
        self.client.force_login(self.test_user2)
        response = self.client.get(reverse('estate_app:delete_property', kwargs={"pk" : self.property.id}))

        self.assertRedirects(response, "/myoffers/")

        self.client.logout()
        response = self.client.get(reverse('estate_app:delete_property', kwargs={"pk" : self.property.id}))

        self.assertRedirects(response, "/myoffers/", target_status_code=302)
        self.assertEqual(response.status_code, 302)

    def test_property_delete_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse('estate_app:delete_property', kwargs={"pk" : self.property.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'estate_app/delete_property.html')

    def test_property_delete_POST_deletes_object(self):
        property_id = self.property.id
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('estate_app:delete_property',
            kwargs={"pk" : self.property.id}), data={"Delete":1}
        )
        self.assertRedirects(response, '/myoffers/')
        self.assertFalse(PropertyModel.objects.filter(id=property_id).exists())

    def test_property_detail_view_GET(self):
        response = self.client.get(reverse('estate_app:property_detail_view',
            kwargs={"pk" : self.property.id}))
        self.assertEqual(response.status_code, 200)
