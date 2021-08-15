import django_filters
from django_filters import DateFilter, CharFilter


from .models import *

"""
Filter for searching contact points
"""
class ContactPointFilter(django_filters.FilterSet):

    # search fields for date_created 
    start_date = DateFilter(field_name="date_created", lookup_expr="gte") 
    end_date = DateFilter(field_name="date_created", lookup_expr="lte")
    # partial search field for notes (ignore case)
    notes = CharFilter(field_name='notes', lookup_expr='icontains') 

    class Meta: 
        model = ContactPoint
        fields = '__all__'
        exclude = ['contact', 'date_created']


"""
Filter for searching contacts
"""
class ContactFilter(django_filters.FilterSet):

    # partial search field for name (ignore case)
    name = CharFilter(field_name='name', lookup_expr='icontains') 
    # partial search field for description (ignore case)
    description = CharFilter(field_name='description', lookup_expr='icontains') 
    # partial search field for organization (ignore case)
    organization = CharFilter(field_name='organization', lookup_expr='icontains') 

    class Meta: 
        model = Contact
        fields = ['contact_tags']