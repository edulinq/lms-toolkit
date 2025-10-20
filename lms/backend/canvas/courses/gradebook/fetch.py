import typing

import lms.backend.canvas.common
import lms.backend.canvas.model.scores
import lms.model.scores

BASE_ENDPOINT = "/api/v1/courses/{course_id}/students/submissions"

def request(backend: typing.Any,
        course_id: int,
        assignment_ids: typing.List[int],
        user_ids: typing.List[int],
        ) -> lms.model.scores.Gradebook:
    """ Fetch a gradebook for the given users and assignments. """

    url = backend.server + BASE_ENDPOINT.format(course_id = course_id)
    headers = backend.get_standard_headers()

    data = {
        'per_page': lms.backend.canvas.common.DEFAULT_PAGE_SIZE,
        'assignment_ids[]': [str(assignment_id) for assignment_id in assignment_ids],
        'student_ids[]': [str(user_id) for user_id in user_ids],
    }

    assignment_queries = [lms.model.assignments.AssignmentQuery(id = id) for id in assignment_ids]
    user_queries = [lms.model.users.UserQuery(id = id) for id in user_ids]
    gradebook = lms.model.scores.Gradebook(assignment_queries, user_queries)

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers, data = data)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
            'assignment_ids': assignment_ids,
            'user_ids': user_ids,
        }
        backend.not_found('gradebook', identifiers)

        return gradebook

    for raw_object in raw_objects:
        # Check if this is an actual submission and not just a placeholder.
        if (raw_object.get('workflow_state', None) == 'unsubmitted'):
            continue

        gradebook.add(lms.backend.canvas.model.scores.AssignmentScore(**raw_object))

    return gradebook
