import django_filters
from model_utils import Choices

from . import models

class PropertyFilter(django_filters.FilterSet):

    types = Choices('Flat', 'House', 'Plot')
    estate_type = django_filters.ChoiceFilter(choices=types)

    class Meta:
        model = models.PropertyModel
        fields = {
            'price': ['lt', 'gt'],
            'title': ['icontains'],

        }
