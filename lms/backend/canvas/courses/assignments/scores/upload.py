import typing

import lms.backend.canvas.common
import lms.model.constants
import lms.model.scores

BASE_ENDPOINT = "/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/update_grades"

def request(backend: typing.Any,
        course_id: int,
        assignment_id: int,
        scores: typing.Dict[int, lms.model.scores.ScoreFragment],
        ) -> int:
    """ Upload scores and return the number of scores sent. """

    if (len(scores) == 0):
        return 0

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, assignment_id = assignment_id)
    headers = backend.get_standard_headers()

    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    data = {}
    for (user_id, score) in scores.items():
        text_score = ''
        if (score.score is not None):
            text_score = str(score.score)

        data[f"grade_data[{user_id}][posted_grade]"] = text_score

        if ((score.comment is not None) and (len(score.comment) > 0)):
            data[f"grade_data[{user_id}][text_comment]"] = score.comment

    response = lms.backend.canvas.common.make_post_request(url, headers = headers, data = data)
    if (response is None):
        return 0

    return len(scores)
