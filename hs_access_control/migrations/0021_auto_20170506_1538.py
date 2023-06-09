# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0020_merge'),
    ]

    operations = [
        # START(ID=306,NAME=MigrationAlterFieldAutoApproveGroupAccess0021,TYPE=ALTER,OBJECTS=[GroupAccess])
        migrations.AlterField(
            model_name='groupaccess',
            name='auto_approve',
            field=models.BooleanField(default=False, help_text='whether group membership can be auto approved', editable=False),
        ),
        # END(ID=306)
    ]
