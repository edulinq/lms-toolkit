import typing

import lms.backend.canvas.common
import lms.backend.canvas.model
import lms.model.backend
import lms.model.users

BASE_ENDPOINT = "/api/v1/courses/{course_id}/users?per_page={page_size}"

def request(backend: lms.model.backend.APIBackend,
        course_id: int,
        include_role: bool = True,
        ) -> typing.List[lms.model.users.CourseUser]:
    """ List course users. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, page_size = lms.backend.canvas.common.DEFAULT_PAGE_SIZE)
    headers = backend.get_standard_headers()

    if (include_role):
        url += '&include[]=enrollments'

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
        }
        backend.not_found('list users', identifiers)

        return []

    return [lms.backend.canvas.model.course_user(backend, raw_object) for raw_object in raw_objects]
