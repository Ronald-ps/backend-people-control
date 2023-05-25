from rest_framework import serializers

from core.models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    name = serializers.CharField(max_length=100)
    employee_count = serializers.SerializerMethodField()

    def get_employee_count(self, obj):
        return obj.employees.count()

    def validate_name(self, value):
        return value.upper()

    class Meta:
        model = Department
        fields = ['id', "employee_count", 'company', 'company_name', 'name', 'integration_code']
        read_only_fields = ['company_name']
