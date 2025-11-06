import typing

import lms.backend.canvas.common
import lms.model.constants

BASE_ENDPOINT = "/api/v1/groups/{group_id}/users"

def request(backend: typing.Any,
        course_id: int,
        groupset_id: int,
        group_id: int,
        user_ids: typing.List[int],
        ) -> int:
    """ Subtract users from a group. """

    url = backend.server + BASE_ENDPOINT.format(group_id = group_id)
    headers = backend.get_standard_headers()

    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    data = {
        'user_ids[]': sorted(user_ids),
    }

    raw_object = lms.backend.canvas.common.make_delete_request(url, headers = headers, data = data)
    if (raw_object is None):
        identifiers = {
            'course_id': course_id,
            'groupset_id': groupset_id,
            'group_id': group_id,
            'user_ids': user_ids,
        }
        backend.not_found('subtract group memberships', identifiers)

        return 0

    return len(raw_object['deleted_user_ids'])
