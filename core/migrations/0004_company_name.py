# Generated by Django 4.2 on 2023-05-24 10:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_company_state_acronym"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="name",
            field=models.TextField(default="whatever"),
            preserve_default=False,
        ),
    ]
