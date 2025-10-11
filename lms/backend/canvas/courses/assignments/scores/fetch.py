import typing

import lms.backend.canvas.common
import lms.backend.canvas.model.scores

BASE_ENDPOINT = "/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}"

def request(backend: typing.Any,
        course_id: int,
        assignment_id: int,
        user_id: int,
        ) -> typing.Union[lms.backend.canvas.model.scores.AssignmentScore, None]:
    """ Fetch a single assignment score. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, assignment_id = assignment_id, user_id = user_id)
    headers = backend.get_standard_headers()

    raw_object = lms.backend.canvas.common.make_get_request(url, headers)
    if (raw_object is None):
        identifiers = {
            'course_id': course_id,
            'assignment_id': assignment_id,
            'user_id': user_id,
        }
        backend.not_found('assignment score', identifiers)

        return None

    # Check if this is an actual submission and not just a placeholder.
    if (raw_object.get('workflow_state', None) == 'unsubmitted'):
        return None

    return lms.backend.canvas.model.scores.AssignmentScore(**raw_object)
