import typing

import lms.backend.canvas.common
import lms.model.constants

BASE_ENDPOINT = "/api/v1/group_categories/{groupset_id}"

def request(backend: typing.Any,
        course_id: int,
        groupset_id: int,
        ) -> bool:
    """ Delete a group set. """

    url = backend.server + BASE_ENDPOINT.format(groupset_id = groupset_id)
    headers = backend.get_standard_headers()

    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    raw_object = lms.backend.canvas.common.make_delete_request(url, headers = headers)
    if (raw_object is None):
        identifiers = {
            'course_id': course_id,
            'groupset_id': groupset_id,
        }
        backend.not_found('delete group set', identifiers)

        return False

    return True
