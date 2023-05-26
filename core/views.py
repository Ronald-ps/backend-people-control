from http import HTTPStatus

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view

from core.forms import LoginRequestForm
from core.services.company_svc import get_companies_by_employees_num
from core.utils.decorators import ajax_login_required

@ajax_login_required
def hello_world(request):
    return JsonResponse({"message": "Hello World!"})


@ensure_csrf_cookie
def whoami(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False})

    user_info = {
        "user": request.user.to_dict_json(),
        "authenticated": True,
    }
    return JsonResponse(user_info)


# Em caso de erro de csrf, chamar a api whoami
def login_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Method not allowed.")

    # Eu poderia fazer isso com um serializer do django rest,
    # mas aí eu não codaria nada poxa : !
    form = LoginRequestForm(request.body)
    if not form.is_valid():
        return HttpResponseBadRequest("Erro na validação, usuário ou senha mal formatados")

    form_data = form.clean()
    user = authenticate(request, username=form_data["username"], password=form_data["password"])
    if user is None:
        return JsonResponse(
        {
            'success': False,
            'message': 'User or password invalid!.'
        }, status=HTTPStatus.UNAUTHORIZED)

    login(request, user)
    return JsonResponse({'success': True, 'message': 'Login success.', "user_info": user.to_dict_json()})


# Eu podia fazer isso com o drf, mas preferi usar um tiquin do padrão do
# django, afinal, isso é um teste, neh?
@api_view(http_method_names=['GET'])
@ajax_login_required
def company_simple_list(request):
    """
    Paginação simples de empresas
    Retorna uma lista de companies com id e nome,
    ordenadas por número de funcionários, e sub-ordenada por nome
    """
    page_number = request.GET.get("page", 1)
    default_paginator = 10
    companies = get_companies_by_employees_num()
    companies_paginated = Paginator(companies, default_paginator).get_page(page_number)
    return JsonResponse({
        "companies": [
            company.simple_to_dict_json() for company in companies_paginated.object_list
        ]
    })
