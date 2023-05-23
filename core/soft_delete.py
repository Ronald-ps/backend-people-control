from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_active=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).exclude(is_active=False)

    def all_without_exception(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteBaseModel(models.Model):
    """ Base model that implements soft delete logic """
    class Meta:
        abstract = True
    objects = SoftDeleteManager()
    # field that checks if the data was "deleted" or not
    is_active = models.BooleanField(default=True, db_index=True)

    def delete(self):
        self.is_active = False
        self.save(update_fields=["is_active"])
