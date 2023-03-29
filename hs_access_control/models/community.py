from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q, F, Exists, OuterRef
from django.contrib.contenttypes.models import ContentType

from hs_core.models import BaseResource
from theme.utils import get_upload_path_community
from sorl.thumbnail import ImageField as ThumbnailImageField


###################################
# Communities of groups
###################################
class Community(models.Model):
    """ a placeholder class for a community of groups """
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    purpose = models.TextField(null=True, blank=True)
    auto_approve = models.BooleanField(null=False, default=False, blank=False, editable=False)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    picture = ThumbnailImageField(upload_to=get_upload_path_community, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def member_groups(self):
        """ This returns all member groups """
        # START(ID=366,NAME=ModelCommunityMemberGroups,TYPE=SELECT,OBJECTS=[Group])
        return Group.objects.filter(gaccess__active=True,
                                    g2gcp__community=self)
        # END(ID=366)

    @property
    def member_users(self):
        # START(ID=367,NAME=ModelCommunityMemberUsers,TYPE=SELECT,OBJECTS=[User])
        return User.objects.filter(is_active=True, u2ucp__community=self)
        # END(ID=367)

    @property
    def owners(self):
        from hs_access_control.models.privilege import PrivilegeCodes
        # START(ID=368,NAME=ModelCommunityOwners,TYPE=SELECT,OBJECTS=[User])
        return User.objects.filter(is_active=True,
                                   u2ucp__community=self,
                                   u2ucp__privilege=PrivilegeCodes.OWNER)
        # END(ID=368)

    def groups_with_public_resources(self):
        """ Return the list of groups that have discoverable or public resources
            These must contain at least one resource that is discoverable and
            is owned by a group member.

            This query is subtle. See
                https://medium.com/@hansonkd/\
                the-dramatic-benefits-of-django-subqueries-and-annotations-4195e0dafb16
            for details of how this improves performance.

           As a short summary, all we need to know is that one resource exists.
           This is not possible to notate in the main query except through an annotation.
           However, that annotation is really efficient, and is implemented as a postgres
           subquery. This is a Django 1.11 extension.
        """
        from hs_access_control.models import PrivilegeCodes
        # START(ID=369,NAME=ModelCommunityGroupsWithPublicResources,TYPE=SELECT,OBJECTS=[BaseResource, Group])
        return self.member_groups\
            .annotate(
                has_public_resources=Exists(
                    BaseResource.objects.filter(
                        raccess__discoverable=True,
                        r2grp__group__id=OuterRef('id'),
                        r2urp__user__u2ugp__group__id=OuterRef('id'),
                        r2urp__privilege=PrivilegeCodes.OWNER)))\
            .filter(has_public_resources=True)\
            .order_by('name')
            # END(ID=369)

    @property
    def public_resources(self):
        """
        prepare a list of everything that gets displayed about each resource in a community.
        """
        # TODO: consider adding GenericRelation to expose reverse querying of metadata field.
        # TODO: This would enable fast querying of first author.
        # TODO: The side-effect of this is enabling deletion cascade, which shouldn't do anything.

        # import here to avoid import loops
        from hs_access_control.models.privilege import PrivilegeCodes

        # TODO: propagated resources should be owned by a member of the publishing group,
        # and not just any group in the community!
        # START(ID=370,NAME=ModelCommunityPublicResources,TYPE=SELECT,OBJECTS=[BaseResource])
        res = BaseResource\
            .objects\
            .filter(Q(r2grp__group__g2gcp__community=self,
                      r2grp__group__gaccess__active=True,
                      r2urp__privilege=PrivilegeCodes.OWNER,  # owned by member of community
                      r2urp__user__u2ugp__group__g2gcp__community=self)
                    | Q(r2crp__community=self))\
            .filter(Q(raccess__public=True)
                    | Q(raccess__published=True)
                    | Q(raccess__discoverable=True))\
            .annotate(group_name=F("r2grp__group__name"),
                      group_id=F("r2grp__group__id"),
                      public=F("raccess__public"),
                      published=F("raccess__published"),
                      discoverable=F("raccess__discoverable"))

        res = res.only('title', 'resource_type', 'created', 'updated')
        # END(ID=370)
        # # Can't do the following because the content model is polymorphic.
        # # This is documented as only working for monomorphic content_type
        # res = res.prefetch_related("content_object___title",
        #                            "content_object___description",
        #                            "content_object__creators")
        # We want something that is not O(# resources + # content types).
        # O(# content types) is sufficiently faster.
        # The following strategy is documented here:
        # https://blog.roseman.org.uk/2010/02/22/django-patterns-part-4-forwards-generic-relations/

        # collect generics from resources
        generics = {}
        for item in res:
            generics.setdefault(item.content_type.id, set()).add(item.object_id)

        # fetch all content types in one query
        # START(ID=371,NAME=ModelCommunityPublicResourcesContentType,TYPE=SELECT,OBJECTS=[ContentType])
        content_types = ContentType.objects.in_bulk(list(generics.keys()))
        # END(ID=371)

        # build a map between content types and the objects that use them.
        relations = {}
        for ct, fk_list in list(generics.items()):
            ct_model = content_types[ct].model_class()
            # START(ID=372,NAME=ModelCommunityPublicResourcesContentTypeModelClass,TYPE=SELECT,OBJECTS=[ContentType])
            relations[ct] = ct_model.objects.in_bulk(list(fk_list))
            # END(ID=372)

        # force-populate the cache of content type objects.
        for item in res:
            setattr(item, '_content_object_cache',
                    relations[item.content_type.id][item.object_id])

        # Detailed notes:
        # This subverts chained lookup by pre-populating the content object cache
        # that is populated by an object reference. It is very dependent upon the
        # implementation of GenericRelation and its pre-fetching strategy.
        # Thus it is quite brittle and vulnerable to major revisions of Generics.

        return res

    # TODO: this currently contains OWNER privilege only
    def get_effective_user_privilege(self, this_user):
        from hs_access_control.models.privilege import UserCommunityPrivilege
        return UserCommunityPrivilege.get_privilege(user=this_user, community=self)

    # TODO: this is never > VIEW.
    def get_effective_group_privilege(self, this_group):
        from hs_access_control.models.privilege import GroupCommunityPrivilege
        return GroupCommunityPrivilege.get_privilege(group=this_group, community=self)

    # TODO: this is never > VIEW.
    def get_effective_resource_privilege(self, this_resource):
        from hs_access_control.models.privilege import CommunityResourcePrivilege
        return CommunityResourcePrivilege.get_privilege(resource=this_resource, community=self)

    def get_groups_with_explicit_access(self, privilege, user=None):
        """
        Groups that contain resources that should be displayed for a community and/or user

        :param privilege: access privilege 1-3
        :param user: (optional) user whose groups should be excluded, because the user is
        already a member of the groups without community access.

        """
        if user is None:
            # START(ID=373,NAME=ModelCommunityGetGroupsWithExplicitAccessUserNone,TYPE=SELECT,OBJECTS=[Group])
            return Group.objects.filter(g2gcp__community=self, g2gcp__privilege=privilege)
            # END(ID=373)
        else:
            # START(ID=374,NAME=ModelCommunityGetGroupsWithExplicitAccess,TYPE=SELECT,OBJECTS=[Group])
            return Group.objects.filter(g2gcp__community=self, g2gcp__privilege=privilege)\
                .exclude(g2ugp__user=user)
            # END(ID=374)

    def is_superuser(self, user):
        """
        Return whether a user is a superuser over the community self.
        """
        # prevent import loops
        from hs_access_control.models.privilege import GroupCommunityPrivilege, PrivilegeCodes
        # START(ID=375,NAME=ModelCommunityIsSuperuser,TYPE=SELECT,OBJECTS=[GroupCommunityPrivilege])
        return GroupCommunityPrivilege.objects.filter(community=self, group__g2ugp__user=user,
                                                      privilege=PrivilegeCodes.CHANGE).exists()
        # END(ID=375)

    def get_resources_with_explicit_access(self, user, group, privilege):
        """
        Get community resources available at a specific privilege for a given user and group.
        This routine is the root of the routines for rendering a community's holdings.
        The group determines which resources will be listed.

        This listing routine has been separated from the main listing routines to avoid
        corrupting existing group views of resources, which have different protections than this.
        """
        from hs_access_control.models.privilege import PrivilegeCodes

        if group is None:
            # At this level, CHANGE is never allowed
            if privilege != PrivilegeCodes.VIEW:
                return BaseResource.objects.none()
            # direct access without group assocation with resource
            # START(ID=376,NAME=ModelCommunityGetResourcesWithExplicitAccessGroupNone,TYPE=SELECT,OBJECTS=[BaseResource])
            return BaseResource.objects.filter(
                Q(r2crp__community=self, r2crp__community__c2urp__user=user)
                | Q(r2crp__community=self, r2crp__community__c2gcp__group__g2ugp__user=user))\
                .distinct()
            # END(ID=376)

        # if user is a member, member privileges apply regardless of superuser privileges
        # (superusers only obtain member privileges over every group in the community)
        elif group.gaccess.members.filter(id=user.id).exists() or self.is_superuser(user):
            if privilege == PrivilegeCodes.CHANGE:
                # START(ID=377,NAME=ModelCommunityGetResourcesWithExplicitAccessGroupPrivilegeChange,TYPE=SELECT,OBJECTS=[BaseResource])
                return BaseResource.objects.filter(raccess__immutable=False,
                                                   r2grp__group=group,
                                                   r2grp__privilege=privilege)
                # END(ID=377)
            else:
                # START(ID=378,NAME=ModelCommunityGetResourcesWithExplicitAccessGroupPrivilegeNotChange,TYPE=SELECT,OBJECTS=[BaseResource])
                return BaseResource.objects.filter(r2grp__group=group,
                                                   r2grp__privilege=privilege)
                # END(ID=378)
        # now user is not a member of group and not a superuser
        elif privilege == PrivilegeCodes.CHANGE:  # requires superuser
            return BaseResource.objects.none()
        else:  # VIEW is requested for regular user via community
            return BaseResource.objects.none()

    @property
    def first_owner(self):
        from hs_access_control.models.privilege import UserCommunityPrivilege, PrivilegeCodes
        # START(ID=379,NAME=ModelCommunityFirstOwner,TYPE=SELECT,OBJECTS=[UserCommunityPrivilege])
        opriv = UserCommunityPrivilege.objects.filter(community=self, privilege=PrivilegeCodes.OWNER)\
            .order_by('start')
        # END(ID=379)
        opriv = list(opriv)
        if opriv:
            return opriv[0].user
        else:
            return None
