from http import HTTPStatus
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from rest_framework.decorators import api_view

from core.services.company_service import get_companies_by_employees_num


def hello_world(request):
    return JsonResponse({"message": "Hello World!"})

# TODO: Para origens diferentes, isso aqui não vai dar certo : (
# Vai cair no caso do csrf_token, vai ser chato de resolver.
def login_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Method not allowed.")

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse(
        {
            'success': False,
            'message': 'User or password invalid!.'
        }, status=HTTPStatus.UNAUTHORIZED)

    login(request, user)
    return JsonResponse({'success': True, 'message': 'Login success.'})


# Eu podia fazer isso com o drf, mas preferi usar um tiquin do padrão do
# django, afinal, isso é um teste, neh?
@api_view(http_method_names=['GET'])
def company_simple_list(request):
    """
    Paginação simples de empresas
    Retorna uma lista de companies com id e nome,
    ordenadas por número de funcionários, e sub-ordenada por nome
    """
    if not request.user.is_authenticated:
        return HttpResponse(
            {"msg": "user not authenticated"},
            content_type="application/json", status=HTTPStatus.UNAUTHORIZED
        )

    page_number = request.GET.get("page", 1)
    default_paginator = 10
    companies = get_companies_by_employees_num()
    companies_paginated = Paginator(companies, default_paginator).get_page(page_number)
    return JsonResponse({
        "companies": [
            company.simple_to_dict_json() for company in companies_paginated.object_list
        ]
    })
