# EU poderia ter usado uma lib como django-safedelete, ou algo assim.
# Se fosse um projeto de longo prazo, isso com certeza seria melhor, pois
# demandaria menos tempo testando as funcionalidades, e o retorno do
# método .delete() seria como o padrão do django, não modificando o fluxo para trabalhar.
from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    """
    Sobrescreve o comportamento padrão de deleção a partir de um QuerySet
    """

    def delete(self):
        self.update(is_active=False)


class SoftDeleteManager(models.Manager):
    """
    Manager para não retornar multas deletadas em consultas normais
    """

    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).exclude(is_active=False)

    def all_without_exception(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteBaseModel(models.Model):
    """
    Classe base abstrata para sobrescrever o comportamento de instance.delete().

    Exemplos:
        class MyModel(SoftDeleteModel):
            pass

        >>> my_model = MyModel()
        >>> my_model.delete()
        >>> my_model.refresh_from_db()
        >>> my_model.is_active
        True
    """

    class Meta:
        abstract = True

    objects = SoftDeleteManager()
    # field que checa se o modelo foi deletado ou não
    is_active = models.BooleanField(default=True, db_index=True)

    def delete(self):
        related_models = self._collect_relation_models()
        self.is_active = False
        self.save(update_fields=["is_active"])
        self._soft_delete_related_models(related_models=related_models)

    def _collect_relation_models(self):
        relation_models = []
        for field in self._meta.get_fields():
            if not field.one_to_many:
                continue

            related_model = field.related_model
            if not issubclass(related_model, SoftDeleteBaseModel):
                raise TypeError("Models are expected to extend SoftDeleteBaseModel")

            relation_models.append(related_model)

        return relation_models

    def _soft_delete_related_models(self, related_models: list[models.base.Model]) -> None:
        if not related_models:
            return

        for model in related_models:
            model.objects.all().delete()
