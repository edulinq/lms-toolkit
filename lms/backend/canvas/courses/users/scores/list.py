import typing

import lms.backend.canvas.common
import lms.backend.canvas.model.scores

BASE_ENDPOINT = "/api/v1/courses/{course_id}/students/submissions"

def request(backend: typing.Any,
        course_id: int,
        user_id: int,
        ) -> typing.List[lms.backend.canvas.model.scores.AssignmentScore]:
    """ List user scores. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id)
    headers = backend.get_standard_headers()

    data = {
        'student_ids[]': str(user_id),
    }

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers, data = data)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
            'user_id': user_id,
        }
        backend.not_found('user scores', identifiers)

        return []

    scores = []
    for raw_object in raw_objects:
        # Check if this is an actual submission and not just a placeholder.
        if (raw_object.get('workflow_state', None) == 'unsubmitted'):
            continue

        scores.append(lms.backend.canvas.model.scores.AssignmentScore(**raw_object))

    return scores
