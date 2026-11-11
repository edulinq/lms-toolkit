import typing

import lms.backend.canvas.common

BASE_ENDPOINT = "/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}"

def request(backend: typing.Any,
        course_id: int,
        assignment_id: int,
        user_id: int,
        comment: str,
        ) -> bool:
    """ Add a submission comment. """

    if (len(comment.strip()) == 0):
        raise ValueError('Comment must not be empty.')

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, assignment_id = assignment_id, user_id = user_id)
    headers = backend.get_standard_headers(write = True)

    data = {
        'comment[text_comment]': comment,
    }

    raw_object = lms.backend.canvas.common.make_put_request(url, headers = headers, data = data)
    if (raw_object is None):
        identifiers = {
            'course_id': course_id,
            'assignment_id': assignment_id,
            'user_id': user_id,
        }
        backend.not_found('add submission comment', identifiers)

        return False

    return True
