# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0012_auto_disallow_nulls'),
    ]

    operations = [
        # START(ID=239,NAME=MigrationAlterUniqueTogetherGroupResourcePrivilege0013,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.AlterUniqueTogether(
            name='groupresourceprivilege',
            unique_together=set([('group', 'resource', 'grantor')]),
        ),
        # END(ID=239)
        # START(ID=240,NAME=MigrationAlterUniqueTogetherUserGroupPrivilege0013,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.AlterUniqueTogether(
            name='usergroupprivilege',
            unique_together=set([('user', 'group', 'grantor')]),
        ),
        # END(ID=240)
        # START(ID=241,NAME=MigrationAlterUniqueTogetherUserResourcePrivilege0013,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.AlterUniqueTogether(
            name='userresourceprivilege',
            unique_together=set([('user', 'resource', 'grantor')]),
        ),
        # END(ID=241)
    ]
