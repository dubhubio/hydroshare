# -*- coding: utf-8 -*-


from django.db import models, migrations

def move_access_data(apps, schema_editor): 

    UserGroupPrivilege = apps.get_model('hs_access_control', 'UserGroupPrivilege') 
    for ugp in UserGroupPrivilege.objects.all(): 
        ugp.usernew = ugp.user.user 
        ugp.groupnew = ugp.group.group
        ugp.grantornew = ugp.grantor.user
        # START(ID=188,NAME=MigrationUpdateUserGroupPrivilegeObjects,TYPE=UPDATE,OBJECTS=[UserGroupPrivilege])
        ugp.save()
        # END(ID=188)
        
    UserResourcePrivilege = apps.get_model('hs_access_control', 'UserResourcePrivilege') 
    for urp in UserResourcePrivilege.objects.all(): 
        urp.usernew = urp.user.user 
        urp.resourcenew = urp.resource.resource
        urp.grantornew = urp.grantor.user
        # START(ID=189,NAME=MigrationUpdateUserResourcePrivilegeObjects,TYPE=UPDATE,OBJECTS=[UserResourcePrivilege])
        urp.save()
        # END(ID=189)

    GroupResourcePrivilege = apps.get_model('hs_access_control', 'GroupResourcePrivilege') 
    for grp in GroupResourcePrivilege.objects.all(): 
        grp.usernew = grp.user.user 
        grp.groupnew = grp.group.group
        grp.grantornew = grp.grantor.user
        # START(ID=190,NAME=MigrationUpdateGroupResourcePrivilegeObjects,TYPE=UPDATE,OBJECTS=[GroupResourcePrivilege])
        grp.save()
        # END(ID=190)

class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0006_auto_add_new_fields'),
    ]

    operations = [
        migrations.RunPython(move_access_data)
    ]
