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
