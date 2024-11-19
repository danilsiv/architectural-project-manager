# Generated by Django 5.1.3 on 2024-11-19 05:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0003_remove_project_team_team_worker_team_project_team"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="team",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="projects",
                to="management.team",
            ),
        ),
    ]
