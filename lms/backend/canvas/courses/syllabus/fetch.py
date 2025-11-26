import typing

import lms.backend.canvas.common

BASE_ENDPOINT = "/api/v1/courses/{course_id}"

def request(backend: typing.Any,
        course_id: int,
        ) -> typing.Union[str, None]:
    """ Fetch a course syllabus. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id)
    headers = backend.get_standard_headers()

    data = {
        'include': ['syllabus_body'],
    }

    raw_object = lms.backend.canvas.common.make_get_request(url, headers = headers, data = data)
    if (raw_object is None):
        identifiers = {
            'course_id': course_id,
        }
        backend.not_found('fetch syllabus', identifiers)

        return None

    result = raw_object.get('syllabus_body', None)
    if (result is None):
        return None

    return str(result)
