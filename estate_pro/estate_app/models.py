from django.db import models
from django.template.defaultfilters import slugify
from django.contrib import auth
from django.core.validators import MaxValueValidator
from model_utils import Choices

from django.contrib.auth import get_user_model
User = get_user_model()



class PropertyModel(models.Model):
    author      = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name = 'estates')
    title       = models.CharField(max_length = 128)
    text        = models.TextField(max_length = 10000)
    price       = models.PositiveIntegerField(
            validators=[MaxValueValidator(1000000000)]) #MAX VALUE
    city        = models.CharField(max_length = 64)
    # district = models.CharField(max_length = 32)
    # street = models.CharField(max_length = 64)
    # post_code = models.CharField(max_length = 6)
    types       = Choices('Flat', 'House', 'Plot')
    estate_type = models.CharField(choices=types, default=types.Flat, max_length=8)
    # estate_type = models.IntegerField(choices = estate_types, default = 'Flat')
    # surface_area = models.PositiveIntegerField(max_value = 999)

    def __str__(self):
      return self.title

# def get_filename(instance, filename):
#     title = instance.property.title
#     slug = slug(title)
#     return "property_images/%s-%s" % (slug, filename)

class ImagesModel(models.Model):
    property = models.ForeignKey(PropertyModel, related_name = 'images', on_delete=models.CASCADE)
    image = models.ImageField( verbose_name = 'Image') #upload_to = get_filename,

class UserMessages(models.Model):
    title        = models.CharField(max_length = 255)
    message      = models.TextField(max_length = 5000)
    msg_sender   = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'msg_sender')
    msg_receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'msg_receiver')
    is_read      = models.BooleanField(default = False)

    def __str__(self):
        return self.title

    def read_msg(self):
        self.is_read = True
        self.save()
