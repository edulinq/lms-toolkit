import typing

import lms.backend.canvas.common
import lms.backend.canvas.model
import lms.model.assignments

BASE_ENDPOINT = "/api/v1/courses/{course_id}/assignments?per_page={page_size}"

def request(backend: typing.Any,
        course_id: int,
        ) -> typing.List[lms.model.assignments.Assignment]:
    """ List course assignments. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, page_size = lms.backend.canvas.common.DEFAULT_PAGE_SIZE)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
        }
        backend.not_found('list assignments', identifiers)

        return []

    return [lms.backend.canvas.model.assignment(raw_object) for raw_object in raw_objects]
