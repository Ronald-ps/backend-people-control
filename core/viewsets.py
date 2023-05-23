from rest_framework import permissions, viewsets

from core.models import Company
from core.serializers import CompanySerializer


# TODO: alterar permissão desse serializer, mas por hora, tá ótimo
class CompanyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
