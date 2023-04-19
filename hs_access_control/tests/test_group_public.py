from django.test import TestCase
from django.contrib.auth.models import Group, User

from hs_access_control.models import PrivilegeCodes

from hs_core import hydroshare
from hs_core.models import BaseResource
from hs_core.testing import MockIRODSTestCaseMixin

from hs_access_control.tests.utilities import global_reset, is_equal_to_as_set


class T09GroupPublic(MockIRODSTestCaseMixin, TestCase):

    def setUp(self):
        super(T09GroupPublic, self).setUp()
        global_reset()
        # START(ID=664,NAME=TestGroupPublicSetUpGetOrCreateGroup,TYPE=MERGE,OBJECTS=[Group])
        self.group, _ = Group.objects.get_or_create(name='Hydroshare Author')
        # END(ID=664)
        self.admin = hydroshare.create_account(
            'admin@gmail.com',
            username='admin',
            first_name='administrator',
            last_name='couch',
            superuser=True,
            groups=[]
        )

        self.dog = hydroshare.create_account(
            'dog@gmail.com',
            username='dog',
            first_name='a little arfer',
            last_name='last_name_dog',
            superuser=False,
            groups=[]
        )

        self.squirrels = hydroshare.create_resource(
            resource_type='CompositeResource',
            owner=self.dog,
            title='all about chasing squirrels',
            metadata=[],
        )

        self.holes = hydroshare.create_resource(
            resource_type='CompositeResource',
            owner=self.dog,
            title='all about storing bones in holes',
            metadata=[],
        )

        # dog owns canines group
        self.canines = self.dog.uaccess.create_group(
            title='canines', description="We are the canines")

    def tearDown(self):
        super(T09GroupPublic, self).tearDown()
        # START(ID=665,NAME=TestGroupPublicTearDownAllUsers,TYPE=DELETE,OBJECTS=[User])
        User.objects.all().delete()
        # END(ID=665)
        # START(ID=666,NAME=TestGroupPublicTearDownAllGroups,TYPE=DELETE,OBJECTS=[Group])
        Group.objects.all().delete()
        # END(ID=666)
        # START(ID=667,NAME=TestGroupPublicTearDownBaseResourceSquirels,TYPE=DELETE,OBJECTS=[BaseResource])
        self.squirrels.delete()
        # END(ID=667)
        # START(ID=668,NAME=TestGroupPublicTearDownBaseResourceHoles,TYPE=DELETE,OBJECTS=[BaseResource])
        self.holes.delete()
        # END(ID=668)
        # START(ID=669,NAME=TestGroupPublicTearDownBaseResource,TYPE=DELETE,OBJECTS=[BaseResource])
        BaseResource.objects.all().delete()
        # END(ID=669)

    def test_public_resources(self):
        """ public resources contain those resources that are public and discoverable """

        res = self.canines.gaccess.public_resources
        self.assertTrue(is_equal_to_as_set(res, []))
        self.dog.uaccess.share_resource_with_group(self.squirrels, self.canines,
                                                   PrivilegeCodes.VIEW)
        self.dog.uaccess.share_resource_with_group(self.holes, self.canines,
                                                   PrivilegeCodes.VIEW)
        res = self.canines.gaccess.public_resources
        self.assertTrue(is_equal_to_as_set(res, []))
        self.holes.raccess.public = True
        self.holes.raccess.discoverable = True
        # START(ID=670,NAME=TestGroupPublicTestPublicResourceHolesResourceAccess,TYPE=UPDATE,OBJECTS=[ResourceAccess])
        self.holes.raccess.save()
        # END(ID=670)
        res = self.canines.gaccess.public_resources
        self.assertTrue(is_equal_to_as_set(res, [self.holes]))
        for r in res:
            self.assertEqual(r.public, r.raccess.public)
            self.assertEqual(r.discoverable, r.raccess.discoverable)
            self.assertEqual(r.published, r.raccess.published)
            self.assertEqual(r.group_name, self.canines.name)
            self.assertEqual(r.group_id, self.canines.id)
        self.squirrels.raccess.discoverable = True
        # START(ID=671,NAME=TestGroupPublicTestPublicResourceHolesResourceAccess,TYPE=UPDATE,OBJECTS=[ResourceAccess])
        self.squirrels.raccess.save()
        # END(ID=671)
        res = self.canines.gaccess.public_resources
        self.assertTrue(is_equal_to_as_set(res, [self.holes, self.squirrels]))
        for r in res:
            self.assertEqual(r.public, r.raccess.public)
            self.assertEqual(r.discoverable, r.raccess.discoverable)
            self.assertEqual(r.published, r.raccess.published)
            self.assertEqual(r.group_name, self.canines.name)
            self.assertEqual(r.group_id, self.canines.id)
