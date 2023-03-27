# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0010_auto_rename_related_names'),
    ]

    operations = [
        # START(ID=218,NAME=MigrationRenameFieldGrantorOrNewGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.RenameField(
            model_name='groupresourceprivilege',
            old_name='grantornew',
            new_name='grantor',
        ),
        # END(ID=218)
        # START(ID=219,NAME=MigrationRenameFieldGroupNewGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.RenameField(
            model_name='groupresourceprivilege',
            old_name='groupnew',
            new_name='group',
        ),
        # END(ID=219)
        # START(ID=220,NAME=MigrationRenameFieldResourceNewGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.RenameField(
            model_name='groupresourceprivilege',
            old_name='resourcenew',
            new_name='resource',
        ),
        # END(ID=220)
        # START(ID=221,NAME=MigrationRenameFieldGrantOrNewGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.RenameField(
            model_name='usergroupprivilege',
            old_name='grantornew',
            new_name='grantor',
        ),
        # END(ID=221)
        # START(ID=222,NAME=MigrationRenameFieldGroupNewGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.RenameField(
            model_name='usergroupprivilege',
            old_name='groupnew',
            new_name='group',
        ),
        # END(ID=222)
        # START(ID=223,NAME=MigrationRenameFieldUserNewGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.RenameField(
            model_name='usergroupprivilege',
            old_name='usernew',
            new_name='user',
        ),
        # END(ID=223)
        # START(ID=224,NAME=MigrationRenameFieldGrantOrNewGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.RenameField(
            model_name='userresourceprivilege',
            old_name='grantornew',
            new_name='grantor',
        ),
        # END(ID=224)
        # START(ID=225,NAME=MigrationRenameFieldResourceNewGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.RenameField(
            model_name='userresourceprivilege',
            old_name='resourcenew',
            new_name='resource',
        ),
        # END(ID=225)
        # START(ID=226,NAME=MigrationRenameFieldUserNewGroupResourcePrivilege,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.RenameField(
            model_name='userresourceprivilege',
            old_name='usernew',
            new_name='user',
        ),
        # END(ID=226)
    ]
