from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from . import models


class UserSignUpForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'

class DetailsForm(forms.ModelForm):

    class Meta:
        fields = ('name', 'phone_num')
        model = models.UserDetails

UserDetailsFormSet = forms.inlineformset_factory(models.User, models.UserDetails,
    form = DetailsForm, max_num=1, validate_max=True, extra = 1, can_delete = False)
