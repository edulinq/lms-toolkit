import typing

import lms.backend.testing
import lms.model.assignments
import lms.model.courses
import lms.model.users

def test_courses_assignments_scores_comments_add_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test adding submission comments, including missing targets. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        # Base
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
                'user_id': '100050000',
                'comment': 'Feedback without a grade change.',
            },
            True,
            None,
        ),

        # Miss - Course
        (
            {
                'course_id': '999',
                'assignment_id': '110000100',
                'user_id': '100050000',
                'comment': 'Feedback without a grade change.',
            },
            False,
            None,
        ),

        # Miss - Assignment
        (
            {
                'course_id': '110000000',
                'assignment_id': '999',
                'user_id': '100050000',
                'comment': 'Feedback without a grade change.',
            },
            False,
            None,
        ),

        # Miss - User
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
                'user_id': '999',
                'comment': 'Feedback without a grade change.',
            },
            False,
            None,
        ),

        # Empty
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
                'user_id': '100050000',
                'comment': '',
            },
            None,
            'Comment must not be empty.',
        ),

        # Whitespace
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
                'user_id': '100050000',
                'comment': ' \n\t',
            },
            None,
            'Comment must not be empty.',
        ),
    ]

    test.base_request_test(test.get_backend().courses_assignments_scores_comments_add, test_cases)

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

def test_courses_assignments_scores_comments_preserve_score(test: lms.backend.testing.BackendTest) -> None:
    """ Keep the existing score across a real comment write during fixture generation. """

    def add_and_read(course_id: str, assignment_id: str) -> typing.Tuple[bool, typing.Any, typing.Any]:
        backend = test.get_backend()
        before = backend.courses_assignments_scores_list(course_id, assignment_id)
        added = backend.courses_assignments_scores_comments_add(course_id, assignment_id, '100050000', 'Feedback without a grade change.')
        after = backend.courses_assignments_scores_list(course_id, assignment_id)
        return (added, before[0].score if before else None, after[0].score if after else None)

    # Keep the live server state across the write and subsequent read.
    test.base_request_test(add_and_read, [
        ({'course_id': '110000000', 'assignment_id': '110000100'}, (True, 2.0, 2.0), None),
    ], disable_server_restart = True)
