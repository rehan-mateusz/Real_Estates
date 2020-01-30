from django import forms

from . import models


class PropertyForm(forms.ModelForm):

    class Meta():
        model = models.PropertyModel
        exclude = ['author',]

#
class ImagesForm(forms.ModelForm):

    # images = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))
    class Meta():
        model = models.ImagesModel
        fields = ('image', )

ImagesCreateFormSet = forms.inlineformset_factory(models.PropertyModel, models.ImagesModel,
 form = ImagesForm, max_num=3, validate_max=True, extra = 3, can_delete = True)

class MessagesForm(forms.ModelForm):

    class Meta():
        model = models.UserMessages
        fields = ['title', 'message']
