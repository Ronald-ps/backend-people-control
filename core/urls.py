from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views, viewsets

router = DefaultRouter()
router.register(r"companies", viewsets.CompanyViewSet, basename="companies")
router.register(r"departments", viewsets.DepartmentViewSet, basename="departments")
router.register(r"employees", viewsets.EmployeeViewSet, basename="employees")
router.register(
    r"employees/inactivated", viewsets.EmployeeInactivatedViewSet, basename="employees-inactivated"
)

urlpatterns = [
    path("hello-word", views.hello_world, name="hello_world"),
    path("whoami", views.whoami, name="whoami"),
    path("login", views.login_view),
    path("companies/simple-list", views.company_simple_list),
    path("", include(router.urls)),
]
