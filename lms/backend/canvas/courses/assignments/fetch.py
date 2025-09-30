import typing

import lms.backend.canvas.common
import lms.backend.canvas.model.assignments

BASE_ENDPOINT = "/api/v1/courses/{course_id}/assignments/{assignment_id}"

def request(backend: typing.Any,
        course_id: int,
        assignment_id: int,
        ) -> typing.Union[lms.backend.canvas.model.assignments.Assignment, None]:
    """ Fetch a single course assignment. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, assignment_id = assignment_id)
    headers = backend.get_standard_headers()

    raw_object = lms.backend.canvas.common.make_get_request(url, headers, raise_on_404 = False)
    if (raw_object is None):
        return None

    return lms.backend.canvas.model.assignments.Assignment(**raw_object)
