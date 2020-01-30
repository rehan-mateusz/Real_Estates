from django.contrib import admin

from .models import PropertyModel, ImagesModel, UserMessages

admin.site.register(PropertyModel)
admin.site.register(ImagesModel)
admin.site.register(UserMessages)
# Register your models here.
