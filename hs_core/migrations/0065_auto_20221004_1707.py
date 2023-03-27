# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-10-04 17:07
from __future__ import unicode_literals

from django.db import migrations, models


def set_creator_contributor_active_user_default(apps, schema_editor):
    Creator = apps.get_model("hs_core", "Creator")
    Contributor = apps.get_model("hs_core", "Contributor")
    Creator.objects.update(is_active_user=False)
    Contributor.objects.update(is_active_user=False)


class Migration(migrations.Migration):

    dependencies = [
        ('hs_core', '0064_auto_20220620_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='is_active_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='creator',
            name='is_active_user',
            field=models.BooleanField(default=False),
        ),
        migrations.RunSQL("ALTER TABLE hs_core_creator ALTER COLUMN is_active_user SET DEFAULT FALSE;"),
        migrations.RunSQL("ALTER TABLE hs_core_contributor ALTER COLUMN is_active_user SET DEFAULT FALSE;"),
        migrations.RunPython(code=set_creator_contributor_active_user_default, reverse_code=migrations.RunPython.noop)
    ]
