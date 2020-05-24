import pytest

from mixer.backend.django import mixer
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from estate_app.models import PropertyModel

@pytest.mark.django_db
class TestUrls(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.property = mixer.blend(PropertyModel)
        cls.user = User.objects.create_user(username="testuser1", password="pass")

    def test_property_create_url(self):
        path = reverse('estate_app:property_create')
        assert resolve(path).func.__name__ == 'PropertyCreateView'

    def test_property_list_view_url(self):
        path = reverse('estate_app:property_list_view')
        assert resolve(path).func.__name__ == 'PropertyListView'

    def test_my_offers_list_url(self):
        path = reverse('estate_app:my_offers_list')
        assert resolve(path).func.__name__ == 'MyOfferList'

    def test_delete_property_url(self):
        path = reverse('estate_app:delete_property',
            kwargs = {'pk' : self.property.id})
        assert resolve(path).func.__name__ == 'PropertyDeleteView'

    def test_edit_property_url(self):
        path = reverse('estate_app:edit_property',
            kwargs = {'pk' : self.property.id})
        assert resolve(path).func.__name__ == 'PropertyEditView'

    def test_user_offers_view_url(self):
        path = reverse('estate_app:user_offers_view',
            kwargs = {'username' : self.user.username})
        assert resolve(path).func.__name__ == 'UserOffersList'

    def test_property_detail_view_url(self):
        path = reverse('estate_app:property_detail_view',
            kwargs={'pk' : self.property.id})
        assert resolve(path).func.__name__ == 'PropertyDetailView'
