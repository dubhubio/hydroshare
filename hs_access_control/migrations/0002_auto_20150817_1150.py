# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.contrib.auth.models import User
from hs_access_control.models import UserAccess


def migrate_users(apps, schema_editor):
    # create a 'UserAccess' record for each existing user - needed for the new access control to work
    # START(ID=164,NAME=ForMigrationDeleteAllUserAccess,TYPE=DELETE,OBJECTS=[UserAccess])
    UserAccess.objects.all().delete()
    # END(ID=164)
    # START(ID=165,NAME=ForMigrationLoopAllUserObjects,TYPE=SELECT,OBJECTS=[User])
    for u in User.objects.all():
    # END(ID=165)
        ua = UserAccess(user=u)
        # START(ID=166,NAME=ForMigrationCreateUserAccess,TYPE=INSERT,OBJECTS=[UserAccess])
        ua.save()
        # END(ID=166)


def undo_migrate_users(apps, schema_editor):
    # delete all 'UserAccess' records
    # START(ID=167,NAME=MigrationDeleteAllUserAccess,TYPE=DELETE,OBJECTS=[UserAccess])
    UserAccess.objects.all().delete()
    # END(ID=167)


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(code=migrate_users, reverse_code=undo_migrate_users),
    ]
