from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).exclude(is_deleted=True)

    def all_without_exception(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteBaseModel(models.Model):
    """ Base model that implements soft delete logic """
    class Meta:
        abstract = True
    objects = SoftDeleteManager()

    is_deleted = models.BooleanField(default=False, db_index=True)

    def delete(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])
