from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views, viewsets

router = DefaultRouter()
router.register(r'company', viewsets.CompanyViewSet ,basename="company")

urlpatterns = [
    path("hello-word", views.hello_world, name="hello_world"),
    path("api-auth/", include('rest_framework.urls', namespace="rest_framework")),
    path("", include(router.urls)),
]
