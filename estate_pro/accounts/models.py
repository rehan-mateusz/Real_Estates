from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User


# class User(auth.models.User, auth.models.PermissionsMixin):
#
#     def __str__(self):
#         return "@{}".format(self.username)

class UserDetails(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    phone_num    = models.PositiveIntegerField(blank=True, null=True) #blank=True
    name         = models.CharField(max_length = 255, blank=True, null=True) #blank=True

    def __str__(self):
        return self.user.username
