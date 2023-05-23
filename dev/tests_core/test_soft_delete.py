from model_bakery.baker import make

def test_soft_delete_no_delete(db):
  make("core.Company", is_deleted=False, _fill_optional=True)
