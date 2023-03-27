# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hs_core', '0004_auto_20150721_1125'),
    ]

    operations = [
        # START(ID=145,NAME=MigrationCreateGroupAccessTable,TYPE=CREATE,OBJECTS=[GroupAccess])
        migrations.CreateModel(
            name='GroupAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, help_text='whether group is currently active', editable=False)),
                ('discoverable', models.BooleanField(default=True, help_text='whether group description is discoverable by everyone', editable=False)),
                ('public', models.BooleanField(default=True, help_text='whether group members can be listed by everyone', editable=False)),
                ('shareable', models.BooleanField(default=True, help_text='whether group can be shared by non-owners', editable=False)),
                ('group', models.OneToOneField(related_query_name='gaccess', related_name='gaccess', null=True, editable=False, on_delete=models.CASCADE, to='auth.Group', help_text='group object that this object protects')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        # END(ID=145)
        # START(ID=146,NAME=MigrationCreateGroupResourcePrivilegeTable,TYPE=CREATE,OBJECTS=[GroupResourcePrivilege])
        migrations.CreateModel(
            name='GroupResourcePrivilege',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('privilege', models.IntegerField(default=3, editable=False, choices=[(1, 'Owner'), (2, 'Change'), (3, 'View')])),
                ('start', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        # END(ID=146)
        # START(ID=147,NAME=MigrationCreateResourceAccessTable,TYPE=CREATE,OBJECTS=[ResourceAccess])
        migrations.CreateModel(
            name='ResourceAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, help_text='whether resource is currently active')),
                ('discoverable', models.BooleanField(default=False, help_text='whether resource is discoverable by everyone')),
                ('public', models.BooleanField(default=False, help_text='whether resource data can be viewed by everyone')),
                ('shareable', models.BooleanField(default=True, help_text='whether resource can be shared by non-owners')),
                ('published', models.BooleanField(default=False, help_text='whether resource has been published')),
                ('immutable', models.BooleanField(default=False, help_text='whether to prevent all changes to the resource')),
                ('holding_groups', models.ManyToManyField(help_text='groups that hold this resource', related_name='group2resource', editable=False, through='hs_access_control.GroupResourcePrivilege', to='hs_access_control.GroupAccess')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        # END(ID=147)
        # START(ID=148,NAME=MigrationCreateUserAccessTable,TYPE=CREATE,OBJECTS=[UserAccess])
        migrations.CreateModel(
            name='UserAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, help_text='whether user is currently capable of action', editable=False)),
                ('admin', models.BooleanField(default=False, help_text='whether user is an administrator', editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        # END(ID=148)
        # START(ID=149,NAME=MigrationCreateUserGroupPrivilegeTable,TYPE=CREATE,OBJECTS=[UserGroupPrivilege])
        migrations.CreateModel(
            name='UserGroupPrivilege',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('privilege', models.IntegerField(default=3, editable=False, choices=[(1, 'Owner'), (2, 'Change'), (3, 'View')])),
                ('start', models.DateTimeField(auto_now=True)),
                ('grantor', models.ForeignKey(related_name='x2ugp', editable=False, on_delete=models.CASCADE, to='hs_access_control.UserAccess', help_text='grantor of privilege', null=True)),
                ('group', models.ForeignKey(related_name='g2ugp', editable=False, on_delete=models.CASCADE, to='hs_access_control.GroupAccess', help_text='group to which privilege applies', null=True)),
                ('user', models.ForeignKey(related_name='u2ugp', editable=False, on_delete=models.CASCADE, to='hs_access_control.UserAccess', help_text='user to be granted privilege', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        # END(ID=149)
        # START(ID=150,NAME=MigrationCreateUserResourcePrivilegeTable,TYPE=CREATE,OBJECTS=[UserResourcePrivilege])
        migrations.CreateModel(
            name='UserResourcePrivilege',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('privilege', models.IntegerField(default=3, editable=False, choices=[(1, 'Owner'), (2, 'Change'), (3, 'View')])),
                ('start', models.DateTimeField(auto_now=True)),
                ('grantor', models.ForeignKey(related_name='x2urp', editable=False, on_delete=models.CASCADE, to='hs_access_control.UserAccess', help_text='grantor of privilege', null=True)),
                ('resource', models.ForeignKey(related_name='r2urp', editable=False, on_delete=models.CASCADE, to='hs_access_control.ResourceAccess', help_text='resource to which privilege applies', null=True)),
                ('user', models.ForeignKey(related_name='u2urp', editable=False, on_delete=models.CASCADE, to='hs_access_control.UserAccess', help_text='user to be granted privilege', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        # END(ID=150)
        # START(ID=151,NAME=MigrationAlterUniqueTogetherUserResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.AlterUniqueTogether(
            name='userresourceprivilege',
            unique_together=set([('user', 'resource', 'grantor')]),
        ),
        # END(ID=151)
        # START(ID=152,NAME=MigrationAlterUniqueTogetherUserGroupPrivilegeTable,TYPE=ALTER,OBJECTS=[UserGroupPrivilege])
        migrations.AlterUniqueTogether(
            name='usergroupprivilege',
            unique_together=set([('user', 'group', 'grantor')]),
        ),
        # END(ID=152)
        # START(ID=153,NAME=MigrationAddFieldHeldGroupsUserAccessTable,TYPE=ALTER,OBJECTS=[UserAccess])
        migrations.AddField(
            model_name='useraccess',
            name='held_groups',
            field=models.ManyToManyField(help_text='groups held by this user', related_name='group2user', editable=False, through='hs_access_control.UserGroupPrivilege', to='hs_access_control.GroupAccess'),
            preserve_default=True,
        ),
        # END(ID=153)
        # START(ID=154,NAME=MigrationAddFieldHeldResourcesUserAccessTable,TYPE=ALTER,OBJECTS=[UserAccess])
        migrations.AddField(
            model_name='useraccess',
            name='held_resources',
            field=models.ManyToManyField(help_text='resources held by this user', related_name='resource2user', editable=False, through='hs_access_control.UserResourcePrivilege', to='hs_access_control.ResourceAccess'),
            preserve_default=True,
        ),
        # END(ID=154)
        # START(ID=155,NAME=MigrationAddFieldUserToUserAccessTable,TYPE=ALTER,OBJECTS=[UserAccess])
        migrations.AddField(
            model_name='useraccess',
            name='user',
            field=models.OneToOneField(related_query_name='uaccess', related_name='uaccess', null=True, editable=False, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        # END(ID=155)
        # START(ID=156,NAME=MigrationAddFieldHoldingUsersResourceAccessTable,TYPE=ALTER,OBJECTS=[ResourceAccess])
        migrations.AddField(
            model_name='resourceaccess',
            name='holding_users',
            field=models.ManyToManyField(help_text='users who hold this resource', related_name='user2resource', editable=False, through='hs_access_control.UserResourcePrivilege', to='hs_access_control.UserAccess'),
            preserve_default=True,
        ),
        # END(ID=156)
        # START(ID=157,NAME=MigrationAddFieldResourceResourceAccessTable,TYPE=ALTER,OBJECTS=[ResourceAccess])
        migrations.AddField(
            model_name='resourceaccess',
            name='resource',
            field=models.OneToOneField(related_query_name='raccess', related_name='raccess', null=True, editable=False, on_delete=models.CASCADE, to='hs_core.BaseResource'),
            preserve_default=True,
        ),
        # END(ID=157)
        # START(ID=158,NAME=MigrationAddFieldGrantorGroupResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.AddField(
            model_name='groupresourceprivilege',
            name='grantor',
            field=models.ForeignKey(related_name='x2grp', editable=False, on_delete=models.CASCADE, to='hs_access_control.UserAccess', help_text='grantor of privilege', null=True),
            preserve_default=True,
        ),
        # END(ID=158)
        # START(ID=159,NAME=MigrationAddFieldGroupGroupResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.AddField(
            model_name='groupresourceprivilege',
            name='group',
            field=models.ForeignKey(related_name='g2grp', editable=False, on_delete=models.CASCADE, to='hs_access_control.GroupAccess', help_text='group to be granted privilege', null=True),
            preserve_default=True,
        ),
        # END(ID=159)
        # START(ID=160,NAME=MigrationAddFieldResourceGroupResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.AddField(
            model_name='groupresourceprivilege',
            name='resource',
            field=models.ForeignKey(related_name='r2grp', editable=False, on_delete=models.CASCADE, to='hs_access_control.ResourceAccess', help_text='resource to which privilege applies', null=True),
            preserve_default=True,
        ),
        # END(ID=160)
        # START(ID=161,NAME=MigrationAlterUniqueTogetherGroupResourcePrivilegeTable,TYPE=ALTER,OBJECTS=[GroupResourcePrivilege])
        migrations.AlterUniqueTogether(
            name='groupresourceprivilege',
            unique_together=set([('group', 'resource', 'grantor')]),
        ),
        # END(ID=161)
        # START(ID=162,NAME=MigrationAddFieldGroupHeldResourcesGroupAccessTable,TYPE=ALTER,OBJECTS=[GroupAccess])
        migrations.AddField(
            model_name='groupaccess',
            name='held_resources',
            field=models.ManyToManyField(help_text='resources held by the group', related_name='resource2group', editable=False, through='hs_access_control.GroupResourcePrivilege', to='hs_access_control.ResourceAccess'),
            preserve_default=True,
        ),
        # END(ID=162)
        # START(ID=163,NAME=MigrationAddFieldGroupMembersGroupAccessTable,TYPE=ALTER,OBJECTS=[GroupAccess])
        migrations.AddField(
            model_name='groupaccess',
            name='members',
            field=models.ManyToManyField(help_text='members of the group', related_name='user2group', editable=False, through='hs_access_control.UserGroupPrivilege', to='hs_access_control.UserAccess'),
            preserve_default=True,
        ),
        # END(ID=163)
    ]
