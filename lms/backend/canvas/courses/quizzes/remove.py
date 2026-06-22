import typing

import lms.backend.canvas.common
import lms.model.constants

BASE_ENDPOINT = "/api/v1/courses/{course_id}/quizzes/{quiz_id}"

def request(backend: typing.Any,
        course_id: int,
        quiz_id: int,
        ) -> None:
    """ Remove a quiz. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, quiz_id = quiz_id)
    headers = backend.get_standard_headers()

    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    lms.backend.canvas.common.make_delete_request(url, headers = headers)
