# -*- coding: utf-8 -*-


from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hs_access_control', '0013_auto_add_uniqueness_constraints'),
    ]

    operations = [
        # START(ID=242,NAME=MigrationCreateTableGroupMembershipRequest,TYPE=CREATE,OBJECTS=[GroupMembershipRequest])
        migrations.CreateModel(
            name='GroupMembershipRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('group_to_join', models.ForeignKey(related_name='g2gmrequest', on_delete=models.CASCADE, to='auth.Group')),
                ('invitation_to', models.ForeignKey(related_name='iu2gmrequest', on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('request_from', models.ForeignKey(related_name='ru2gmrequest', on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL)),
            ],
        ),
        # END(ID=242)
        # START(ID=243,NAME=MigrationAlterUniqueTogetherUserResourcePrivilege,TYPE=ALTER,OBJECTS=[UserResourcePrivilege])
        migrations.AddField(
            model_name='groupaccess',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 24, 16, 28, 14, 996767), auto_now_add=True),
            preserve_default=False,
        ),
        # END(ID=243)
        # START(ID=244,NAME=MigrationAddFieldDescriptionGroupAccess,TYPE=ALTER,OBJECTS=[GroupAccess])
        migrations.AddField(
            model_name='groupaccess',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        # END(ID=244)
        # START(ID=245,NAME=MigrationAddFieldPictureGroupAccess,TYPE=ALTER,OBJECTS=[GroupAccess])
        migrations.AddField(
            model_name='groupaccess',
            name='picture',
            field=models.ImageField(null=True, upload_to='group', blank=True),
        ),
        # END(ID=245)
        # START(ID=246,NAME=MigrationAddFieldPurposeGroupAccess,TYPE=ALTER,OBJECTS=[GroupAccess])
        migrations.AddField(
            model_name='groupaccess',
            name='purpose',
            field=models.TextField(null=True, blank=True),
        ),
        # END(ID=246)
    ]
