import time

from django.core.management.base import BaseCommand
from model_bakery import baker
from core.models import Company, Department, Employee, CostCenter, Cost, User


# TODO: isso aqui tá feio, gera nomes enormes pra empresa e pode ser melhorado usando Recipes
# do model_bakery. Porém, por enquanto é isso
class Command(BaseCommand):
    help = "Populates sample data"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_user(username="admin", password="password", is_staff=True, is_superuser=True)
            self.stdout.write(self.style.SUCCESS("Super User created"))
            self.stdout.write(self.style.SUCCESS('password: "password", username: "admin"'))
            time.sleep(0.3)

        if not User.objects.filter(username="user_teste"):
            User.objects.create_user(username="user_teste", password="password")
            self.stdout.write(self.style.SUCCESS("User created"))
            self.stdout.write(self.style.SUCCESS('password: "password", username: "user_teste"'))
            time.sleep(0.5)

        # Criando empresas
        companies = baker.make(Company, _quantity=5, _fill_optional=True)
        self.stdout.write(self.style.SUCCESS("Companies created"))

        for company in companies:
            # Criando departamentos para cada empresa
            departments = baker.make(Department, company=company, _quantity=3, _fill_optional=True)

            for department in departments:
                # Criando funcionários para cada departamento
                baker.make(
                    Employee, company=company, department=department, _quantity=10, _fill_optional=True
                )

                cost_centers = baker.make(
                    CostCenter, company=company, department=department, _quantity=5, _fill_optional=True
                )

                for cost_center in cost_centers:
                    # Criando registros de custos para cada centro de custo
                    baker.make(Cost, cost_center=cost_center, _quantity=10, _fill_optional=True)

        self.stdout.write(self.style.SUCCESS("Sample data populated successfully."))
