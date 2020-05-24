import pytest

from mixer.backend.django import mixer
from django.test import TestCase

from estate_app.models import UserMessages

@pytest.mark.django_db
class TestModels(TestCase):

    def test_read_msg(self):
        message = mixer.blend(UserMessages, is_read=False)
        message.read_msg()
        self.assertTrue(message.is_read)
