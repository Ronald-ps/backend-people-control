# Generated by Django 4.2 on 2023-05-24 10:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_company_department_employee"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="state_acronym",
            field=models.CharField(default="MG", max_length=2),
            preserve_default=False,
        ),
    ]
