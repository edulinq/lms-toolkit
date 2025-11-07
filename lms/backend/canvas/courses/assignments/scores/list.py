import typing

import lms.backend.canvas.common
import lms.backend.canvas.model
import lms.model.scores

BASE_ENDPOINT = "/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions"

def request(backend: typing.Any,
        course_id: int,
        assignment_id: int,
        ) -> typing.List[lms.model.scores.AssignmentScore]:
    """ List assignment scores. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, assignment_id = assignment_id)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
            'assignment_id': assignment_id,
        }
        backend.not_found('list assignment scores', identifiers)

        return []

    scores = []
    for raw_object in raw_objects:
        # Check if this is an actual submission and not just a placeholder.
        if (raw_object.get('workflow_state', None) == 'unsubmitted'):
            continue

        scores.append(lms.backend.canvas.model.assignment_score(raw_object))

    return scores
