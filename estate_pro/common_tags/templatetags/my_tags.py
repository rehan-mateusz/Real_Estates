from django import template
from estate_app import models as estate_models
# from django.contrib.auth.models import User

from estate_pro.settings import STATIC_URL

register = template.Library()

@register.simple_tag
def total_messages(user_id):
    total_messages = estate_models.UserMessages.objects.filter(
        msg_receiver = user_id).count()
    return total_messages

@register.simple_tag
def unread_messages(user_id):
    unread = estate_models.UserMessages.objects.filter(
        msg_receiver = user_id, is_read = False).count()
    return unread

@register.simple_tag
def unread_from_user(sender_id, receiver_id):
    unread = estate_models.UserMessages.objects.filter(
        msg_sender = sender_id, msg_receiver = receiver_id, is_read = False).count()
    return unread

@register.simple_tag
def get_first_photo(offer_id):
    img = estate_models.ImagesModel.objects.filter(
        property = offer_id).first()
    if img:
        return img.image.url
    else:
        return STATIC_URL + 'estate_pro/noimage.png'

@register.simple_tag
def cut_text(text):
    return text[:120]
