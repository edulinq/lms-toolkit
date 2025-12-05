# pylint: disable=abstract-method

import typing

import lms.backend.canvas.courses.assignments.list
import lms.backend.canvas.courses.assignments.scores.list
import lms.backend.canvas.courses.assignments.scores.upload
import lms.backend.canvas.courses.gradebook.fetch
import lms.backend.canvas.courses.groupsets.create
import lms.backend.canvas.courses.groupsets.delete
import lms.backend.canvas.courses.groupsets.list
import lms.backend.canvas.courses.groupsets.memberships.list
import lms.backend.canvas.courses.groups.create
import lms.backend.canvas.courses.groups.delete
import lms.backend.canvas.courses.groups.list
import lms.backend.canvas.courses.groups.memberships.add
import lms.backend.canvas.courses.groups.memberships.list
import lms.backend.canvas.courses.groups.memberships.subtract
import lms.backend.canvas.courses.list
import lms.backend.canvas.courses.syllabus.fetch
import lms.backend.canvas.courses.users.list
import lms.backend.canvas.courses.users.scores.list
import lms.model.assignments
import lms.model.backend
import lms.model.constants
import lms.model.courses
import lms.model.groups
import lms.model.groupsets
import lms.model.scores
import lms.model.users
import lms.util.parse

class CanvasBackend(lms.model.backend.APIBackend):
    """ An API backend for Instructure's Canvas LMS. """

    def __init__(self,
            server: str,
            auth_token: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(server, lms.model.constants.BACKEND_TYPE_CANVAS, **kwargs)

        if (auth_token is None):
            raise ValueError("Canvas backends require a token.")

        self.auth_token: str = auth_token
        """ The token to authenticate with. """

    def get_standard_headers(self) -> typing.Dict[str, str]:
        headers = super().get_standard_headers()

        headers['Authorization'] = f"Bearer {self.auth_token}"

        return headers

    def courses_list(self,
            **kwargs: typing.Any) -> typing.List[lms.model.courses.Course]:
        return lms.backend.canvas.courses.list.request(self)

    def courses_assignments_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.assignments.Assignment]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        return lms.backend.canvas.courses.assignments.list.request(self, parsed_course_id)

    def courses_assignments_scores_list(self,
            course_id: str,
            assignment_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.scores.AssignmentScore]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_assignment_id = lms.util.parse.required_int(assignment_id, 'assignment_id')
        return lms.backend.canvas.courses.assignments.scores.list.request(self, parsed_course_id, parsed_assignment_id)

    def courses_assignments_scores_upload(self,
            course_id: str,
            assignment_id: str,
            scores: typing.Dict[str, lms.model.scores.ScoreFragment],
            **kwargs: typing.Any) -> int:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_assignment_id = lms.util.parse.required_int(assignment_id, 'assignment_id')
        parsed_scores = {lms.util.parse.required_int(user_id, 'user_id'): score for (user_id, score) in scores.items()}
        return lms.backend.canvas.courses.assignments.scores.upload.request(self, parsed_course_id, parsed_assignment_id, parsed_scores)

    def courses_gradebook_fetch(self,
            course_id: str,
            assignment_ids: typing.Collection[str],
            user_ids: typing.Collection[str],
            **kwargs: typing.Any) -> lms.model.scores.Gradebook:
        if ((len(assignment_ids) == 0) or (len(user_ids) == 0)):
            assignment_queries = [lms.model.assignments.AssignmentQuery(id = id) for id in assignment_ids]
            user_queries = [lms.model.users.UserQuery(id = id) for id in user_ids]
            return lms.model.scores.Gradebook(assignment_queries, user_queries)

        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_assignment_ids = [lms.util.parse.required_int(assignment_id, 'assignment_id') for assignment_id in assignment_ids]
        parsed_user_ids = [lms.util.parse.required_int(user_id, 'user_id') for user_id in user_ids]

        return lms.backend.canvas.courses.gradebook.fetch.request(self, parsed_course_id, parsed_assignment_ids, parsed_user_ids)

    def courses_groupsets_create(self,
            course_id: str,
            name: str,
            **kwargs: typing.Any) -> lms.model.groupsets.GroupSet:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        return lms.backend.canvas.courses.groupsets.create.request(self, parsed_course_id, name)

    def courses_groupsets_delete(self,
            course_id: str,
            groupset_id: str,
            **kwargs: typing.Any) -> bool:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_groupset_id = lms.util.parse.required_int(groupset_id, 'groupset_id')
        return lms.backend.canvas.courses.groupsets.delete.request(self, parsed_course_id, parsed_groupset_id)

    def courses_groupsets_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.groupsets.GroupSet]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        return lms.backend.canvas.courses.groupsets.list.request(self, parsed_course_id)

    def courses_groupsets_memberships_list(self,
            course_id: str,
            groupset_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.groupsets.GroupSetMembership]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_groupset_id = lms.util.parse.required_int(groupset_id, 'groupset_id')
        return lms.backend.canvas.courses.groupsets.memberships.list.request(self, parsed_course_id, parsed_groupset_id)

    def courses_groups_create(self,
            course_id: str,
            groupset_id: str,
            name: str,
            **kwargs: typing.Any) -> lms.model.groups.Group:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_groupset_id = lms.util.parse.required_int(groupset_id, 'groupset_id')
        return lms.backend.canvas.courses.groups.create.request(self, parsed_course_id, parsed_groupset_id, name)

    def courses_groups_delete(self,
            course_id: str,
            groupset_id: str,
            group_id: str,
            **kwargs: typing.Any) -> bool:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_groupset_id = lms.util.parse.required_int(groupset_id, 'groupset_id')
        parsed_group_id = lms.util.parse.required_int(group_id, 'group_id')
        return lms.backend.canvas.courses.groups.delete.request(self, parsed_course_id, parsed_groupset_id, parsed_group_id)

    def courses_groups_list(self,
            course_id: str,
            groupset_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.groups.Group]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_groupset_id = lms.util.parse.required_int(groupset_id, 'groupset_id')
        return lms.backend.canvas.courses.groups.list.request(self, parsed_course_id, parsed_groupset_id)

    def courses_groups_memberships_add(self,
            course_id: str,
            groupset_id: str,
            group_id: str,
            user_ids: typing.Collection[str],
            **kwargs: typing.Any) -> int:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_groupset_id = lms.util.parse.required_int(groupset_id, 'groupset_id')
        parsed_group_id = lms.util.parse.required_int(group_id, 'group_id')
        parsed_user_ids = [lms.util.parse.required_int(user_id, 'user_id') for user_id in user_ids]
        return lms.backend.canvas.courses.groups.memberships.add.request(self, parsed_course_id, parsed_groupset_id, parsed_group_id, parsed_user_ids)

    def courses_groups_memberships_list(self,
            course_id: str,
            groupset_id: str,
            group_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.groupsets.GroupSetMembership]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_groupset_id = lms.util.parse.required_int(groupset_id, 'groupset_id')
        parsed_group_id = lms.util.parse.required_int(group_id, 'group_id')
        return lms.backend.canvas.courses.groups.memberships.list.request(self, parsed_course_id, parsed_groupset_id, parsed_group_id)

    def courses_groups_memberships_subtract(self,
            course_id: str,
            groupset_id: str,
            group_id: str,
            user_ids: typing.Collection[str],
            **kwargs: typing.Any) -> int:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_groupset_id = lms.util.parse.required_int(groupset_id, 'groupset_id')
        parsed_group_id = lms.util.parse.required_int(group_id, 'group_id')
        parsed_user_ids = [lms.util.parse.required_int(user_id, 'user_id') for user_id in user_ids]
        return lms.backend.canvas.courses.groups.memberships.subtract.request(self,
                parsed_course_id, parsed_groupset_id, parsed_group_id, parsed_user_ids)

    def courses_syllabus_fetch(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.Union[str, None]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        return lms.backend.canvas.courses.syllabus.fetch.request(self, parsed_course_id)

    def courses_users_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.users.CourseUser]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        return lms.backend.canvas.courses.users.list.request(self, parsed_course_id)

    def courses_users_scores_list(self,
            course_id: str,
            user_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.scores.AssignmentScore]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')
        parsed_user_id = lms.util.parse.required_int(user_id, 'user_id')
        return lms.backend.canvas.courses.users.scores.list.request(self, parsed_course_id, parsed_user_id)
