# EU poderia ter usado uma lib como django-safedelete, ou algo assim.
# Se fosse um projeto de longo prazo, isso com certeza seria melhor, pois
# demandaria menos tempo testando as funcionalidades, e o retorno do
# método .delete() seria como o padrão do django, não modificando o fluxo para trabalhar.
from django.db import models

class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_active=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).exclude(is_active=False)

    def all_without_exception(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteBaseModel(models.Model):
    """ Base model that implements soft delete logic """
    class Meta:
        abstract = True
    objects = SoftDeleteManager()
    # field that checks if the data was "deleted" or not
    is_active = models.BooleanField(default=True, db_index=True)

    def delete(self):
        related_models = self._collect_relation_models()
        self.is_active = False
        self.save(update_fields=["is_active"])
        self._soft_delete_related_models(related_models=related_models)


    # TODO: retornar aqui uma lista de SoftDeleteBaseModel
    def _collect_relation_models(self) -> list[models.base.ModelBase]:
        relation_models = []
        for field in self._meta.get_fields():
            if not field.one_to_many:
                continue

            related_model = field.related_model
            # TODO: usar aqui direto a extensão do modelo, e não o QuerySet
            if not isinstance(related_model.objects.all(), SoftDeleteQuerySet):
                raise TypeError("Models are expected to extend SoftDeleteBaseModel")

            relation_models.append(related_model)

        return relation_models

    def _soft_delete_related_models(self, related_models: list[models.base.Model]) -> None:
        if not related_models:
            return

        for model in related_models:
            model.objects.all().delete()
