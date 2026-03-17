import typing

import lms.backend.canvas.common
import lms.backend.canvas.model
import lms.model.quizzes

BASE_ENDPOINT = "/api/v1/courses/{course_id}/quizzes?per_page={page_size}"

def request(backend: typing.Any,
        course_id: int,
        fetch_resources: bool = False,
        ) -> typing.List[lms.model.quizzes.Quiz]:
    """ List course quizzes. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, page_size = lms.backend.canvas.common.DEFAULT_PAGE_SIZE)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
        }
        backend.not_found('list quizzes', identifiers)

        return []

    return [lms.backend.canvas.model.quiz(backend, raw_object, fetch_resources) for raw_object in raw_objects]
