import json

from model_bakery.baker import make
from model_bakery.recipe import seq
from core.models import Department

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
