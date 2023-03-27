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
        migrations.RemoveField(
            model_name='groupresourceprivilege',
            name='grantor',
        ),
        migrations.AlterUniqueTogether(
            name='usergroupprivilege',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='usergroupprivilege',
            name='user',
        ),
        migrations.RemoveField(
            model_name='usergroupprivilege',
            name='group',
        ),
        migrations.RemoveField(
            model_name='usergroupprivilege',
            name='grantor',
        ),
        migrations.AlterUniqueTogether(
            name='userresourceprivilege',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='userresourceprivilege',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userresourceprivilege',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='userresourceprivilege',
            name='grantor',
        ),
    ]
