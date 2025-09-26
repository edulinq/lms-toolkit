import typing

import lms.model.assignments
import lms.model.users

BACKEND_TYPE_CANVAS: str = 'canvas'
BACKEND_TYPES: typing.List[str] = [
    BACKEND_TYPE_CANVAS,
]

class APIBackend():
    """
    API backends provide a unified interface to an LMS.

    Note that instead of using an abstract class,
    methods will raise a NotImplementedError by default.
    This will allow child backends to fill in as much functionality as they can,
    while still leaving gaps where they are incomplete or impossible.
    """

    def __init__(self,
            server: str,
            **kwargs: typing.Any) -> None:
        self.server: str = server
        """ The server this backend will connect to. """

    def courses_users_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.users.CourseUser]:
        """
        Get the users associated with the given course.
        """

        raise NotImplementedError('courses_users_list')

    def courses_assignments_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.assignments.Assignment]:
        """
        Get the assignments associated with the given course.
        """

        raise NotImplementedError('courses_assignments_list')

    def validate_string(self, raw_value: typing.Any, name: str, strip: bool = True) -> str:
        """ Validate and clean a string parameter. """

        if (raw_value is None):
            raise ValueError(f"Parameter '{name}' is None, when it should be a string.")

        value = str(raw_value)

        if (strip):
            value = value.strip()

        return value

    def validate_int(self, raw_value: typing.Any, name: str) -> int:
        """ Validate and clean an int parameter. """

        if (raw_value is None):
            raise ValueError(f"Parameter '{name}' is None, when it should be an int.")

        return int(raw_value)
