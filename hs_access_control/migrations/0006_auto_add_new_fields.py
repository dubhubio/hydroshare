# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hs_core', '0014_auto_20151123_1451'),
        ('hs_access_control', '0005_remove_useraccess_active'),
    ]

    operations = [
        # START(ID=179,NAME=MigrationAddFieldGrantOrNewGroupResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.AddField(
            model_name='groupresourceprivilege',
            name='grantornew',
            field=models.ForeignKey(related_name='x2grpnew', editable=False, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, help_text='grantor of privilege', null=True),
            preserve_default=True,
        ),
        # END(ID=179)
        # START(ID=180,NAME=MigrationAddFieldGroupNewGroupResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.AddField(
            model_name='groupresourceprivilege',
            name='groupnew',
            field=models.ForeignKey(related_name='g2grpnew', editable=False, on_delete=models.CASCADE, to='auth.Group', help_text='group to be granted privilege', null=True),
            preserve_default=True,
        ),
        # END(ID=180)
        # START(ID=181,NAME=MigrationAddFieldResourceNewGroupResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.AddField(
            model_name='groupresourceprivilege',
            name='resourcenew',
            field=models.ForeignKey(related_name='r2grpnew', editable=False, on_delete=models.CASCADE, to='hs_core.BaseResource', help_text='resource to which privilege applies', null=True),
            preserve_default=True,
        ),
        # END(ID=181)
        # START(ID=182,NAME=MigrationAddFieldGrantOrNewUserGroupPrivilegeTable,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.AddField(
            model_name='usergroupprivilege',
            name='grantornew',
            field=models.ForeignKey(related_name='x2ugpnew', editable=False, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, help_text='grantor of privilege', null=True),
            preserve_default=True,
        ),
        # END(ID=182)
        # START(ID=183,NAME=MigrationAddFieldGroupNewUserGroupPrivilegeTable,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.AddField(
            model_name='usergroupprivilege',
            name='groupnew',
            field=models.ForeignKey(related_name='g2ugpnew', editable=False, on_delete=models.CASCADE, to='auth.Group', help_text='group to which privilege applies', null=True),
            preserve_default=True,
        ),
        # END(ID=183)
        # START(ID=184,NAME=MigrationAddFieldUserNewUserGroupPrivilegeTable,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.AddField(
            model_name='usergroupprivilege',
            name='usernew',
            field=models.ForeignKey(related_name='u2ugpnew', editable=False, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, help_text='user to be granted privilege', null=True),
            preserve_default=True,
        ),
        # END(ID=184)
        # START(ID=185,NAME=MigrationAddFieldGrantOrNewUserResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.AddField(
            model_name='userresourceprivilege',
            name='grantornew',
            field=models.ForeignKey(related_name='x2urpnew', editable=False, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, help_text='grantor of privilege', null=True),
            preserve_default=True,
        ),
        # END(ID=185)
        # START(ID=186,NAME=MigrationAddFieldResourceNewUserResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.AddField(
            model_name='userresourceprivilege',
            name='resourcenew',
            field=models.ForeignKey(related_name='r2urpnew', editable=False, on_delete=models.CASCADE, to='hs_core.BaseResource', help_text='resource to which privilege applies', null=True),
            preserve_default=True,
        ),
        # END(ID=186)
        # START(ID=187,NAME=MigrationAddFieldUserNewUserResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.AddField(
            model_name='userresourceprivilege',
            name='usernew',
            field=models.ForeignKey(related_name='u2urpnew', editable=False, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, help_text='user to be granted privilege', null=True),
            preserve_default=True,
        ),
        # END(ID=187)
    ]
