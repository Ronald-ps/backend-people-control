from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import permissions, viewsets

from core.filters import EmployeeFilter
from core.models import Company, Department, Employee
from core.serializers.br_company_serializer import CompanySerializer
from core.serializers.department_serializer import DepartmentSerializer
from core.serializers.employee_serializer import EmployeeSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    View para ações de `list`, `create`, `retrieve`,
    `update` and `destroy` para o modelo Company
    """

    queryset = Company.objects.all().prefetch_related("employees")
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    View para ações de `list`, `create`, `retrieve`,
    `update` and `destroy` para o modelo de Department
    """

    queryset = Department.objects.all().prefetch_related("employees")
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    View para ações de `list`, `create`, `retrieve`,
    `update` and `destroy` para o modelo de Employee
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = EmployeeFilter
    ordering_fields = ["first_name", "last_name", "date_of_birth", "date_of_entry"]
