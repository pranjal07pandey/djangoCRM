import django_filters

from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        models = Order

        fields = ['status', 'product', 'date_created' ]