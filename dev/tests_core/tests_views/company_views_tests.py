import json
from http import HTTPStatus

from model_bakery.baker import make
from model_bakery.recipe import seq
from rest_framework.test import force_authenticate

from core.models import Company
from core.views import company_simple_list
from core.viewsets import CompanyViewSet
from core.serializers.br_company_serializer import CompanySerializer


def test_company_simple_list(db, rf, user):
    companies = make("core.Company", name=seq("company"), _quantity=3)
    make("core.Employee", company=companies[2], department__company_id=companies[0].id, _quantity=2)
    # Número de funcionários impacta na ordenação
    make("core.Employee", company=companies[1], department__company_id=companies[1].id, _quantity=1)

    request = rf.get("/companies/simple-list")
    request.user = user
    response = company_simple_list(request)

    response_content = json.loads(response.content)
    expected_response = {
        "companies": [
            {"id": companies[2].id, "name": companies[2].name},
            {"id": companies[1].id, "name": companies[1].name},
            {"id": companies[0].id, "name": companies[0].name},
        ]
    }
    assert response_content == expected_response


# TODO: setar um setup de banco de dados para ser usado o mesmo banco de dados.
# recriar um banco de dados é custoso
def test_company_simple_list_invalide_request(db, rf, user):
    request = rf.post("/companies/simple-list", {})
    request.user = user
    response = company_simple_list(request)
    assert response.status_code == HTTPStatus.FORBIDDEN

    request = rf.get("/companies/simple-list")
    request.user = None
    response = company_simple_list(request)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_company_simple_list_pagination(db, rf, user):
    default_num_pagination = 10
    companies_without_employees = make("core.Company", name=seq("company"), _quantity=10)
    companies_with_employees = make("core.Company", name=seq("company"), _quantity=10)
    companies_without_employees_ids = [c.id for c in companies_without_employees]
    # pela ordenação, companies sem funcionário viriam na próxima paginação
    for company in companies_with_employees:
        make("core.Employee", company=company, department__company_id=company.id, _quantity=2)

    request = rf.get("/companies/simple-list", {"page": 2})
    request.user = user
    response = company_simple_list(request)
    assert response.status_code == HTTPStatus.OK

    response_content = json.loads(response.content)
    assert len(response_content["companies"]) == default_num_pagination

    response_companies_ids = [c["id"] for c in response_content["companies"]]
    assert sorted(response_companies_ids) == sorted(companies_without_employees_ids)


def test_company_viewset_create(drf_api_client, user, db):
    request_data = {
        "id": 3,
        "cnpj": "98765432000101",
        "cep": "54321098",
        "state_acronym": "RJ",
        "name": "Indústria XYZ S/A",
        "employee_count": 500,
        "address": "Avenida das Amostras, 456",
        "city": "Rio de Janeiro",
        "country": "Brasil",
    }
    headers = {"Content-Type": "application/json"}
    request = drf_api_client.post("/api/companies/", request_data, format="json", headers=headers)
    request.user = user
    force_authenticate(request, user=user)

    view = CompanyViewSet.as_view(actions={"post": "create"})
    response = view(request)
    serializer = CompanySerializer(Company.objects.first())
    assert response.status_code == 201
    assert response.data == serializer.data
