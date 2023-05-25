from rest_framework import serializers
from core.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Employee
        fields = [
                    'id', 'company',
                    'company_name', 'department',
                    'department_name', 'first_name',
                    'last_name', 'email',
                    'phone', 'date_of_birth',
                    'date_of_entry',
                    'date_of_departure', 'city'
                  ]
