"""
Utility functions for management commands for access control.
"""

from django.contrib.auth.models import User, Group
from hs_core.models import BaseResource
from hs_access_control.models.community import Community
import re


RE_INT = re.compile(r'^([1-9]\d*|0)$')


def group_from_name_or_id(gname):
    """ return a group object given either an id or a name """

    if RE_INT.match(gname):
        try:
            gid = int(gname)
            # START(ID=139,NAME=GetGroupByIdRegex,TYPE=SELECT,OBJECTS=[Group])
            group = Group.objects.get(id=gid)
            # END(ID=139)
            return group
        except Group.DoesNotExist:
            print("group with id {} does not exist.".format(str(gid)))
            return None

    else:  # interpret as name
        # START(ID=140,NAME=GetGroupInterpretAsName,TYPE=SELECT,OBJECTS=[Group])
        groups = Group.objects.filter(name=gname)
        # END(ID=140)
        if groups.count() == 0:
            print("group '{}' not found.".format(gname))
            return None
        elif groups.count() == 1:
            group = groups[0]
            return group
        else:
            print("Group name {} is not unique. Please use group id instead:".format(gname))
            for g in groups:
                print("   '{}' (id={})".format(g.name, str(g.id)))
            return None


def community_from_name_or_id(cname):
    """ return a group object given either an id or a name """

    if RE_INT.match(cname):
        try:
            cid = int(cname)
            # START(ID=141,NAME=GetCommunityIdRegex,TYPE=SELECT,OBJECTS=[Community])
            group = Community.objects.get(id=cid)
            # END(ID=141)
            return group
        except Community.DoesNotExist:
            print("community with id {} does not exist.".format(str(cid)))
            return None

    else:  # interpret as name
        # START(ID=142,NAME=GetCommunityInterpretAsName,TYPE=SELECT,OBJECTS=[Community])
        communities = Community.objects.filter(name=cname)
        # END(ID=142)
        if communities.count() == 0:
            print("community with name '{}' does not exist.".format(cname))
            return None

        elif communities.count() == 1:
            community = communities[0]
            return community
        else:
            print("Community name '{}' is not unique. Please use community id instead:"
                  .format(cname))
            for g in communities:
                print("   '{}' (id={})".format(g.name, str(g.id)))
            return None


def user_from_name(uname):
    try:
        # START(ID=143,NAME=GetUserFromName,TYPE=SELECT,OBJECTS=[User])
        return User.objects.get(username=uname)
        # END(ID=143)
    except User.DoesNotExist:
        print("user with username '{}' does not exist.".format(uname))
        return None


def resource_from_id(id):
    try:
        # START(ID=144,NAME=GetBaseResourceFromShortId,TYPE=SELECT,OBJECTS=[BaseResource])
        return BaseResource.objects.get(short_id=id)
        # END(ID=144)
    except BaseResource.DoesNotExist:
        print("resource with id '{} does not exist.".format(id))
        return None
