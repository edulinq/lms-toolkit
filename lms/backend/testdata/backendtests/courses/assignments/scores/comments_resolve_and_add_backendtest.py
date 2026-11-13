import typing

import lms.backend.testing
import lms.model.assignments
import lms.model.courses
import lms.model.users

def test_courses_assignments_scores_comments_resolve_and_add_base(test: lms.backend.testing.BackendTest) -> None:
    """ Resolve names and reject missing users before a write. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        # Queries
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'assignment_query': lms.model.assignments.AssignmentQuery(name = 'Homework 0'),
                'user_query': lms.model.users.UserQuery(name = 'course-student'),
                'comment': 'Feedback without a grade change.',
            },
            True,
            None,
        ),

        # Miss - User
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'assignment_query': lms.model.assignments.AssignmentQuery(name = 'Homework 0'),
                'user_query': lms.model.users.UserQuery(id = '999'),
                'comment': 'Feedback without a grade change.',
            },
            None,
            'Could not resolve user query:',
        ),
    ]

    test.base_request_test(test.get_backend().courses_assignments_scores_comments_resolve_and_add, test_cases)
