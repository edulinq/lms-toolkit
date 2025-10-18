import typing

import lms.model.users

CORE_FIELDS: typing.List[str] = [
    'id',
    'email',
]

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

class CourseUser(lms.model.users.CourseUser):
    """
    A Canvas user associated with a course.

    Common fields will be held in lms.model.users.CourseUser.
    Fields that are not common, but used by this backend will be explicitly listed.
    Other fields coming from Canvas will be held in lms.model.base.BaseType.extra_fields.

    See: https://developerdocs.instructure.com/services/canvas/resources/users
    """

    def __init__(self,
            enrollments: typing.Union[typing.Any, None] = None,
            **kwargs: typing.Any) -> None:
        # Check for important fields.
        for field in CORE_FIELDS:
            if (field not in kwargs):
                raise ValueError(f"Canvas user is missing '{field}'.")

        # Modify specific arguments before sending them to super.
        kwargs['id'] = lms.util.parse.required_string(kwargs.get('id', None), 'id')

        if (enrollments is not None):
            kwargs['raw_role'] = self._parse_role_from_enrollments(enrollments)
            kwargs['role'] = ENROLLMENT_TYPE_TO_ROLE.get(kwargs['raw_role'], None)

        super().__init__(**kwargs)

        if (enrollments is None):
            enrollments = []

        if (not isinstance(enrollments, list)):
            raise ValueError(f"Enrollments should be a list of enrollments, found {type(enrollments)}.")

        for (i, enrollment) in enumerate(enrollments):
            if (not isinstance(enrollment, dict)):
                raise ValueError(f"Enrollment at index {i} should be a dict, found {type(enrollment)}.")

        self.enrollments: typing.List[typing.Dict[str, typing.Any]] = enrollments
        """
        This field can be requested with certain API calls, and will return a list of the users active enrollments.
        See the List enrollments API for more details about the format of these records.
        """

    def _parse_role_from_enrollments(self, enrollments: typing.Any) -> typing.Union[str, None]:
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
