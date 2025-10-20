# pylint: disable=abstract-method

import typing

import lms.backend.canvas.courses.assignments.list
import lms.backend.canvas.courses.assignments.scores.list
import lms.backend.canvas.courses.gradebook.fetch
import lms.backend.canvas.courses.list
import lms.backend.canvas.courses.users.list
import lms.backend.canvas.courses.users.scores.list
import lms.model.assignments
import lms.model.courses
import lms.model.backend
import lms.model.scores
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

    def courses_list(self,
            **kwargs: typing.Any) -> typing.Sequence[lms.model.courses.Course]:
        return lms.backend.canvas.courses.list.request(self)

    def courses_assignments_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.Sequence[lms.model.assignments.Assignment]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        return lms.backend.canvas.courses.assignments.list.request(self, parsed_course_id)

    def courses_assignments_scores_list(self,
            course_id: str,
            assignment_id: str,
            **kwargs: typing.Any) -> typing.Sequence[lms.model.scores.AssignmentScore]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_assignment_id = lms.util.parse.required_int(assignment_id, 'assignment_id')
        return lms.backend.canvas.courses.assignments.scores.list.request(self, parsed_course_id, parsed_assignment_id)

    def courses_gradebook_fetch(self,
            course_id: str,
            assignment_ids: typing.List[str],
            user_ids: typing.List[str],
            **kwargs: typing.Any) -> lms.model.scores.Gradebook:
        if ((len(assignment_ids) == 0) or (len(user_ids) == 0)):
            assignment_queries = [lms.model.assignments.AssignmentQuery(id = id) for id in assignment_ids]
            user_queries = [lms.model.users.UserQuery(id = id) for id in user_ids]
            return lms.model.scores.Gradebook(assignment_queries, user_queries)

        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_assignment_ids = [lms.util.parse.required_int(assignment_id, 'assignment_id') for assignment_id in assignment_ids]
        parsed_user_ids = [lms.util.parse.required_int(user_id, 'user_id') for user_id in user_ids]

        return lms.backend.canvas.courses.gradebook.fetch.request(self, parsed_course_id, parsed_assignment_ids, parsed_user_ids)

    def courses_users_list(self,
            course_id: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> typing.Sequence[lms.model.users.CourseUser]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        return lms.backend.canvas.courses.users.list.request(self, parsed_course_id)

    def courses_users_scores_list(self,
            course_id: str,
            user_id: str,
            **kwargs: typing.Any) -> typing.Sequence[lms.model.scores.AssignmentScore]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_user_id = lms.util.parse.required_int(user_id, 'user_id')
        return lms.backend.canvas.courses.users.scores.list.request(self, parsed_course_id, parsed_user_id)
