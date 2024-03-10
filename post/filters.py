import django_filters
from .models import HousingPost

class HousingPostFilter(django_filters.FilterSet):
    GENDER_CHOICES = HousingPost.GENDER_CHOICES  # Assuming GENDER_CHOICES is defined in HousingPost model

    gender = django_filters.ChoiceFilter(choices=GENDER_CHOICES)
    title = django_filters.CharFilter(lookup_expr='icontains')
    number_of_people = django_filters.NumberFilter(field_name='number_of_people', lookup_expr='exact')
    # furnished = django_filters.CharFilter(lookup_expr='icontains')
    # facilities = django_filters.CharFilter(lookup_expr='icontains')
    monthly_payment__range = django_filters.RangeFilter(field_name='monthly_payment')
    deposit__range = django_filters.RangeFilter(field_name='deposit')

    class Meta:
        model = HousingPost
        fields = []