# -*- coding: utf-8 -*-

from django.db import migrations, models


def remove_extra_privileges(apps, schema_editor):
    """ 
    Remove extra records from privileges tables
        
    This change removes extra records that were generated by early versions of the user interface. 
    These records are redundant, in the sense that the highest privilege always wins. 
    The method for eliminating them is to retain the highest privilege that was instituted latest. 
    This is consistent with what would have resulted if the access control system were running 
    under the new semantics. 

    For example, if user 'foo' had the following privilege records over resource 'bar': 
    
    
        VIEW   1/1/2016  michael 
        CHANGE 1/2/2016  robert
        VIEW   2/1/2016  alva

    Then 
    
    * The new effective privilege record will be: 
        
        CHANGE 1/2/2016  robert

    * The first record will be considered to be overridden by the second. 
    * The third record cannot be honored because it would result in a perceivable downgrade of 
      privilege. So it is ignored. 

    There are commented out print statements that will track the progress of this request if enabled. 
    These do not show up in my (broken) development system. 

    """
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")
    BaseResource = apps.get_model("hs_core", "BaseResource")
    UserResourcePrivilege = apps.get_model("hs_access_control", "UserResourcePrivilege")
    UserGroupPrivilege = apps.get_model("hs_access_control", "UserGroupPrivilege")
    GroupResourcePrivilege = apps.get_model("hs_access_control", "GroupResourcePrivilege")

    # brute force removal of offending records.
    # START(ID=247,NAME=MigrationGetAllUsersForForceRemoval,TYPE=SELECT,OBJECTS=[USER])
    for u in User.objects.all():
    # END(ID=247)
        # START(ID=248,NAME=MigrationGetAllBaseResourceForForceRemoval,TYPE=SELECT,OBJECTS=[BaseResource])
        for r in BaseResource.objects.all():
        # END(ID=248)
            # START(ID=249,NAME=MigrationFilterUserResourcePrivilegeForForceRemoval,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
            records = UserResourcePrivilege.objects.filter(user=u, resource=r)
            # END(ID=249)
            # START(ID=250,NAME=MigrationFilterUserResourcePrivilegeForForceRemovalCount,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
            if records.count() > 1:  # do nothing if there are no duplicates
            # END(ID=250)
                # print(str.format("User '{}' (id={}) has {} privilege records" +
                #                  " over resource '{}'",
                #                  str(r.user.username).encode('ascii'), str(r.user.id),
                #                  str(records.count()),
                #                  str(r.short_id).encode('ascii')))

                # for x in records:
                #     print(str.format("   {}", str(x)))

                # determine the lowest privilege number
                # START(ID=251,NAME=MigrationFindMinOfUserResourcePrivilegeForForceRemoval,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
                min = records.aggregate(models.Min('privilege'))
                # END(ID=251)
                min_privilege = min['privilege__min']
                # print (str.format("   minimum privilege is {}", str(min_privilege)))

                # of records with this number, select the record with maximum timestamp.
                # This determines the (last) grantor
                # START(ID=252,NAME=MigrationFindMaxOfUserResourcePrivilegeForForceRemovalWithMinPriviledge,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
                max = records.filter(privilege=min_privilege).aggregate(models.Max('start'))
                # END(ID=252)
                max_start = max['start__max']
                # print (str.format("   maximum start is {}", str(max_start)))
                # START(ID=253,NAME=MigrationUserResourcePrivilegeToKeepWithMinPriviledge,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
                to_keep = records.filter(privilege=min_privilege, start=max_start)
                # END(ID=253)
                # START(ID=254,NAME=MigrationUserResourcePrivilegeToKeepWithMinPriviledgeIsOne,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
                if to_keep.count() == 1:
                # END(ID=254)
                    # print("   one UNIQUE start record: {}", str(to_keep[0]))
                    # START(ID=255,NAME=MigrationUserResourcePrivilegeToExludeWithMinPriviledge,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
                    to_delete = records.exclude(pk__in=to_keep)
                    # END(ID=255)
                    # START(ID=256,NAME=MigrationUserResourcePrivilegeToDelete,TYPE=DELETE,OBJECTS=[UserResourcePrivilege])
                    to_delete.delete()
                    # END(ID=256)
                # START(ID=257,NAME=MigrationUserResourcePrivilegeToKeepWithMinPriviledgeGreaterThanOne,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
                elif to_keep.count() > 1:  # unlikely
                # END(ID=257)
                    kept = records[0]  # choose first one arbitrarily
                    # print("   choosing arbitrary record: {}", str(kept))
                    # START(ID=258,NAME=MigrationUserResourcePrivilegeToExludeWithMinPriviledgeGreateThanOne,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
                    to_delete = records.exclude(pk=kept)
                    # END(ID=258)
                    # START(ID=259,NAME=MigrationUserResourcePrivilegeToDeleteGreaterThanOne,TYPE=DELETE,OBJECTS=[UserResourcePrivilege])
                    to_delete.delete()
                    # END(ID=259)

    # START(ID=260,NAME=MigrationGetAllUsersUserGroupPrivilegeForRemoval,TYPE=SELECT,OBJECTS=[USER])
    for u in User.objects.all():
    # END(ID=260)
        # START(ID=261,NAME=MigrationGetAllGroupsUserGroupPrivilegeForRemoval,TYPE=SELECT,OBJECTS=[Group])
        for g in Group.objects.all():
        # END(ID=261)
            # START(ID=262,NAME=MigrationFilterUserAndGroupForUserGroupPrivilegeForRemoval,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
            records = UserGroupPrivilege.objects.filter(user=u, group=g)
            # END(ID=262)
            # START(ID=263,NAME=MigrationCountUserGroupPrivilegeForRemoval,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
            if records.count() > 1:  # do nothing if there are no duplicates
            # END(ID=263)
                # print(str.format("User '{}' (id={}) has {} privilege records" +
                #                  " over group '{}' ({})",
                #                  str(r.user.username), str(r.user.id),
                #                  str(records.count()),
                #                  str(r.group.name), str(r.group.id)))

                # determine the lowest privilege number
                # START(ID=263,NAME=MigrationMinOfUserGroupPrivilegeForRemoval,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
                min = records.aggregate(models.Min('privilege'))
                # END(ID=263)
                min_privilege = min['privilege__min']
                # print (str.format("   minimum privilege is {}", str(min_privilege)))

                # of records with this number, select the record with maximum timestamp.
                # This determines the (last) grantor
                # START(ID=264,NAME=MigrationPrivilegeMinAgregStartOfUserGroupPrivilegeForRemoval,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
                max = records.filter(privilege=min_privilege).aggregate(models.Max('start'))
                # END(ID=264)
                max_start = max['start__max']
                # print (str.format("   maximum start is {}", str(max_start)))
                # START(ID=265,NAME=MigrationPrivilegeMinToKeepStartOfUserGroupPrivilegeForRemoval,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
                to_keep = records.filter(privilege=min_privilege, start=max_start)
                # END(ID=265)
                # START(ID=266,NAME=MigrationPrivilegeMinToKeepCountOfUserGroupPrivilegeForRemoval,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
                if to_keep.count() == 1:
                # END(ID=266)
                    # print("   one UNIQUE start record: {}", str(to_keep[0]))
                    # START(ID=267,NAME=MigrationPrivilegeMinToKeepExcludeOfUserGroupPrivilegeForRemoval,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
                    to_delete = records.exclude(pk__in=to_keep)
                    # END(ID=267)
                    # START(ID=268,NAME=MigrationPrivilegeOfUserGroupPrivilegeDeleteCountIsOne,TYPE=DELETE,OBJECTS=[UserGroupPrivilege])
                    to_delete.delete()
                    # END(ID=268)
                # START(ID=269,NAME=MigrationPrivilegeMinToKeepCountOverOneOfUserGroupPrivilegeForRemoval,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
                elif to_keep.count() > 1:  # unlikely
                # END(ID=269)
                    kept = records[0]  # choose first one arbitrarily
                    # print("   choosing arbitrary record: {}", str(kept))
                    # START(ID=270,NAME=MigrationPrivilegeMinExcludeToKeepOverOneOfUserGroupPrivilegeForRemoval,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
                    to_delete = records.exclude(pk=kept)
                    # END(ID=270)
                    # START(ID=271,NAME=MigrationPrivilegeOfUserGroupPrivilegeDeleteCountIsOne,TYPE=DELETE,OBJECTS=[UserGroupPrivilege])
                    to_delete.delete()
                    # END(ID=271)
    # START(ID=272,NAME=MigrationGetAllGroupsGroupResourcePrivilegeForRemoval,TYPE=SELECT,OBJECTS=[Group])
    for g in Group.objects.all():
    # END(ID=272)
        # START(ID=273,NAME=MigrationGetAllBaseResourceGroupResourcePrivilegeForRemoval,TYPE=SELECT,OBJECTS=[BaseResource])
        for r in BaseResource.objects.all():
        # END(ID=273)
            # START(ID=274,NAME=MigrationGetAllGroupResourcePrivilegeFilterGroupResourceForRemoval,TYPE=SELECT,OBJECTS=[GroupResourcePrivilege])
            records = GroupResourcePrivilege.objects.filter(group=g, resource=r)
            # END(ID=274)
            # START(ID=275,NAME=MigrationGetAllGroupResourcePrivilegeFilterGroupResourceCountForRemoval,TYPE=SELECT,OBJECTS=[GroupResourcePrivilege])
            if records.count() > 1:  # do nothing if there are no duplicates
            # END(ID=275)
                # print(str.format("Group '{}' (id={}) has {} privilege records" +
                #                  " over resource '{}'",
                #                  str(r.group.name).encode('ascii'), str(r.group.id),
                #                  str(records.count()),
                #                  str(r.short_id)).encode('ascii'))

                # determine the lowest privilege number
                # START(ID=276,NAME=MigrationGetAllGroupResourcePrivilegeFilterGroupResourceCountAgregatePrivForRemoval,TYPE=SELECT,OBJECTS=[GroupResourcePrivilege])
                min = records.aggregate(models.Min('privilege'))
                # END(ID=276)
                min_privilege = min['privilege__min']
                # print (str.format("   minimum privilege is {}", str(min_privilege)))

                # of records with this number, select the record with maximum timestamp.
                # This determines the (last) grantor
                # START(ID=277,NAME=MigrationGetAllGroupResourcePrivilegeAgregateStartMaxForRemoval,TYPE=SELECT,OBJECTS=[GroupResourcePrivilege])
                max = records.filter(privilege=min_privilege).aggregate(models.Max('start'))
                # END(ID=277)
                max_start = max['start__max']
                # print (str.format("   maximum start is {}", str(max_start)))
                # START(ID=278,NAME=MigrationGetAllGroupResourcePrivilegeToKeepCountGreaterThanOneAgregateStartMaxForRemoval,TYPE=SELECT,OBJECTS=[GroupResourcePrivilege])
                to_keep = records.filter(privilege=min_privilege, start=max_start)
                # END(ID=278)
                # START(ID=279,NAME=MigrationGetAllGroupResourcePrivilegeToKeepCountIsOneAgregateStartMaxForRemoval,TYPE=SELECT,OBJECTS=[GroupResourcePrivilege])
                if to_keep.count() == 1:
                # END(ID=279)
                    # print("   one UNIQUE start record: {}", str(to_keep[0]))
                    # START(ID=280,NAME=MigrationGetAllGroupResourcePrivilegeToKeepCountIsOneExcludeForRemoval,TYPE=SELECT,OBJECTS=[GroupResourcePrivilege])
                    to_delete = records.exclude(pk__in=to_keep)
                    # END(ID=280)
                    # START(ID=281,NAME=MigrationGetAllGroupResourcePrivilegeToKeepCountIsOneDelete,TYPE=DELETE,OBJECTS=[GroupResourcePrivilege])
                    to_delete.delete()
                    # END(ID=281)
                # START(ID=282,NAME=MigrationGetAllGroupResourcePrivilegeToKeepCountGreaterThanOneUnlikely,TYPE=SELECT,OBJECTS=[GroupResourcePrivilege])
                elif to_keep.count() > 1:  # unlikely
                # END(ID=282)
                    kept = records[0]  # choose first one arbitrarily
                    # print("   choosing arbitrary record: {}", str(kept))
                     # START(ID=283,NAME=MigrationGetAllGroupResourcePrivilegeToKeepCountGreaterThanOneUnlikelyExclude,TYPE=SELECT,OBJECTS=[GroupResourcePrivilege])
                    to_delete = records.exclude(pk=kept)
                    # END(ID=283)
                    # START(ID=284,NAME=MigrationGetAllGroupResourcePrivilegeToKeepCountGreaterThanOneUnlikelyDelete,TYPE=DELETE,OBJECTS=[GroupResourcePrivilege])
                    to_delete.delete()
                    # END(ID=284)


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0014_auto_20160424_1628'),
    ]

    operations = [
        migrations.RunPython(remove_extra_privileges),
    ]
