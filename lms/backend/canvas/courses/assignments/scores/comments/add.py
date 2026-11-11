import typing

import lms.backend.canvas.common

BASE_ENDPOINT = "/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}"

def request(backend: typing.Any,
        course_id: int,
        assignment_id: int,
        user_id: int,
        comment: str,
        ) -> bool:
    """ Add a submission comment without sending or clearing a grade. """

    if (len(comment.strip()) == 0):
        raise ValueError('Comment must not be empty.')

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, assignment_id = assignment_id, user_id = user_id)
    headers = backend.get_standard_headers(write = True)

    # Do not reuse score upload: a missing score there explicitly clears the grade.
    response = lms.backend.canvas.common.make_put_request(url, headers = headers, data = {'comment[text_comment]': comment})
    return (response is not None)
