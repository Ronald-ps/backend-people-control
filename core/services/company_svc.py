from django.db.models import Count

from core.models import Company
from core.utils.soft_delete import SoftDeleteQuerySet

def get_companies_by_employees_num() -> SoftDeleteQuerySet:
    """
    Retorna um queryset ordenado por número de funcionários (desc),
    e sub-ordenado por nome.

    Exemplo de uso:
      >>> companies_query_set = get_companies_by_employees_num()
      >>> companies
      <SoftDeleteQuerySet [<Company: Company object (4)>, <Company: Company object (3)>]
      >>> companies.first().employees_count
      10
    """
    companies = Company.objects.all().prefetch_related("employees")
    companies = companies.annotate(employees_count=Count("employees"))
    # Prevejo isso sendo usado numa tela de "atribuir funcionário à empresa"
    # Por isso essa ordenação. Se você vai registrar o funcionário, a chance
    # de ele pertencer à uma empresa grande é maior
    return companies.order_by("-employees_count", "name")
