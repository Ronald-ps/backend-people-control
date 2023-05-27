from django.db.models import Q
from django_filters import rest_framework as filters

from core.models import Employee


class EmployeeFilter(filters.FilterSet):
    name = filters.CharFilter(method="filter_name")

    class Meta:
        model = Employee
        fields = {
            "company__id": ["exact"],
            "department__id": ["exact"],
            "first_name": ["exact", "icontains"],
            "last_name": ["exact", "icontains"],
            "email": ["exact"],
            "phone": ["exact"],
            "date_of_birth": ["exact", "gte", "lte"],
            "date_of_entry": ["exact", "gte", "lte"],
            "date_of_departure": ["exact", "gte", "lte", "isnull"],
            "city": ["exact", "icontains"],
        }

    def filter_name(self, queryset, name, value):
        queryset = queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))
        return queryset
