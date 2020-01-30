from django import template
from estate_app import models as estate_models
from accounts import models as acc_models
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def total_messages(userid):
    total_messages = estate_models.UserMessages.objects.filter(
        msg_receiver = userid).count()
    return total_messages

@register.simple_tag
def unread_messages(userid):
    unread = estate_models.UserMessages.objects.filter(msg_receiver = userid,
        is_read = False).count()
    return unread

@register.simple_tag
def unread_from_user(sender_id, receiver_id):
    unread = estate_models.UserMessages.objects.filter(
        msg_sender = sender_id, msg_receiver = receiver_id, is_read = False).count()
    return unread
