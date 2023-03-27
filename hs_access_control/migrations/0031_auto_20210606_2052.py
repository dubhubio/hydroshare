# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-06 20:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0030_groupcommunityinvite_groupcommunityrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupcommunityinvite',
            name='when_requested',
            field=models.DateTimeField(default=None, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='groupcommunityinvite',
            name='when_responded',
            field=models.DateTimeField(default=None, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='groupcommunityrequest',
            name='when_requested',
            field=models.DateTimeField(default=None, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='groupcommunityrequest',
            name='when_responded',
            field=models.DateTimeField(default=None, editable=False, null=True),
        ),
    ]
