import typing

import lms.backend.canvas.courses.users.list
import lms.model.backend
import lms.model.users

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
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json+canvas-string-ids",
        }

    def courses_users_list(self,
            course_id: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> typing.List[lms.model.users.CourseUser]:
        # TEST - Common validation
        parsed_course_id = int(course_id)

        return lms.backend.canvas.courses.users.list.request(self, parsed_course_id)
