import typing

import lms.backend.canvas.common
import lms.backend.canvas.model
import lms.model.quizzes

BASE_ENDPOINT = "/api/v1/courses/{course_id}/quizzes/{quiz_id}/groups?per_page={page_size}"

def request(backend: typing.Any,
        course_id: int,
        quiz_id: int
        ) -> typing.List[lms.model.quizzes.QuestionGroup]:
    """ List quiz question groups. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, quiz_id = quiz_id, page_size = lms.backend.canvas.common.DEFAULT_PAGE_SIZE)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
            'quiz_id': quiz_id,
        }
        backend.not_found('list quiz question groups', identifiers)

        return []

    return sorted([lms.backend.canvas.model.quiz_question_group(raw_object) for raw_object in raw_objects.get('quiz_groups', [])])
