import typing

import lms.backend.canvas.common
import lms.backend.canvas.model
import lms.model.backend
import lms.model.groups
import lms.model.groupsets
import lms.model.users

BASE_ENDPOINT = "/api/v1/groups/{group_id}/users?per_page={page_size}"

def request(backend: lms.model.backend.APIBackend,
        course_id: int,
        groupset_id: int,
        group_id: int,
        ) -> typing.List[lms.model.groupsets.GroupSetMembership]:
    """ List a group memberships. """

    url = backend.server + BASE_ENDPOINT.format(group_id = group_id, page_size = lms.backend.canvas.common.DEFAULT_PAGE_SIZE)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
            'groupset_id': groupset_id,
            'group_id': group_id,
        }
        backend.not_found('list group memberships', identifiers)

        return []

    groupset_query = lms.model.groupsets.GroupSetQuery(id = groupset_id)
    group_query = lms.model.groups.GroupQuery(id = group_id)

    memberships = []
    for raw_object in raw_objects:
        user = lms.backend.canvas.model.course_user(backend, raw_object)
        membership = lms.model.groupsets.GroupSetMembership(user = user.to_query(), groupset = groupset_query, group = group_query)
        memberships.append(membership)

    return memberships
