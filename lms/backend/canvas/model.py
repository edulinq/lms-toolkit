import typing

import lms.backend.canvas.common
import lms.model.assignments
import lms.model.backend
import lms.model.courses
import lms.model.groups
import lms.model.groupsets
import lms.model.scores
import lms.model.users
import lms.util.parse

ENROLLMENT_TYPE_TO_ROLE: typing.Dict[str, lms.model.users.CourseRole] = {
    'ObserverEnrollment': lms.model.users.CourseRole.OTHER,
    'StudentEnrollment': lms.model.users.CourseRole.STUDENT,
    'TaEnrollment': lms.model.users.CourseRole.GRADER,
    'DesignerEnrollment': lms.model.users.CourseRole.ADMIN,
    'TeacherEnrollment': lms.model.users.CourseRole.OWNER,
}
"""
Canvas enrollment types mapped to roles.
This map is ordered by priority/power.
The later in the dict, the more power.
"""

_testing_override: bool = False  # pylint: disable=invalid-name
""" A special override to signal testing. """

def assignment(data: typing.Dict[str, typing.Any]) -> lms.model.assignments.Assignment:
    """
    Create a Canvas assignment associated with a course.

    See: https://developerdocs.instructure.com/services/canvas/resources/assignments
    """

    for field in ['id']:
        if (field not in data):
            raise ValueError(f"Canvas assignment is missing '{field}' field.")

    # Modify specific arguments before creation.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')
    data['due_date'] = lms.backend.canvas.common.parse_timestamp(data.get('due_at', None))
    data['open_date'] = lms.backend.canvas.common.parse_timestamp(data.get('unlock_at', None))
    data['close_date'] = lms.backend.canvas.common.parse_timestamp(data.get('lock_at', None))

    return lms.model.assignments.Assignment(**data)

def assignment_score(data: typing.Dict[str, typing.Any]) -> lms.model.scores.AssignmentScore:
    """
    Create a Canvas assignment score.

    See: https://developerdocs.instructure.com/services/canvas/resources/scores
    """

    # Check for important fields.
    for field in ['id', 'assignment_id', 'user_id']:
        if (field not in data):
            raise ValueError(f"Canvas assignment score is missing '{field}' field.")

    # Modify specific arguments before creation.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')
    data['score'] = lms.util.parse.optional_float(data.get('score', None), 'score')
    data['points_possible'] = lms.util.parse.optional_float(data.get('points_possible', None), 'points_possible')
    data['submission_date'] = lms.backend.canvas.common.parse_timestamp(data.get('submitted_at', None))
    data['graded_date'] = lms.backend.canvas.common.parse_timestamp(data.get('graded_at', None))

    assignment_id = lms.util.parse.required_string(data.get('assignment_id', None), 'assignment_id')
    data['assignment_query'] = lms.model.assignments.AssignmentQuery(id = assignment_id)

    user_id = lms.util.parse.required_string(data.get('user_id', None), 'user_id')
    data['user_query'] = lms.model.users.UserQuery(id = user_id)

    return lms.model.scores.AssignmentScore(**data)

def course(data: typing.Dict[str, typing.Any]) -> lms.model.courses.Course:
    """
    Create a Canvas course.

    See: https://developerdocs.instructure.com/services/canvas/resources/courses
    """

    # Check for important fields.
    for field in ['id']:
        if (field not in data):
            raise ValueError(f"Canvas course is missing '{field}' field.")

    # Modify specific arguments before creation.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')

    return lms.model.courses.Course(**data)

def course_user(backend: lms.model.backend.APIBackend, data: typing.Dict[str, typing.Any]) -> lms.model.users.CourseUser:
    """
    Create a Canvas user associated with a course.

    See: https://developerdocs.instructure.com/services/canvas/resources/users
    """

    # Check for important fields.
    for field in ['id']:
        if (field not in data):
            raise ValueError(f"Canvas user is missing '{field}' field.")

    # Modify specific arguments before sending them to super.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')

    # Canvas sometimes has email under different fields.
    if ((data.get('email', None) is None) or (len(data.get('email', '')) == 0)):
        data['email'] = data.get('login_id', None)

    enrollments = data.get('enrollments', None)
    if (enrollments is not None):
        data['raw_role'] = _parse_role_from_enrollments(enrollments)
        data['role'] = ENROLLMENT_TYPE_TO_ROLE.get(data['raw_role'], None)

        # Canvas has a discontinuity with its default course roles.
        # We need to patch this during testing.
        if ((backend.is_testing() or _testing_override) and data['email'] == 'course-admin@test.edulinq.org'):
            data['role'] = lms.model.users.CourseRole.ADMIN

    return lms.model.users.CourseUser(**data)

def group(data: typing.Dict[str, typing.Any]) -> lms.model.groups.Group:
    """
    Create a Canvas group associated with a course.

    See: https://developerdocs.instructure.com/services/canvas/resources/groups
    """

    # Check for important fields.
    for field in ['id']:
        if (field not in data):
            raise ValueError(f"Canvas group is missing '{field}' field.")

    # Modify specific arguments before creation.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')

    return lms.model.groups.Group(**data)

def group_set(data: typing.Dict[str, typing.Any]) -> lms.model.groupsets.GroupSet:
    """
    Create a Canvas group set associated with a course.

    See: https://developerdocs.instructure.com/services/canvas/resources/group_categories
    """

    # Check for important fields.
    for field in ['id']:
        if (field not in data):
            raise ValueError(f"Canvas group set is missing '{field}' field.")

    # Modify specific arguments before creation.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')

    return lms.model.groupsets.GroupSet(**data)

def _parse_role_from_enrollments(enrollments: typing.Any) -> typing.Union[str, None]:
    """
    Try to parse the user's role from their enrollments.
    If multiple roles are discovered, take the "highest" one.

    See: https://developerdocs.instructure.com/services/canvas/resources/enrollments
    """

    if (not isinstance(enrollments, list)):
        return None

    best_role = None
    best_index = -1

    enrollment_types = list(ENROLLMENT_TYPE_TO_ROLE.keys())

    for enrollment in enrollments:
        if (not isinstance(enrollment, dict)):
            continue

        if (enrollment.get('enrollment_state', None) != 'active'):
            continue

        role = enrollment.get('role', None)

        role_index = -1
        if (role in enrollment_types):
            role_index = enrollment_types.index(role)

        if ((best_role is None) or (role_index > best_index)):
            best_role = role
            best_index = role_index

    return best_role
