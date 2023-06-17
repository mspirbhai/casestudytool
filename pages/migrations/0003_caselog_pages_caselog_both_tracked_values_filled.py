# Generated by Django 4.2 on 2023-06-17 09:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0002_trackedmetric_caselog_tracked_value_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="caselog",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("tracked_description__isnull", True),
                    ("tracked_value__isnull", True),
                ),
                name="pages_caselog_both_tracked_values_filled",
            ),
        ),
    ]