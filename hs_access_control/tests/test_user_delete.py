from django.test import TestCase
from django.contrib.auth.models import Group, User

from hs_access_control.models import UserAccess, GroupAccess, ResourceAccess, \
    UserGroupPrivilege, UserResourcePrivilege, GroupMembershipRequest

from hs_core import hydroshare
from hs_core.models import BaseResource
from hs_core.testing import MockIRODSTestCaseMixin
from hs_access_control.tests.utilities import global_reset


class T12UserDelete(MockIRODSTestCaseMixin, TestCase):

    def setUp(self):
        super(T12UserDelete, self).setUp()

        global_reset()
        # START(ID=728,NAME=TestUserDeleteSetUpGetOrCreateGroup,TYPE=MERGE,OBJECTS=[Group])
        self.group, _ = Group.objects.get_or_create(name='Hydroshare Author')
        # END(ID=728)
        self.admin = hydroshare.create_account(
            'admin@gmail.com',
            username='admin',
            first_name='administrator',
            last_name='couch',
            superuser=True,
            groups=[]
        )

        self.cat = hydroshare.create_account(
            'cat@gmail.com',
            username='cat',
            first_name='not a dog',
            last_name='last_name_cat',
            superuser=False,
            groups=[]
        )

        self.scratching = hydroshare.create_resource(
            resource_type='CompositeResource',
            owner=self.cat,
            title='all about sofas as scratching posts',
            metadata=[]
        )

        self.felines = self.cat.uaccess.create_group(
            title='felines',
            description="We are the felines"
        )

        self.dog = hydroshare.create_account(
            'dog@gmail.com',
            username='dog',
            first_name='a little arfer',
            last_name='last_name_dog',
            superuser=False,
            groups=[]
        )

        self.arfers = self.dog.uaccess.create_group(
            title='arfers',
            description='animals that bark'
        )

        self.cat.uaccess.create_group_membership_request(self.arfers)

    def tearDown(self):
        super(T12UserDelete, self).tearDown()
        # START(ID=729,NAME=TestUserDeleteTearDownUser,TYPE=DELETE,OBJECTS=[User])
        User.objects.all().delete()
        # END(ID=729)
        # START(ID=730,NAME=TestUserDeleteTearDownGroup,TYPE=DELETE,OBJECTS=[Group])
        Group.objects.all().delete()
        # END(ID=730)
        # START(ID=731,NAME=TestUserDeleteTearDownBaseResourceScratching,TYPE=DELETE,OBJECTS=[BaseResource])
        self.scratching.delete()
        # END(ID=731)
        # START(ID=732,NAME=TestUserDeleteTearDownBaseResource,TYPE=DELETE,OBJECTS=[BaseResource])
        BaseResource.objects.all().delete()
        # END(ID=732)

    def test_00_cascade(self):
        """
        Deleting a user cascade-deletes its access control
        # This tests that deleting a user cleans up its access control.
        # Note that deleting the sole owner of a resource or group
        # leaves it orphaned. This is not prevented.
        """
        cat = self.cat

        # get the id's of all objects that should be deleted.
        uid = cat.uaccess.id
        orid = self.scratching.id
        arid = self.scratching.raccess.id
        ogid = self.felines.id
        agid = self.felines.gaccess.id
        # START(ID=733,NAME=TestUserDeleteTest00CascadeGetUserGroupPrivilegeUserCatId,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
        gpid = UserGroupPrivilege.objects.get(user=cat).id
        # END(ID=733)
        # START(ID=734,NAME=TestUserDeleteTest00CascadeGetUserResourcePrivilegeUserCatId,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
        rpid = UserResourcePrivilege.objects.get(user=cat).id
        # END(ID=734)
        # START(ID=735,NAME=TestUserDeleteTest00CascadeGetGroupMembershipRequestUserCatId,TYPE=SELECT,OBJECTS=[GroupMembershipRequest])
        mpid = GroupMembershipRequest.objects.get(request_from=cat).id
        # END(ID=735)

        # all objects exist before the delete
        # START(ID=736,NAME=TestUserDeleteTest00CascadeGetUserAccessCount,TYPE=SELECT,OBJECTS=[UserAccess])
        self.assertEqual(UserAccess.objects.filter(id=uid).count(), 1)
        # END(ID=736)
        # START(ID=737,NAME=TestUserDeleteTest00CascadeGetUserGroupPrivilegeCount,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
        self.assertEqual(UserGroupPrivilege.objects.filter(id=gpid).count(), 1)
        # END(ID=737)
        self.assertEqual(
            # START(ID=738,NAME=TestUserDeleteTest00CascadeGetUserResourcePrivilegeCount,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
            UserResourcePrivilege.objects.filter(
                id=rpid).count()
            # END(ID=738)
            , 1)
        self.assertEqual(
            # START(ID=739,NAME=TestUserDeleteTest00CascadeGetGroupMembershipRequestCount,TYPE=SELECT,OBJECTS=[GroupMembershipRequest])
            GroupMembershipRequest.objects.filter(
                id=mpid).count()
            # END(ID=739)    
                , 1)
        # START(ID=740,NAME=TestUserDeleteTest00CascadeGetResourceAccessCount,TYPE=SELECT,OBJECTS=[ResourceAccess])
        self.assertEqual(ResourceAccess.objects.filter(id=arid).count(), 1)
        # END(ID=740)
        # START(ID=741,NAME=TestUserDeleteTest00CascadeGetGroupAccessCount,TYPE=SELECT,OBJECTS=[GroupAccess])
        self.assertEqual(GroupAccess.objects.filter(id=agid).count(), 1)
        # END(ID=741)
        # START(ID=742,NAME=TestUserDeleteTest00CascadeGetBaseResourceCount,TYPE=SELECT,OBJECTS=[BaseResource])
        self.assertEqual(BaseResource.objects.filter(id=orid).count(), 1)
        # END(ID=742)
        # START(ID=743,NAME=TestUserDeleteTest00CascadeGetGroupCount,TYPE=SELECT,OBJECTS=[Group])
        self.assertEqual(Group.objects.filter(id=ogid).count(), 1)
        # END(ID=743)
        # START(ID=750,NAME=TestUserDeleteTest00DeleteCatUser,TYPE=DELETE,OBJECTS=[User])
        cat.delete()
        # END(ID=750)

        # objects tied to the user are deleted, other objects continue to exist
        # START(ID=744,NAME=TestUserDeleteTest00CascadeGetUserAccessCountAfterDelete,TYPE=SELECT,OBJECTS=[UserAccess])
        self.assertEqual(UserAccess.objects.filter(id=uid).count(), 0)
        # END(ID=744)
        # START(ID=745,NAME=TestUserDeleteTest00CascadeGetUserGroupPrivilegeCountAfterDelete,TYPE=SELECT,OBJECTS=[UserGroupPrivilege])
        self.assertEqual(UserGroupPrivilege.objects.filter(id=gpid).count(), 0)
        # END(ID=745)
        self.assertEqual(
            # START(ID=746,NAME=TestUserDeleteTest00CascadeGetUserResourcePrivilegeCountAfterDelete,TYPE=SELECT,OBJECTS=[UserResourcePrivilege])
            UserResourcePrivilege.objects.filter(
                id=rpid).count()
            # END(ID=746)    
                , 0)
        # START(ID=747,NAME=TestUserDeleteTest00CascadeGetGroupMembershipRequestCountAfterDelete,TYPE=SELECT,OBJECTS=[GroupMembershipRequest])
        self.assertEqual(
            GroupMembershipRequest.objects.filter(
                id=mpid).count(), 0)
        # END(ID=747) 
        # deleting a user should not remove the groups that user owns
        # START(ID=748,NAME=TestUserDeleteTest00CascadeGetGroupMembershipRequestCountCheckGroupAccessNotDeleted,TYPE=SELECT,OBJECTS=[GroupAccess])
        self.assertEqual(GroupAccess.objects.filter(id=agid).count(), 1)
        # END(ID=748)
        # START(ID=749,NAME=TestUserDeleteTest00CascadeGetGroupMembershipRequestCountCheckGroupNotDeleted,TYPE=SELECT,OBJECTS=[Group])
        self.assertEqual(Group.objects.filter(id=ogid).count(), 1)
        # END(ID=749)

        # the following tests will fail, because the resource field
        # "creator" is a foreign key to User with on_delete=models.CASCADE
        # and null=False. Thus removing the creator of a resource will
        # remove the resource record (and orphan many files in the process).

        # print('resource access count is ', ResourceAccess.objects.filter(id=arid).count())
        # print('resource count is ', BaseResource.objects.filter(id=orid).count())
        # self.assertEqual(ResourceAccess.objects.filter(id=arid).count(), 1)
        # self.assertEqual(BaseResource.objects.filter(id=orid).count(), 1)
