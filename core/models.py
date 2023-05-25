from django.db import models
from django.contrib.auth.models import AbstractUser

from core.utils.soft_delete import SoftDeleteBaseModel


class User(AbstractUser):
    """ Extend default auth User  """
    def to_dict_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }


class Company(SoftDeleteBaseModel):
    """ Modelo de empresa válido para o Brasil """
    # TODO: empresas de outros países não tem cnpj. Tem de ser null=True
    name = models.TextField()
    cnpj = models.CharField(max_length=14, unique=True)
    cep = models.CharField(max_length=8)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state_acronym = models.CharField(max_length=2)
    country = models.CharField(max_length=100)

    def simple_to_dict_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Department(SoftDeleteBaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="departments")
    # TODO: pensar melhor sobre como deve ser esse centro de custos
    # vou deixar esse carinha nulo por enquanto, até descobrir sobre como deve ser um centro de custos
    cost_center = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    integration_code = models.CharField(max_length=100)


class Employee(SoftDeleteBaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    date_of_entry = models.DateField()
    date_of_departure = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100)
