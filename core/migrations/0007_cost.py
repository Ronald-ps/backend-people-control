# Generated by Django 4.2 on 2023-05-26 00:02

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_remove_department_cost_center_costcenter"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("value", models.DecimalField(decimal_places=2, default=Decimal("0"), max_digits=10)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_planned_cost", models.BooleanField(default=True)),
                (
                    "cost_center",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="costs", to="core.costcenter"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
