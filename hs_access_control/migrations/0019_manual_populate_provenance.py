# -*- coding: utf-8 -*-

from django.db import migrations


def populate_provenance(apps, schema_editor):
    """
    Remove extra records from privileges tables

    This change adds a matching provenance record for each record in the corresponding privilege.
    This enables undo for existing privileges.

    """
    UserResourcePrivilege = apps.get_model("hs_access_control", "UserResourcePrivilege")
    UserGroupPrivilege = apps.get_model("hs_access_control", "UserGroupPrivilege")
    GroupResourcePrivilege = apps.get_model("hs_access_control", "GroupResourcePrivilege")
    UserResourceProvenance = apps.get_model("hs_access_control", "UserResourceProvenance")
    UserGroupProvenance = apps.get_model("hs_access_control", "UserGroupProvenance")
    GroupResourceProvenance = apps.get_model("hs_access_control", "GroupResourceProvenance")

    # brute force addition of provenance records
    # START(ID=300,NAME=MigrationLoopGroupResourcePrivilegeForBruteForceAdd,TYPE=SELECT,OBJECTS=[GroupResourcePrivilege])
    for r in GroupResourcePrivilege.objects.all():
    # END(ID=300)
        # START(ID=301,NAME=MigrationGroupResourceProvenanceBruteForceAdd,TYPE=INSERT,OBJECTS=[GroupResourceProvenance])
        GroupResourceProvenance.objects.create(group=r.group,
                                               resource=r.resource,
                                               start=r.start,
                                               privilege=r.privilege,
                                               grantor=r.grantor,
                                               undone=False)
        # END(ID=301)
    # START(ID=302,NAME=MigrationLoopUserResourcePrivilegeForBruteForceAdd,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
    for r in UserResourcePrivilege.objects.all():
    # END(ID=302)
        # START(ID=303,NAME=MigrationUserResourceProvenanceBruteForceAdd,TYPE=INSERT,OBJECTS=[UserResourceProvenance])
        UserResourceProvenance.objects.create(user=r.user,
                                              resource=r.resource,
                                              start=r.start,
                                              privilege=r.privilege,
                                              grantor=r.grantor,
                                              undone=False)
        # END(ID=303)
    # START(ID=304,NAME=MigrationLoopUserGroupPrivilegeForBruteForceAdd,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
    for r in UserGroupPrivilege.objects.all():
    # END(ID=304)
        # START(ID=305,NAME=MigrationUserGroupProvenanceBruteForceAdd,TYPE=INSERT,OBJECTS=[UserGroupProvenance])
        UserGroupProvenance.objects.create(user=r.user,
                                           group=r.group,
                                           start=r.start,
                                           privilege=r.privilege,
                                           grantor=r.grantor,
                                           undone=False)
        # END(ID=305)


class Migration(migrations.Migration):

    dependencies = [
        ('hs_access_control', '0018_auto_tune_provenance'),
    ]

    operations = [
        migrations.RunPython(populate_provenance),
    ]
