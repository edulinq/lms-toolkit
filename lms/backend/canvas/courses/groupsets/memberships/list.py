import typing

import lms.backend.canvas.common
import lms.model.groups
import lms.model.groupsets
import lms.model.users

BASE_ENDPOINT = "/api/v1/group_categories/{groupset_id}/export"

def request(backend: typing.Any,
        course_id: int,
        groupset_id: int,
        ) -> typing.List[lms.model.groupsets.GroupSetMembership]:
    """ List group set memberships. """

    url = backend.server + BASE_ENDPOINT.format(groupset_id = groupset_id)
    headers = backend.get_standard_headers()

    raw_text = lms.backend.canvas.common.make_get_request(url, headers = headers, json = False)
    if (raw_text is None):
        identifiers = {
            'course_id': course_id,
            'groupset_id': groupset_id,
        }
        backend.not_found('list group set memberships', identifiers)

        return []

    raw_objects = _parse_csv(raw_text)

    groupset_query = lms.model.groupsets.GroupSetQuery(id = groupset_id)

    memberships = []
    for raw_object in raw_objects:
        # Canvas includes unassigned users.
        if (raw_object.get('canvas_group_id', None) is None):
            continue

        user_query = lms.model.users.UserQuery(
            id = raw_object.get('canvas_user_id', None),
            name = raw_object.get('name', None),
            email = raw_object.get('user_id', None)
        )
        group_query = lms.model.groups.GroupQuery(
            id = raw_object.get('canvas_group_id', None),
            name = raw_object.get('group_name', None),
        )

        membership = lms.model.groupsets.GroupSetMembership(user = user_query, groupset = groupset_query, group = group_query)
        memberships.append(membership)

    return memberships

def _parse_csv(text: str) -> typing.List[typing.Dict[str, str]]:
    rows: typing.List[typing.Dict[str, str]] = []
    headers = None

    for line in text.splitlines():
        if (len(line.strip()) == 0):
            continue

        parts = [part.strip() for part in line.split(',')]

        if (headers is None):
            headers = parts
            continue

        if (len(parts) != len(headers)):
            raise ValueError("Canvas returned an improperly formatted CSV file.")

        rows.append({headers[i]: parts[i] for i in range(len(headers))})

    return rows
