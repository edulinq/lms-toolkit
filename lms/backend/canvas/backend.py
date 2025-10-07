import typing

import lms.backend.canvas.courses.assignments.fetch
import lms.backend.canvas.courses.assignments.list
import lms.backend.canvas.courses.users.fetch
import lms.backend.canvas.courses.users.list
import lms.model.assignments
import lms.model.backend
import lms.model.users
import lms.util.parse

class CanvasBackend(lms.model.backend.APIBackend):
    """ An API backend for Instructure's Canvas LMS. """

    def __init__(self,
            server: str,
            token: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(server, **kwargs)

        if (token is None):
            raise ValueError("Canvas backends require a token.")

        self.token: str = token

    def get_standard_headers(self) -> typing.Dict[str, str]:
        """ Get standard Canvas headers. """

        return {
            "Authorization": f"Bearer {self.token}",
        }

    def courses_assignments_fetch(self,
            course_id: str,
            assignment_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.assignments.Assignment, None]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_assignment_id = lms.util.parse.required_int(assignment_id, 'assignment_id')
        return lms.backend.canvas.courses.assignments.fetch.request(self, parsed_course_id, parsed_assignment_id)

    def courses_assignments_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.Sequence[lms.model.assignments.Assignment]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        return lms.backend.canvas.courses.assignments.list.request(self, parsed_course_id)

    def courses_users_fetch(self,
            course_id: str,
            user_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.users.CourseUser, None]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_user_id = lms.util.parse.required_int(user_id, 'user_id')
        return lms.backend.canvas.courses.users.fetch.request(self, parsed_course_id, parsed_user_id)

    def courses_users_list(self,
            course_id: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> typing.Sequence[lms.model.users.CourseUser]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        return lms.backend.canvas.courses.users.list.request(self, parsed_course_id)
