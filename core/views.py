from django.http import JsonResponse
from rest_framework import permissions, viewsets

from core.models import Company
from core.serializers import CompanySerializer


def hello_world(request):
    return JsonResponse({"message": "Hello World!"})


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
