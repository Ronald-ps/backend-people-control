from model_bakery.baker import make

from core.models import Company

def test_query_all_without_exception(db):
    make(Company, is_deleted=True)

    assert Company.objects.all().count() == 0
    assert Company.objects.all_without_exception().first().is_deleted == True


def test_no_delete_soft_delete_models(db):
    company = make(Company, is_deleted=False)
    company.delete()
    company.refresh_from_db()

    assert company.is_deleted
