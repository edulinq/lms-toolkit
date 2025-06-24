import lms.api.group.common
import lms.api.group.listgroupings
import lms.api.group.listgroups
import lms.api.resolve

def fetch_and_resolve_grouping_id(server, token, course, grouping_query):
    groupings = fetch_and_resolve_groupings(server, token, course, [grouping_query])
    if (len(groupings) == 0):
        return None

    return groupings[0].get('id', None)

def fetch_and_resolve_groupings(server, token, course, grouping_queries,
        keys = lms.api.group.common.DEFAULT_KEYS):
    return lms.api.resolve.fetch_and_resolve(server, token, course, grouping_queries,
            lms.api.group.listgroupings.request,
            keys = keys, resolve_kwargs = {'match_email': False, 'label_uses_email': False})

def fetch_and_resolve_group_id(server, token, course, group_query):
    groups = fetch_and_resolve_groups(server, token, course, [group_query])
    if (len(groups) == 0):
        return None

    return groups[0].get('id', None)

def fetch_and_resolve_groups(server, token, course, group_queries,
        keys = lms.api.group.common.DEFAULT_KEYS):
    return lms.api.resolve.fetch_and_resolve(server, token, course, group_queries,
            lms.api.group.listgroups.request,
            keys = keys, resolve_kwargs = {'match_email': False, 'label_uses_email': False})


def requires_resolution(groups):
    return lms.api.resolve.requires_resolution(groups)
