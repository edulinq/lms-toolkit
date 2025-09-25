import typing

import lms.model.users

CORE_FIELDS: typing.List[str] = [
    'id',
    'email',
]

class CourseUser(lms.model.users.CourseUser):
    """
    A Canvas user associated with a course.

    Common fields will be held in lms.model.users.CourseUser.
    Fields that are not common, but used by this backend will be explicitly listed.
    Other fields coming from Canvas will be held in lms.model.users.CourseUser.extra_fields.

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
        kwargs['id'] = str(kwargs['id'])
        kwargs['username'] = kwargs.get('login_id', None)

        super().__init__(**kwargs)

        # TODO(eriq) - Resolve type.
        self.enrollments: typing.Union[typing.Any, None] = enrollments
        """
        This field can be requested with certain API calls, and will return a list of the users active enrollments.
        See the List enrollments API for more details about the format of these records.
        """
