# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0015_manual_remove_redundant_privileges'),
    ]

    operations = [
        # START(ID=285,NAME=MigrationAlterUniqueTogetherGroupResourcePrivilegeSetGroupResource,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.AlterUniqueTogether(
            name='groupresourceprivilege',
            unique_together=set([('group', 'resource')]),
        ),
        # END(ID=285)
        # START(ID=286,NAME=MigrationAlterUniqueTogetherUserGroupPrivilegeSetGroupUser,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.AlterUniqueTogether(
            name='usergroupprivilege',
            unique_together=set([('user', 'group')]),
        ),
        # END(ID=286)
        # START(ID=287,NAME=MigrationAlterUniqueTogetherUserResourcePrivilegeSetResourceUser,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.AlterUniqueTogether(
            name='userresourceprivilege',
            unique_together=set([('user', 'resource')]),
        ),
        # END(ID=287)
    ]
