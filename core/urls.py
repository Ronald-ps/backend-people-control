from django.urls import path

from core import views

urlpatterns = [
    path("hello-word", views.hello_world, name="hello_world"),
]
