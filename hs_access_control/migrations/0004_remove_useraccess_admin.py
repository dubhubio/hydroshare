# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0003_auto_20150824_2215'),
    ]

    operations = [
        # START(ID=177,NAME=MigrationRemoveFieldAdminUserResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[UserAccess])
        migrations.RemoveField(
            model_name='useraccess',
            name='admin',
        ),
        # END(ID=177)
    ]
