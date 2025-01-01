# Generated by Django 4.2.16 on 2024-12-30 04:03

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import laid_out.goal.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GoalEntry",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, default="New Goal Entry", max_length=255, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "data",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.JSONField(
                            blank=True, default=laid_out.goal.models.default_goal_node, null=True
                        ),
                        default=laid_out.goal.models.default_goal_data,
                        size=None,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="goal_entries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Goal Entry",
                "verbose_name_plural": "Goal Entries",
            },
        ),
    ]