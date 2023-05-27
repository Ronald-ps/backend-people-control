import pytest
from model_bakery.baker import make

from core.models import Company


@pytest.fixture
def activity_company(db):
    return make(Company, is_active=True)


def test_query_all_without_exception(db):
    make(Company, is_active=False)

    assert Company.objects.all().count() == 0
    assert not Company.objects.all_without_exception().first().is_active


def test_no_delete_soft_delete_from_instance(activity_company):
    activity_company.delete()
    activity_company.refresh_from_db()

    assert not activity_company.is_active


def test_no_delete_soft_delete_from_queryset(activity_company):
    Company.objects.all().delete()
    companies = Company.objects.all_without_exception()
    assert len(companies) == 1
    assert not companies[0].is_active


def test_no_delete_soft_delete_from_reverse_relation_model(activity_company):
    employee = make("core.Employee", company=activity_company)
    activity_company.employees.all().delete()
    employee.refresh_from_db()
    assert not employee.is_active


def test_soft_delete_in_cascade_deletion(activity_company):
    employee = make("core.Employee", company=activity_company)
    activity_company.delete()
    employee.refresh_from_db()
    assert not employee.is_active
