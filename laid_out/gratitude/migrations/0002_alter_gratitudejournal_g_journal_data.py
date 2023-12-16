# Generated by Django 4.2.8 on 2023-12-16 13:26

import django.contrib.postgres.fields
from django.db import migrations, models
import laid_out.gratitude.models


class Migration(migrations.Migration):
    dependencies = [
        ("gratitude", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gratitudejournal",
            name="g_journal_data",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.JSONField(
                    blank=True, default=laid_out.gratitude.models.default_g_journal_node, null=True
                ),
                default=laid_out.gratitude.models.default_g_journal_data,
                size=None,
            ),
        ),
    ]
