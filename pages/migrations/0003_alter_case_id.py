# Generated by Django 4.2 on 2023-06-10 12:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0002_rename_cases_case"),
    ]

    operations = [
        migrations.AlterField(
            model_name="case",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
