# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0007_manual_populate_new_fields'),
    ]

    operations = [
        # START(ID=191,NAME=MigrationRemoveFieldHeldResourcesGroupAccessTable,TYPE=ALTER,OBJECTS=[GroupAccess])
        migrations.RemoveField(
            model_name='groupaccess',
            name='held_resources',
        ),
        # END(ID=191)
        # START(ID=192,NAME=MigrationRemoveFieldMembersGroupAccessTable,TYPE=ALTER,OBJECTS=[GroupAccess])
        migrations.RemoveField(
            model_name='groupaccess',
            name='members',
        ),
        # END(ID=192)
        # START(ID=193,NAME=MigrationRemoveFieldHoldingGroupsResourceAccessTable,TYPE=ALTER,OBJECTS=[ResourceAccess])
        migrations.RemoveField(
            model_name='resourceaccess',
            name='holding_groups',
        ),
        # END(ID=193)
        # START(ID=194,NAME=MigrationRemoveFieldHoldingUsersResourceAccessTable,TYPE=ALTER,OBJECTS=[ResourceAccess])
        migrations.RemoveField(
            model_name='resourceaccess',
            name='holding_users',
        ),
        # END(ID=194)
        # START(ID=195,NAME=MigrationRemoveFieldHeldGroupsUserAccessTable,TYPE=ALTER,OBJECTS=[UserAccess])
        migrations.RemoveField(
            model_name='useraccess',
            name='held_groups',
        ),
        # END(ID=195)
        # START(ID=196,NAME=MigrationRemoveFieldHeldResourcesUserAccessTable,TYPE=ALTER,OBJECTS=[UserAccess])
        migrations.RemoveField(
            model_name='useraccess',
            name='held_resources',
        ),
        # END(ID=196)
    ]
