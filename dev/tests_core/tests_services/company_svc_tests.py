from model_bakery.baker import make
from model_bakery.recipe import seq

from core.services.company_svc import get_companies_by_employees_num


def test_get_companies_by_employees_num_order_by_employees_num(db):
    companies = make("core.Company", _quantity=3)
    make("core.Employee", company=companies[1], department__company_id=companies[1].id, _quantity=1)
    make("core.Employee", company=companies[2], department__company_id=companies[2].id, _quantity=2)

    filtered_companies = get_companies_by_employees_num()
    list(filtered_companies)
    assert companies[0].id == filtered_companies[2].id
    assert companies[1].id == filtered_companies[1].id
    assert companies[2].id == filtered_companies[0].id

    assert filtered_companies[0].employees_count == 2
    assert filtered_companies[1].employees_count == 1
    assert filtered_companies[2].employees_count == 0


def test_get_companies_by_employees_num_order_by_name(db):
    companies = make("core.Company", name=seq("company", increment_by=-1, start=3), _quantity=3)
    # nomes: company3, company2, company1
    filtered_companies = get_companies_by_employees_num()
    assert filtered_companies[0].name == companies[2].name
    assert filtered_companies[1].name == companies[1].name
    assert filtered_companies[2].name == companies[0].name
