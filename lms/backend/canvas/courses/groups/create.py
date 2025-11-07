import typing

import lms.backend.canvas.common
import lms.backend.canvas.model
import lms.model.constants
import lms.model.groups

BASE_ENDPOINT = "/api/v1/group_categories/{groupset_id}/groups"

def request(backend: typing.Any,
        course_id: int,
        groupset_id: int,
        name: str,
        ) -> lms.model.groups.Group:
    """ Create a group. """

    url = backend.server + BASE_ENDPOINT.format(groupset_id = groupset_id)
    headers = backend.get_standard_headers()

    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    data = {
        'name': name,
    }

    raw_object = lms.backend.canvas.common.make_post_request(url, headers = headers, data = data)
    if (raw_object is None):
        identifiers = {
            'course_id': course_id,
            'groupset_id': groupset_id,
        }
        backend.not_found('create group', identifiers)

        raise ValueError(f"Unable to create group '{name}' for course '{course_id}' and group set '{groupset_id}'.")

    return lms.backend.canvas.model.group(raw_object)
