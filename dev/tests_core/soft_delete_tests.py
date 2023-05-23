import pytest
from model_bakery.baker import make

from core.models import Company

@pytest.fixture
def activity_company(db):
    return make(Company, is_deleted=False)

def test_query_all_without_exception(db):
    make(Company, is_deleted=True)

    assert Company.objects.all().count() == 0
    assert Company.objects.all_without_exception().first().is_deleted


def test_no_delete_soft_delete_from_instance(activity_company):
    activity_company.delete()
    activity_company.refresh_from_db()

    assert activity_company.is_deleted


def test_no_delete_soft_delete_from_queryset(activity_company):
    Company.objects.all().delete()
    companies = Company.objects.all_without_exception()
    assert len(companies) == 1
    assert companies[0].is_deleted


def test_no_delete_soft_delete_from_reverse_relation_model(activity_company):
    employee = make("core.Employee", company=activity_company)
    activity_company.employees.all().delete()
    employee.refresh_from_db()
    assert employee.is_deleted
