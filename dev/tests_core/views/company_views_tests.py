from http import HTTPStatus
import json

from model_bakery.baker import make
from model_bakery.recipe import seq

from core.views import company_simple_list

def test_company_simple_list(db, rf, user):
  companies = make("core.Company", name=seq("company"), _quantity=3)
  make("core.Employee", company=companies[2], department__company_id=companies[0].id, _quantity=2)
  # Número de funcionários impacta na ordenação
  make("core.Employee", company=companies[1], department__company_id=companies[1].id, _quantity=1)

  request = rf.get("/company/simple-list")
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
  request = rf.post("/company/simple-list", {})
  request.user = user
  response = company_simple_list(request)
  assert response.status_code == HTTPStatus.FORBIDDEN

  request = rf.get("/company/simple-list")
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

  request = rf.get("/company/simple-list", { "page": 2 })
  request.user = user
  response = company_simple_list(request)
  assert response.status_code == HTTPStatus.OK

  response_content = json.loads(response.content)
  assert len(response_content["companies"]) == default_num_pagination

  response_companies_ids = [c["id"] for c in response_content["companies"]]
  assert sorted(response_companies_ids) == sorted(companies_without_employees_ids)
