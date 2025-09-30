import typing

import lms.backend.canvas.common
import lms.backend.canvas.model.users

BASE_ENDPOINT = "/api/v1/courses/{course_id}/users?user_ids[]={user_id}"

def request(backend: typing.Any,
        course_id: int,
        user_id: int,
        include_role: bool = True,
        ) -> typing.Union[lms.backend.canvas.model.users.CourseUser, None]:
    """ Fetch a single course user. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, user_id = user_id)
    headers = backend.get_standard_headers()

    if (include_role):
        url += '&include[]=enrollments'

    raw_object = lms.backend.canvas.common.make_get_request(url, headers, raise_on_404 = False)
    if (raw_object is None):
        return None

    if (len(raw_object) != 1):
        return None

    return lms.backend.canvas.model.users.CourseUser(**raw_object[0])
