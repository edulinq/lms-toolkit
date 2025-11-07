import typing

import lms.backend.canvas.common
import lms.backend.canvas.model
import lms.model.constants
import lms.model.groupsets

BASE_ENDPOINT = "/api/v1/courses/{course_id}/group_categories"

def request(backend: typing.Any,
        course_id: int,
        name: str,
        ) -> lms.model.groupsets.GroupSet:
    """ Create a group set. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id)
    headers = backend.get_standard_headers()

    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    data = {
        'name': name,
    }

    raw_object = lms.backend.canvas.common.make_post_request(url, headers = headers, data = data)
    if (raw_object is None):
        identifiers = {
            'course_id': course_id,
        }
        backend.not_found('create group set', identifiers)

        raise ValueError(f"Unable to create group set '{name}' for course '{course_id}'.")

    return lms.backend.canvas.model.group_set(raw_object)
