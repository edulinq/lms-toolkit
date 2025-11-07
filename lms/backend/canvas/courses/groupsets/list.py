import typing

import lms.backend.canvas.common
import lms.backend.canvas.model
import lms.model.groupsets

BASE_ENDPOINT = "/api/v1/courses/{course_id}/group_categories?per_page={page_size}"

def request(backend: typing.Any,
        course_id: int,
        ) -> typing.List[lms.model.groupsets.GroupSet]:
    """ List course group sets. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, page_size = lms.backend.canvas.common.DEFAULT_PAGE_SIZE)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
        }
        backend.not_found('list group sets', identifiers)

        return []

    return [lms.backend.canvas.model.group_set(raw_object) for raw_object in raw_objects]
