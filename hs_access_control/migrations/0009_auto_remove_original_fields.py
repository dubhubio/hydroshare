# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0008_auto_remove_many2many_relationships'),
    ]

    operations = [
        # START(ID=197,NAME=MigrationAlterUniqueTogetherSetGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.AlterUniqueTogether(
            name='groupresourceprivilege',
            unique_together=set([]),
        ),
        # END(ID=197)
        # START(ID=198,NAME=MigrationRemoveFieldResourceGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.RemoveField(
            model_name='groupresourceprivilege',
            name='resource',
        ),
        # END(ID=198)
        # START(ID=199,NAME=MigrationRemoveFieldGroupGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.RemoveField(
            model_name='groupresourceprivilege',
            name='group',
        ),
        # END(ID=199)
        # START(ID=200,NAME=MigrationRemoveFieldGrantorGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.RemoveField(
            model_name='groupresourceprivilege',
            name='grantor',
        ),
        # END(ID=200)
        # START(ID=201,NAME=MigrationAlterUniqueTogetherSetUserGroupPrivilege,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.AlterUniqueTogether(
            name='usergroupprivilege',
            unique_together=set([]),
        ),
        # END(ID=201)
        # START(ID=202,NAME=MigrationRemoveFieldUserFromUserGroupPrivilege,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.RemoveField(
            model_name='usergroupprivilege',
            name='user',
        ),
        # END(ID=202)
        # START(ID=203,NAME=MigrationRemoveFieldGroupFromUserGroupPrivilege,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.RemoveField(
            model_name='usergroupprivilege',
            name='group',
        ),
        # END(ID=203)
        # START(ID=204,NAME=MigrationRemoveFieldGrantorFromUserGroupPrivilege,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.RemoveField(
            model_name='usergroupprivilege',
            name='grantor',
        ),
        # END(ID=204)
        # START(ID=205,NAME=MigrationAlterUniqueTogetherSetUserResourcePrivilege,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.AlterUniqueTogether(
            name='userresourceprivilege',
            unique_together=set([]),
        ),
        # END(ID=205)
        # START(ID=206,NAME=MigrationRemoveFieldUserFromUserResourcePrivilege,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.RemoveField(
            model_name='userresourceprivilege',
            name='user',
        ),
        # END(ID=206)
        # START(ID=207,NAME=MigrationRemoveFieldResourceFromUserResourcePrivilege,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.RemoveField(
            model_name='userresourceprivilege',
            name='resource',
        ),
        # END(ID=207)
        # START(ID=208,NAME=MigrationRemoveFieldGrantorFromUserResourcePrivilege,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.RemoveField(
            model_name='userresourceprivilege',
            name='grantor',
        ),
        # END(ID=208)
    ]
