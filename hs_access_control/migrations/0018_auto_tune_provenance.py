# -*- coding: utf-8 -*-


from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0017_auto_add_provenance'),
    ]

    operations = [
        # START(ID=295,NAME=MigrationAddFieldBooleanUndoneGroupResourceProvenance,TYPE=ALTER,OBJECTS=[GroupResourceProvenance])
        migrations.AddField(
            model_name='groupresourceprovenance',
            name='undone',
            field=models.BooleanField(default=False, editable=False),
        ),
        # END(ID=295)
        # START(ID=296,NAME=MigrationAddFieldBooleanUndoneUserGroupProvenance,TYPE=ALTER,OBJECTS=[UserGroupProvenance])
        migrations.AddField(
            model_name='usergroupprovenance',
            name='undone',
            field=models.BooleanField(default=False, editable=False),
        ),
        # END(ID=296)
        # START(ID=296,NAME=MigrationAddFieldBooleanUndoneUserResourceProvenance,TYPE=ALTER,OBJECTS=[UserResourceProvenance])
        migrations.AddField(
            model_name='userresourceprovenance',
            name='undone',
            field=models.BooleanField(default=False, editable=False),
        ),
        # END(ID=296)
        # START(ID=297,NAME=MigrationAlterFieldGrantorFkGroupResourceProvenance,TYPE=ALTER,OBJECTS=[GroupResourceProvenance])
        migrations.AlterField(
            model_name='groupresourceprovenance',
            name='grantor',
            field=models.ForeignKey(related_name='x2grq', editable=False, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, help_text='grantor of privilege', null=True),
        ),
        # END(ID=297)
        # START(ID=298,NAME=MigrationAlterFieldGrantorFkUserGroupProvenance,TYPE=ALTER,OBJECTS=[UserGroupProvenance])
        migrations.AlterField(
            model_name='usergroupprovenance',
            name='grantor',
            field=models.ForeignKey(related_name='x2ugq', editable=False, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, help_text='grantor of privilege', null=True),
        ),
        # END(ID=298)
        # START(ID=299,NAME=MigrationAlterFieldGrantorFkUserResourceProvenance,TYPE=ALTER,OBJECTS=[UserResourceProvenance])
        migrations.AlterField(
            model_name='userresourceprovenance',
            name='grantor',
            field=models.ForeignKey(related_name='x2urq', editable=False, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, help_text='grantor of privilege', null=True),
        ),
        # END(ID=299)
    ]
