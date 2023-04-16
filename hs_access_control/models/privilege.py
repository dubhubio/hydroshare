from django.contrib.auth.models import User, Group
from django.db import models
from django.db import transaction

from hs_core.models import BaseResource
from hs_access_control.models.community import Community

#############################################
# Classes involving privilege
#
# These manipulate privilege but do not include business logic, which is instead
# coded into user.py, resource.py, group.py
#############################################


class PrivilegeCodes(object):
    """
    Privilege codes describe what capabilities a user has for a thing
    Privilege is a numeric code 1-4:

        * 1 or PrivilegeCodes.OWNER:
            the user owns the object.

        * 2 or PrivilegeCodes.CHANGE:
            the user can change the content of the object but not its state.

        * 3 or PrivilegeCodes.VIEW:
            the user can view but not change the object.

        * 4 or PrivilegeCodes.NONE:
            the user has no privilege over the object.
    """
    OWNER = 1
    CHANGE = 2
    VIEW = 3
    NONE = 4
    CHOICES = (
        (OWNER, 'Owner'),
        (CHANGE, 'Change'),
        (VIEW, 'View')
        # (NONE, 'None') : disallow "no privilege" lines
    )
    # Names of privileges for printing
    NAMES = ('Unspecified', 'Owner', 'Change', 'View', 'None')

    @classmethod
    def from_string(self, privilege):
        """ Converts a string representation to a PrivilegeCode """
        if privilege.lower() == 'view':
            return PrivilegeCodes.VIEW
        if privilege.lower() == 'edit':
            return PrivilegeCodes.CHANGE
        if privilege.lower() == 'owner':
            return PrivilegeCodes.OWNER
        if privilege.lower() == 'none':
            return PrivilegeCodes.NONE
        return None


class PrivilegeBase(models.Model):
    """
    Shared methods for Privilege handling

    These polymorphic routines act on any type of keys, so that
    they are independent of the types of the base class members.
    They implement the major interactions with privileges, including
    share, unshare, undo_share, and ensure that provenance and privilege
    are always in sync with one another.
    """

    class Meta:
        abstract = True

    @classmethod
    def get_privilege(cls, **kwargs):
        """
        Get an effective privilege for a pair of keys

        This works for any pair of attributes that together, form a key.
        Examples include:

            * UserResourcePrivilege.get_privilege(user={X}, resource={Y})
            * GroupResourcePrivilege.get_privilege(group={X}, resource={Y})
            * UserGroupPrivilege.get_privilege(user={X}, group={Y})
            * UserCommunityPrivilege.get_privilege(user={X}, community={Y})
            * GroupCommunityPrivilege.get_privilege(group={X}, community={Y})

        **This is a system routine** and not recommended for use in application code.
        """
        try:
            # START(ID=419,NAME=PrivilegeBaseGetPrivilege,TYPE=SELECT,OBJECTS=[PrivilegeBase])
            return cls.objects.get(**kwargs).privilege
            # END(ID=419)
        except cls.DoesNotExist:
            return PrivilegeCodes.NONE

    @classmethod
    def update(cls, **kwargs):
        """
        Update an effective privilege record without maintaining provenance.

        This works for any pair of attributes that together, form a key, along with shared
        parameters `grantor` and `privilege`.  Examples include:

            * UserResourcePrivilege.update(user={X}, resource={Y}, privilege={Z}, grantor={W})
            * GroupResourcePrivilege.update(group={X}, resource={Y}, privilege={Z}, grantor={W})
            * UserGroupPrivilege.update(user={X}, group={Y}, privilege={Z}, grantor={W})
            * UserCommunityPrivilege.update(user={X}, community={Y}, privilege={Z}, grantor={W})
            * GroupCommunityPrivilege.update(group={X}, community={Y}, privilege={Z}, grantor={W})

        **This is a system routine** and not recommended for use in application code.
        There are no access control rules applied; this routine is unconditional.
        Only use this routine if you wish to completely bypass access control.
        Note also that using this routine directly breaks provenance and disables undo.
        """
        grantor = kwargs['grantor']
        privilege = kwargs.get('privilege', None)
        if privilege is not None and privilege < PrivilegeCodes.NONE:
            if 'privilege' in kwargs:
                del kwargs['privilege']
            del kwargs['grantor']
            with transaction.atomic():
                # START(ID=420,NAME=PrivilegeBaseGetOrCreate,TYPE=MERGE,OBJECTS=[PrivilegeBase])
                record, create = cls.objects.get_or_create(defaults={'privilege': privilege,
                                                                     'grantor': grantor},
                                                           **kwargs)
                # END(ID=420)
                if not create:
                    record.privilege = privilege
                    record.grantor = grantor
                    # START(ID=422,NAME=PrivilegeBaseUpdate,TYPE=UPDATE,OBJECTS=[PrivilegeBase])
                    record.save()
                    # END(ID=422)
        else:
            if 'privilege' in kwargs:
                del kwargs['privilege']
            del kwargs['grantor']
            # START(ID=421,NAME=PrivilegeBaseDelete,TYPE=DELETE,OBJECTS=[PrivilegeBase])
            cls.objects.filter(**kwargs) \
               .delete()
            # END(ID=421)

    @classmethod
    def share(cls, **kwargs):
        """
        Share an item with a user or group without maintaining provenance.

        This works for any pair of attributes that together, form a key, along with shared
        parameters `grantor` and `privilege`.  Examples include:

            * UserResourcePrivilege.share(user={X}, resource={Y}, privilege={Z}, grantor={W})
            * GroupResourcePrivilege.share(group={X}, resource={Y}, privilege={Z}, grantor={W})
            * UserGroupPrivilege.share(user={X}, group={Y}, privilege={Z}, grantor={W})
            * UserCommunityPrivilege.share(user={X}, community={Y}, privilege={Z}, grantor={W})
            * GroupCommunityPrivilege.share(group={X}, community={Y}, privilege={Z}, grantor={W})

        A share operation is just an update operation.

        **This is a system routine** and not recommended for use in application code.
        There are no access control rules applied; this routine is unconditional.
        Only use this routine if you wish to completely bypass access control.
        Note also that using this routine directly breaks provenance and disables undo.
        """
        # START(ID=439,NAME=PriveledgeShareUpdateClsPrivilegeBase,TYPE=UPDATE,OBJECTS=[PrivilegeBase])
        cls.update(cls, **kwargs)
        # END(ID=439)

    @classmethod
    def unshare(cls, **kwargs):
        """
        Unshare an item with a user or group without maintaining provenance.

        This works for any pair of attributes that together, form a key, along with shared
        parameter `grantor`.  Examples include:

            * UserResourcePrivilege.share(user={X}, resource={Y}, grantor={W})
            * GroupResourcePrivilege.share(group={X}, resource={Y}, grantor={W})
            * UserGroupPrivilege.share(user={X}, group={Y}, grantor={W})
            * UserCommunityPrivilege.share(user={X}, community={Y}, grantor={W})
            * GroupCommunityPrivilege.share(group={X}, community={Y}, grantor={W})

        An unshare operation is just an update operation with privilege=PrivilegeCodes.NONE.

        **This is a system routine** and not recommended for use in application code.
        There are no access control rules applied; this routine is unconditional.
        Only use this routine if you wish to completely bypass access control.
        Note also that using this routine directly breaks provenance and disables undo.

        An unshare operation is just an update with privilege NONE.
        """
        # START(ID=440,NAME=PriveledgeUnShareUpdateClsPrivilegeBase,TYPE=UPDATE,OBJECTS=[PrivilegeBase])
        cls.update(cls, privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=440)


class UserGroupPrivilege(PrivilegeBase):
    """ Privileges of a user over a group

    Having any privilege over a group is synonymous with membership.

    There is a reasonable meaning to PrivilegeCodes.NONE, which is to be
    a group member without the ability to discover the identities of other
    group members.  However, this is currently disallowed. It is used in the
    provenance models to record removing a privilege.
    """

    privilege = models.IntegerField(choices=PrivilegeCodes.CHOICES,
                                    editable=False,
                                    default=PrivilegeCodes.VIEW)
    start = models.DateTimeField(editable=False, auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=False,
                             editable=False,
                             related_name='u2ugp',
                             help_text='user to be granted privilege')

    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              null=False,
                              editable=False,
                              related_name='g2ugp',
                              help_text='group to which privilege applies')

    grantor = models.ForeignKey(User, on_delete=models.CASCADE,
                                null=False,
                                editable=False,
                                related_name='x2ugp',
                                help_text='grantor of privilege')

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        """ Return printed depiction for debugging """
        return str.format("<user '{}' (id={}) holds {} ({})"
                          + " over group '{}' (id={})"
                          + " via grantor '{}' (id={})>",
                          str(self.user.username), str(self.user.id),
                          PrivilegeCodes.NAMES[self.privilege],
                          str(self.privilege),
                          str(self.group.name), str(self.group.id),
                          str(self.grantor.username), str(self.grantor.id))

    @classmethod
    def share(cls, **kwargs):
        """
        Share a group with a user and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param group: target group.
        :param user: target user.
        :param privilege: privilege 1-4.
        :param grantor: user who requested privilege.

        Usage:
            UserGroupPrivilege.share(group={X}, user={Y}, privilege={Z}, grantor={W}
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserGroupProvenance
        if __debug__:
            assert 'group' in kwargs
            assert isinstance(kwargs['group'], Group)
            assert 'user' in kwargs
            assert isinstance(kwargs['user'], User)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert 'privilege' in kwargs
            assert \
                kwargs['privilege'] >= PrivilegeCodes.OWNER and \
                kwargs['privilege'] <= PrivilegeCodes.NONE
            assert len(kwargs) == 4
        # START(ID=441,NAME=PriveledgeShareUpdateClsUserGroupPrivilege,TYPE=UPDATE,OBJECTS=[UserGroupPrivilege])
        cls.update(**kwargs)
        # END(ID=441)
        # START(ID=442,NAME=PriveledgeShareUpdateClsUserGroupProvenance,TYPE=UPDATE,OBJECTS=[UserGroupProvenance])
        UserGroupProvenance.update(**kwargs)
        # END(ID=442)

    @classmethod
    def unshare(cls, **kwargs):
        """
        Unshare a group with a user and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param group: target group.
        :param user: target user.
        :param grantor: user who requested privilege.

        Usage:
            UserGroupPrivilege.unshare(group={X}, user={Y}, grantor={W})

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        Use UserAccess.unshare_group_with_user instead. That routine avoids single-owner
        deletion.
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserGroupProvenance
        if __debug__:
            assert 'group' in kwargs
            assert isinstance(kwargs['group'], Group)
            assert 'user' in kwargs
            assert isinstance(kwargs['user'], User)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 3
        # START(ID=443,NAME=PriveledgeUnhareUpdateClsUserGroupPrivilege,TYPE=UPDATE,OBJECTS=[UserGroupPrivilege])
        cls.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=443)
        # START(ID=444,NAME=PriveledgeUnhareUpdateClsUserGroupProvenance,TYPE=UPDATE,OBJECTS=[UserGroupProvenance])
        UserGroupProvenance.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=444)

    @classmethod
    def undo_share(cls, **kwargs):
        """
        Undo a share a group with a user and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param group: target group.
        :param user: target user.
        :param grantor: user who requested privilege.

        Usage:
            UserGroupPrivilege.undo_share(group={X}, user={Y}, grantor={W})

        In practice:

        The "undo" operation is independent of the privileges a user currently holds.
        Suppose -- for example -- that a user holds CHANGE, grants that to another user,
        and then loses CHANGE. The undo of the other user is still possible, even though the
        original user no longer has the privilege.

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        Use UserAccess.undo_share_group_with_user instead. That routine avoids single-owner
        deletion.
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserGroupProvenance
        if __debug__:
            assert 'group' in kwargs
            assert isinstance(kwargs['group'], Group)
            assert 'user' in kwargs
            assert isinstance(kwargs['user'], User)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 3
        grantor = kwargs['grantor']
        del kwargs['grantor']
        # undo in provenance model; add a record that reinstates previous privilege.
        UserGroupProvenance.undo_share(grantor=grantor, **kwargs)
        # read that record and post to privilege table.
        r = UserGroupProvenance.get_current_record(**kwargs)
        # START(ID=445,NAME=PriveledgeUndoUnhareUpdateClsUserGroupPrivilege,TYPE=UPDATE,OBJECTS=[UserGroupPrivilege])
        cls.update(user=r.user, group=r.group, privilege=r.privilege, grantor=r.grantor)
        # END(ID=445)

    @classmethod
    def get_undo_users(cls, **kwargs):
        """ Get a set of users for which a grantor can undo privilege

        :param group: group to check
        :param grantor: user that will undo privilege

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        Use UserAccess.__get_group_undo_users instead. That routine avoids single-owner deletion.
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserGroupProvenance
        if __debug__:
            assert 'group' in kwargs
            assert isinstance(kwargs['group'], Group)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 2
        return UserGroupProvenance.get_undo_users(**kwargs)


class UserResourcePrivilege(PrivilegeBase):
    """ Privileges of a user over a resource

    This model encodes privileges of individual users, like an access
    control list; see GroupResourcePrivilege and UserGroupPrivilege
    for other kinds of privilege.
    """

    privilege = models.IntegerField(choices=PrivilegeCodes.CHOICES,
                                    editable=False,
                                    default=PrivilegeCodes.VIEW)
    start = models.DateTimeField(editable=False, auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=False,
                             editable=False,
                             related_name='u2urp',
                             help_text='user to be granted privilege')

    resource = models.ForeignKey(BaseResource, on_delete=models.CASCADE,
                                 null=False,
                                 editable=False,
                                 related_name='r2urp',
                                 help_text='resource to which privilege applies')

    grantor = models.ForeignKey(User, on_delete=models.CASCADE,
                                null=False,
                                editable=False,
                                related_name='x2urp',
                                help_text='grantor of privilege')

    exhibit = models.BooleanField(default=False,
                                  null=False,
                                  editable=False,
                                  help_text='exhibit resource as product')

    class Meta:
        unique_together = ('user', 'resource')

    def __str__(self):
        """ Return printed depiction for debugging """
        return str.format("<user '{}' (id={}) holds {} ({})"
                          + " over resource '{}' (id={})"
                          + " via grantor '{}' (id={})>",
                          str(self.user.username), str(self.user.id),
                          PrivilegeCodes.NAMES[self.privilege],
                          str(self.privilege),
                          str(self.resource.title),
                          str(self.resource.short_id),
                          str(self.grantor.username), str(self.grantor.id))

    @classmethod
    def share(cls, **kwargs):
        """
        Share a resource with a user and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param resource: target resource.
        :param user: target user.
        :param privilege: privilege 1-4.
        :param grantor: user who requested privilege.

        Usage:
            UserResourcePrivilege.share(resource={X}, user={Y}, privilege={Z}, grantor={W})

        This routine links UserResourcePrivilege and UserResourceProvenance.
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserResourceProvenance
        # START(ID=446,NAME=PriveledgeShareUpdateClsUserResourcePrivilege,TYPE=UPDATE,OBJECTS=[UserResourcePrivilege])
        cls.update(**kwargs)
        # END(ID=446)
        # START(ID=447,NAME=PriveledgeShareUpdateClsUserResourceProvenance,TYPE=UPDATE,OBJECTS=[UserResourceProvenance])
        UserResourceProvenance.update(**kwargs)
        # END(ID=447)

    @classmethod
    def unshare(cls, **kwargs):
        """
        Unshare a resource with a user and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param resource: target resource.
        :param user: target user.
        :param grantor: user who requested privilege.

        Usage:
            UserResourcePrivilege.unshare(resource={X}, user={Y}, grantor={W})

        This routine links UserResourcePrivilege and UserResourceProvenance.

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        Use UserAccess.unshare_resource_with user instead. That routine avoids
        single-owner deletion.
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserResourceProvenance
        # START(ID=448,NAME=PriveledgeUnShareUpdateClsUserResourcePrivilege,TYPE=UPDATE,OBJECTS=[UserResourcePrivilege])
        cls.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=448)
        # START(ID=449,NAME=PriveledgeUnShareUpdateClsUserResourceProvenance,TYPE=UPDATE,OBJECTS=[UserResourceProvenance])
        UserResourceProvenance.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=449)

    @classmethod
    def undo_share(cls, **kwargs):
        """
        Undo a share of a resource with a user and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param resource: target resource.
        :param user: target user.
        :param grantor: user who requested privilege.

        Usage:
            UserResourcePrivilege.undo_share(resource={X}, user={Y}, grantor={W})

        In practice:

        The "undo" operation is independent of the privileges a user currently holds.
        Suppose -- for example -- that a user holds CHANGE, grants that to another user,
        and then loses CHANGE. The undo of the other user is still possible, even though the
        original user no longer has the privilege.

        This routine links UserResourcePrivilege and UserResourceProvenance.

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        Use UserAccess.undo_share_resource_with user instead. That routine avoids
        single-owner deletion.
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserResourceProvenance
        if __debug__:
            assert 'resource' in kwargs
            assert isinstance(kwargs['resource'], BaseResource)
            assert 'user' in kwargs
            assert isinstance(kwargs['user'], User)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
        # add an undo record to the provenance table.
        UserResourceProvenance.undo_share(**kwargs)
        # read that record.
        del kwargs['grantor']
        r = UserResourceProvenance.get_current_record(**kwargs)
        # post to privilege table.
        # START(ID=450,NAME=PriveledgeUndoShareUpdateClsUserResourcePrivilege,TYPE=UPDATE,OBJECTS=[UserResourcePrivilege])
        cls.update(user=r.user, resource=r.resource, privilege=r.privilege, grantor=r.grantor, exhibit=r.exhibit)
        # END(ID=450)

    @classmethod
    def get_undo_users(cls, **kwargs):
        """ Get a set of users for which the current user can undo privilege

        :param resource: resource to check
        :param grantor: user that will undo privilege

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        Use UserAccess.__get_resource_undo_users instead. That routine avoids single-owner
        deletion.
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserResourceProvenance
        if __debug__:
            assert 'resource' in kwargs
            assert isinstance(kwargs['resource'], BaseResource)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 2
        return UserResourceProvenance.get_undo_users(**kwargs)


class GroupResourcePrivilege(PrivilegeBase):
    """
    Privileges of a group over a resource.

    The group privilege over a resource is never directly meaningful;
    it is resolved instead into user privilege for each member of
    the group, as listed in UserGroupPrivilege above.
    """

    privilege = models.IntegerField(choices=PrivilegeCodes.CHOICES,
                                    editable=False,
                                    default=PrivilegeCodes.VIEW)
    start = models.DateTimeField(editable=False, auto_now=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              null=False,
                              editable=False,
                              related_name='g2grp',
                              help_text='group to be granted privilege')

    resource = models.ForeignKey(BaseResource, on_delete=models.CASCADE,
                                 null=False,
                                 editable=False,
                                 related_name='r2grp',
                                 help_text='resource to which privilege applies')

    grantor = models.ForeignKey(User, on_delete=models.CASCADE,
                                null=False,
                                editable=False,
                                related_name='x2grp',
                                help_text='grantor of privilege')

    exhibit = models.BooleanField(default=False,
                                  null=False,
                                  editable=False,
                                  help_text='exhibit resource as product')

    class Meta:
        unique_together = ('group', 'resource')

    def __str__(self):
        """ Return printed depiction for debugging """
        return str.format("<group '{}' (id={}) holds {} ({})"
                          + " over resource '{}' (id={})"
                          + " via grantor '{}' (id={})>",
                          str(self.group.name), str(self.group.id),
                          PrivilegeCodes.NAMES[self.privilege],
                          str(self.privilege),
                          str(self.resource.title),
                          str(self.resource.short_id),
                          str(self.grantor.username), str(self.grantor.id))

    @classmethod
    def share(cls, **kwargs):
        """
        Share a resource with a group and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param resource: target resource.
        :param group: target group.
        :param privilege: privilege 1-4.
        :param grantor: user who requested privilege.

        Usage:
            GroupResourcePrivilege.share(resource={X}, group={Y}, privilege={Z}, grantor={W})

        This routine links GroupResourceProvenance and GroupResourcePrivilege.
        """
        # prevent import loops
        from hs_access_control.models.provenance import GroupResourceProvenance
        # START(ID=451,NAME=PriveledgeShareUpdateClsGroupResourcePrivilege,TYPE=UPDATE,OBJECTS=[GroupResourcePrivilege])
        cls.update(**kwargs)
        # END(ID=451)
        # START(ID=452,NAME=PriveledgeShareUpdateClsGroupResourceProvenance,TYPE=UPDATE,OBJECTS=[GroupResourceProvenance])
        GroupResourceProvenance.update(**kwargs)
        # END(ID=452)

    @classmethod
    def unshare(cls, **kwargs):
        """
        Unshare a resource with a group and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param resource: target resource.
        :param group: target group.
        :param grantor: user who requested privilege.

        Usage:
            GroupResourcePrivilege.unshare(resource={X}, group={Y}, grantor={W})

        This routine links GroupResourceProvenance and GroupResourcePrivilege.
        """
        # prevent import loops
        from hs_access_control.models.provenance import GroupResourceProvenance
        # START(ID=453,NAME=PriveledgeUnShareUpdateClsGroupResourcePrivilege,TYPE=UPDATE,OBJECTS=[GroupResourcePrivilege])
        cls.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=453)
        # START(ID=454,NAME=PriveledgeUnShareUpdateClsGroupResourceProvenance,TYPE=UPDATE,OBJECTS=[GroupResourceProvenance])
        GroupResourceProvenance.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=454)

    @classmethod
    def undo_share(cls, **kwargs):
        """
        Undo a share of a resource with a group and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param resource: target resource.
        :param group: target group.
        :param grantor: user who requested privilege.

        Usage:
            GroupResourcePrivilege.undo_share(resource={X}, group={Y}, grantor={W})

        In practice:

        The "undo" operation is independent of the privileges a user currently holds.
        Suppose -- for example -- that a user holds CHANGE, grants that to another user,
        and then loses CHANGE. The undo of the other user is still possible, even though the
        original user no longer has the privilege.

        This routine links GroupResourceProvenance and GroupResourcePrivilege.
        """
        # prevent import loops
        from hs_access_control.models.provenance import GroupResourceProvenance
        if __debug__:
            assert 'resource' in kwargs
            assert isinstance(kwargs['resource'], BaseResource)
            assert 'group' in kwargs
            assert isinstance(kwargs['group'], Group)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
        GroupResourceProvenance.undo_share(**kwargs)
        del kwargs['grantor']
        r = GroupResourceProvenance.get_current_record(**kwargs)
        # START(ID=455,NAME=PriveledgeUndoShareUpdateClsGroupResourcePrivilege,TYPE=UPDATE,OBJECTS=[GroupResourcePrivilege])
        cls.update(group=r.group, resource=r.resource, privilege=r.privilege, grantor=r.grantor, exhibit=r.exhibit)
        # END(ID=455)

    @classmethod
    def get_undo_groups(cls, **kwargs):
        """ Get a set of groups for which the current user can undo privilege

        :param resource: resource to check
        :param grantor: user that will undo privilege

        **This is a system routine** that should not be called directly by developers!
        Use UserAccess.__get_resource_undo_groups instead.
        """
        # prevent import loops
        from hs_access_control.models.provenance import GroupResourceProvenance
        if __debug__:
            assert 'resource' in kwargs
            assert isinstance(kwargs['resource'], BaseResource)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 2
        return GroupResourceProvenance.get_undo_groups(**kwargs)


class UserCommunityPrivilege(PrivilegeBase):
    """ Privileges of a user over a community

    Having any privilege over a community is synonymous with membership.

    There is a reasonable meaning to PrivilegeCodes.NONE, which is to be
    a community member without the ability to discover the identities of other
    group members.  However, this is currently disallowed. It is used in the
    provenance models to record removing a privilege.
    """

    privilege = models.IntegerField(choices=PrivilegeCodes.CHOICES,
                                    editable=False,
                                    default=PrivilegeCodes.VIEW)
    start = models.DateTimeField(editable=False, auto_now=True)

    community = models.ForeignKey(Community, on_delete=models.CASCADE,
                                  null=False,
                                  editable=False,
                                  related_name='c2ucp',
                                  help_text='community to be granted privilege')

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=False,
                             editable=False,
                             related_name='u2ucp',
                             help_text='group providing privilege')

    grantor = models.ForeignKey(User, on_delete=models.CASCADE,
                                null=False,
                                editable=False,
                                related_name='x2ucp',
                                help_text='grantor of privilege')

    class Meta:
        unique_together = ('community', 'user')

    def __str__(self):
        """ Return printed depiction for debugging """
        return str.format("<community '{}' (id={}) holds {} ({})"
                          + " over user '{}' (id={})"
                          + " via grantor '{}' (id={})>",
                          str(self.community.name), str(self.community.id),
                          PrivilegeCodes.NAMES[self.privilege],
                          str(self.privilege),
                          str(self.user.username), str(self.user.id),
                          str(self.grantor.username), str(self.grantor.id))

    @classmethod
    def share(cls, **kwargs):
        """
        Share a community with a user and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param user: user to be granted access.
        :param community: target community with which to share
        :param privilege: privilege 1-4.
        :param grantor: user who requested privilege.

        Usage:
            UserCommunityPrivilege.share(user={X}, community={Y}, privilege={Z}, grantor={W}
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserCommunityProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'user' in kwargs
            assert isinstance(kwargs['user'], User)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert 'privilege' in kwargs
            assert \
                kwargs['privilege'] >= PrivilegeCodes.OWNER and \
                kwargs['privilege'] <= PrivilegeCodes.NONE
            assert len(kwargs) == 4
        # START(ID=456,NAME=PriveledgeShareUpdateClsUserCommunityPrivilege,TYPE=UPDATE,OBJECTS=[UserCommunityPrivilege])
        cls.update(**kwargs)
        # END(ID=456)
        # START(ID=457,NAME=PriveledgeShareUpdateClsUserCommunityProvenance,TYPE=UPDATE,OBJECTS=[UserCommunityProvenance])
        UserCommunityProvenance.update(**kwargs)
        # END(ID=457)

    @classmethod
    def unshare(cls, **kwargs):
        """
        Unshare a user with a community and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param user: user to unshare
        :param community: target community with which to unshare
        :param grantor: user who requested privilege.

        Usage:
            UserCommunityPrivilege.unshare(user={X}, user={Y}, grantor={W})

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        Use UserAccess.unshare_user_with_community instead. This prevents unsharing with single
        owners.
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserCommunityProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'user' in kwargs
            assert isinstance(kwargs['user'], User)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 3
        # START(ID=458,NAME=PriveledgeUnShareUpdateClsUserCommunityPrivilege,TYPE=UPDATE,OBJECTS=[UserCommunityPrivilege])
        cls.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=458)
        # START(ID=459,NAME=PriveledgeUnShareUpdateClsUserCommunityProvenance,TYPE=UPDATE,OBJECTS=[UserCommunityProvenance])
        UserCommunityProvenance.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=459)

    @classmethod
    def undo_share(cls, **kwargs):
        """
        Undo a share a user with a community and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param user: user for which to undo
        :param community: target community with which to undo share
        :param grantor: user who requested privilege.

        Usage:
            UserCommunityPrivilege.undo_share(community={X}, user={Y}, grantor={W})

        In practice:

        The "undo" operation is independent of the privileges a user currently holds.
        Suppose -- for example -- that a user holds CHANGE, grants that to another user,
        and then loses CHANGE. The undo of the other user is still possible, even though the
        original user no longer has the privilege.

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserCommunityProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'user' in kwargs
            assert isinstance(kwargs['user'], User)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 3
        grantor = kwargs['grantor']
        del kwargs['grantor']
        # undo in provenance model; add a record that reinstates previous privilege.
        UserCommunityProvenance.undo_share(grantor=grantor, **kwargs)
        # read that record and post to privilege table.
        r = UserCommunityProvenance.get_current_record(**kwargs)
        # START(ID=460,NAME=PriveledgeUndoShareUpdateClsUserCommunityPrivilege,TYPE=UPDATE,OBJECTS=[UserCommunityPrivilege])
        cls.update(community=r.community, user=r.user, privilege=r.privilege, grantor=r.grantor)
        # END(ID=460)

    @classmethod
    def get_undo_users(cls, **kwargs):
        """ Get a set of users for which a grantor can undo privilege

        :param community: community to check
        :param grantor: user that will undo privilege

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        """
        # prevent import loops
        from hs_access_control.models.provenance import UserCommunityProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 2
        return UserCommunityProvenance.get_undo_users(**kwargs)


class GroupCommunityPrivilege(PrivilegeBase):
    """ Privileges of a group over a community

    This encodes the privileges of a specific group over a community.

    * VIEW privilege means the group can view resources of the community.
    * No other privileges are allowed.

    There is a reasonable meaning to PrivilegeCodes.NONE, which is to be
    a community member without the ability to view anything in the community.
    However, this is currently disallowed. It is used in the provenance models
    to record removing a privilege.
    """

    privilege = models.IntegerField(choices=PrivilegeCodes.CHOICES,
                                    editable=False,
                                    default=PrivilegeCodes.VIEW)

    start = models.DateTimeField(editable=False, auto_now=True)

    community = models.ForeignKey(Community, on_delete=models.CASCADE,
                                  null=False,
                                  editable=False,
                                  related_name='c2gcp',
                                  help_text='community to be granted privilege')

    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              null=False,
                              editable=False,
                              related_name='g2gcp',
                              help_text='group providing privilege')

    grantor = models.ForeignKey(User, on_delete=models.CASCADE,
                                null=False,
                                editable=False,
                                related_name='x2gcp',
                                help_text='grantor of privilege')

    exhibit = models.BooleanField(default=False,
                                  null=False,
                                  editable=False,
                                  help_text='exhibit resource as product')

    class Meta:
        unique_together = ('community', 'group')

    def __str__(self):
        """ Return printed depiction for debugging """
        return str.format("<community '{}' (id={}) holds {} ({})"
                          + " over group '{}' (id={})"
                          + " via grantor '{}' (id={})>",
                          str(self.community.name), str(self.community.id),
                          PrivilegeCodes.NAMES[self.privilege],
                          str(self.privilege),
                          str(self.group.name), str(self.group.id),
                          str(self.grantor.username), str(self.grantor.id))

    @classmethod
    def share(cls, **kwargs):
        """
        Share a community with a group and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param group: source group to share
        :param community: target community with which to share
        :param privilege: privilege 1-4.
        :param grantor: user who requested privilege.

        Usage:
            GroupCommunityPrivilege.share(group={X}, community={Y}, privilege={Z}, grantor={W}
        """
        # prevent import loops
        from hs_access_control.models.provenance import GroupCommunityProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'group' in kwargs
            assert isinstance(kwargs['group'], Group)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert 'privilege' in kwargs
            assert \
                kwargs['privilege'] >= PrivilegeCodes.OWNER and \
                kwargs['privilege'] <= PrivilegeCodes.NONE
            assert len(kwargs) == 4
        # START(ID=461,NAME=PriveledgeShareUpdateClsGroupCommunityPrivilege,TYPE=UPDATE,OBJECTS=[GroupCommunityPrivilege])
        cls.update(**kwargs)
        # END(ID=461)
        # START(ID=462,NAME=PriveledgeShareUpdateClsGroupCommunityProvenance,TYPE=UPDATE,OBJECTS=[GroupCommunityProvenance])
        GroupCommunityProvenance.update(**kwargs)
        # END(ID=462)

    @classmethod
    def unshare(cls, **kwargs):
        """
        Unshare a group with a community and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param group: source group to share
        :param community: target community with which to unshare
        :param grantor: user who requested privilege.

        Usage:
            GroupCommunityPrivilege.unshare(group={X}, user={Y}, grantor={W})

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        Use UserAccess.unshare_group_with_community instead.
        """
        # prevent import loops
        from hs_access_control.models.provenance import GroupCommunityProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'group' in kwargs
            assert isinstance(kwargs['group'], Group)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 3
        # START(ID=463,NAME=PriveledgeUnShareUpdateClsGroupCommunityPrivilege,TYPE=UPDATE,OBJECTS=[GroupCommunityPrivilege])
        cls.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=463)
        # START(ID=464,NAME=PriveledgeUnShareUpdateClsGroupCommunityProvenanceTYPE=UPDATE,OBJECTS=[GroupCommunityProvenance])
        GroupCommunityProvenance.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=464)

    @classmethod
    def undo_share(cls, **kwargs):
        """
        Undo a share a group with a community and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param group: source group to undo
        :param community: target community with which to undo share
        :param grantor: user who requested privilege.

        Usage:
            GroupCommunityPrivilege.undo_share(community={X}, group={Y}, grantor={W})

        In practice:

        The "undo" operation is independent of the privileges a user currently holds.
        Suppose -- for example -- that a user holds CHANGE, grants that to another user,
        and then loses CHANGE. The undo of the other user is still possible, even though the
        original user no longer has the privilege.

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        """
        # prevent import loops
        from hs_access_control.models.provenance import GroupCommunityProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'group' in kwargs
            assert isinstance(kwargs['group'], Group)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 3
        grantor = kwargs['grantor']
        del kwargs['grantor']
        # undo in provenance model; add a record that reinstates previous privilege.
        GroupCommunityProvenance.undo_share(grantor=grantor, **kwargs)
        # read that record and post to privilege table.
        r = GroupCommunityProvenance.get_current_record(**kwargs)
        # START(ID=465,NAME=PriveledgeUndoShareUpdateClsGroupCommunityPrivilege,TYPE=UPDATE,OBJECTS=[GroupCommunityPrivilege])
        cls.update(community=r.community, group=r.group, privilege=r.privilege,
                   grantor=r.grantor, exhibit=r.exhibit)
        # END(ID=465)

    @classmethod
    def get_undo_groups(cls, **kwargs):
        """ Get a set of groups for which a grantor can undo privilege

        :param community: community to check
        :param grantor: user that will undo privilege

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        """
        # prevent import loops
        from hs_access_control.models.provenance import GroupCommunityProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 2
        return GroupCommunityProvenance.get_undo_groups(**kwargs)


class CommunityResourcePrivilege(PrivilegeBase):
    """ Privileges of a resource over a community

    This encodes the privileges of a specific resource over a community.

    * VIEW privilege means the resource can view resources of the community.
    * No other privileges are allowed.

    There is a reasonable meaning to PrivilegeCodes.NONE, which is to be
    a community member without the ability to view anything in the community.
    However, this is currently disallowed. It is used in the provenance models
    to record removing a privilege.
    """

    privilege = models.IntegerField(choices=PrivilegeCodes.CHOICES,
                                    editable=False,
                                    default=PrivilegeCodes.VIEW)

    start = models.DateTimeField(editable=False, auto_now=True)

    community = models.ForeignKey(Community, on_delete=models.CASCADE,
                                  null=False,
                                  editable=False,
                                  related_name='c2crp',
                                  help_text='community to be granted privilege')

    resource = models.ForeignKey(BaseResource, on_delete=models.CASCADE,
                                 null=False,
                                 editable=False,
                                 related_name='r2crp',
                                 help_text='resource providing privilege')

    grantor = models.ForeignKey(User, on_delete=models.CASCADE,
                                null=False,
                                editable=False,
                                related_name='x2crp',
                                help_text='grantor of privilege')

    exhibit = models.BooleanField(default=False,
                                  null=False,
                                  editable=False,
                                  help_text='exhibit resource as product')

    class Meta:
        unique_together = ('community', 'resource')

    def __str__(self):
        """ Return printed depiction for debugging """
        return str.format("<community '{}' (id={}) holds {} ({})"
                          + " over resource '{}' (id={})"
                          + " via grantor '{}' (id={})>",
                          str(self.community.name), str(self.community.id),
                          PrivilegeCodes.NAMES[self.privilege],
                          str(self.privilege),
                          str(self.resource.name), str(self.group.id),
                          str(self.grantor.username), str(self.grantor.id))

    @classmethod
    def share(cls, **kwargs):
        """
        Share a resource with a community and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param resource: source group to share
        :param community: target community with which to share
        :param privilege: privilege 1-4.
        :param grantor: user who requested privilege.

        Usage:
            CommunityResourcePrivilege.share(resource={X}, community={Y}, privilege={Z}, grantor={W}
        """
        # prevent import loops
        from hs_access_control.models.provenance import CommunityResourceProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'resource' in kwargs
            assert isinstance(kwargs['resource'], BaseResource)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert 'privilege' in kwargs
            assert \
                kwargs['privilege'] >= PrivilegeCodes.OWNER and \
                kwargs['privilege'] <= PrivilegeCodes.NONE
            assert len(kwargs) == 4
        # START(ID=466,NAME=PriveledgeShareUpdateClsCommunityResourcePrivilege,TYPE=UPDATE,OBJECTS=[CommunityResourcePrivilege])
        cls.update(**kwargs)
        # END(ID=466)
        # START(ID=467,NAME=PriveledgeShareUpdateClsCommunityResourceProvenance,TYPE=UPDATE,OBJECTS=[CommunityResourceProvenance])
        CommunityResourceProvenance.update(**kwargs)
        # END(ID=467)

    @classmethod
    def unshare(cls, **kwargs):
        """
        Unshare a resource with a community and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param resource: source group to share
        :param community: target community with which to unshare
        :param grantor: user who requested privilege.

        Usage:
            CommunityResourcePrivilege.unshare(resource={X}, user={Y}, grantor={W})

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        Use UserAccess.unshare_resource_with_community instead.
        """
        # prevent import loops
        from hs_access_control.models.provenance import CommunityResourceProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'resource' in kwargs
            assert isinstance(kwargs['resource'], BaseResource)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 3
        # START(ID=468,NAME=PriveledgeUnShareUpdateClsCommunityResourcePrivilege,TYPE=UPDATE,OBJECTS=[CommunityResourcePrivilege])
        cls.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=468)
        # START(ID=469,NAME=PriveledgeUnShareUpdateClsCommunityResourceProvenance,TYPE=UPDATE,OBJECTS=[CommunityResourceProvenance])
        CommunityResourceProvenance.update(privilege=PrivilegeCodes.NONE, **kwargs)
        # END(ID=469)

    @classmethod
    def undo_share(cls, **kwargs):
        """
        Undo a share a resource with a community and update provenance

        ***This completely bypasses access control*** but keeps provenance in sync.

        :param resource: source group to undo
        :param community: target community with which to undo share
        :param grantor: user who requested privilege.

        Usage:
            CommunityResourcePrivilege.undo_share(community={X}, resource={Y}, grantor={W})

        In practice:

        The "undo" operation is independent of the privileges a user currently holds.
        Suppose -- for example -- that a user holds CHANGE, grants that to another user,
        and then loses CHANGE. The undo of the other user is still possible, even though the
        original user no longer has the privilege.

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        """
        # prevent import loops
        from hs_access_control.models.provenance import CommunityResourceProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'resource' in kwargs
            assert isinstance(kwargs['resource'], BaseResource)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 3
        grantor = kwargs['grantor']
        del kwargs['grantor']
        # undo in provenance model; add a record that reinstates previous privilege.
        CommunityResourceProvenance.undo_share(grantor=grantor, **kwargs)
        # read that record and post to privilege table.
        r = CommunityResourceProvenance.get_current_record(**kwargs)
        # START(ID=470,NAME=PriveledgeUndoShareUpdateClsCommunityResourcePrivilege,TYPE=UPDATE,OBJECTS=[CommunityResourcePrivilege])
        cls.update(community=r.community, resource=r.resource, privilege=r.privilege, grantor=r.grantor)
        # END(ID=470)

    @classmethod
    def get_undo_resources(cls, **kwargs):
        """ Get a set of communities for which a grantor can undo privilege

        :param community: community to check
        :param grantor: user that will undo privilege

        Important: this does not guard against removing a single owner.

        **This is a system routine** that should not be called directly by developers!
        """
        # prevent import loops
        from hs_access_control.models.provenance import CommunityResourceProvenance
        if __debug__:
            assert 'community' in kwargs
            assert isinstance(kwargs['community'], Community)
            assert 'grantor' in kwargs
            assert isinstance(kwargs['grantor'], User)
            assert len(kwargs) == 2
        return CommunityResourceProvenance.get_undo_resources(**kwargs)
