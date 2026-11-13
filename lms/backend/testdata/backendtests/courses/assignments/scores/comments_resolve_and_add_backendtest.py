import typing

import lms.backend.testing
import lms.model.assignments
import lms.model.courses
import lms.model.testdata.assignments
import lms.model.testdata.courses
import lms.model.testdata.users
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

def test_courses_assignments_scores_comments_resolve_and_add_permissions(test: lms.backend.testing.BackendTest) -> None:
    """ Check the authenticated user's access, including already resolved targets. """

    other_submission = {
        'course_query': lms.model.testdata.courses.COURSES['Extra Course'].to_query(),
        'assignment_query': lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 1'].to_query(),
        'user_query': lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-1'].to_query(),
        'comment': 'Feedback without a grade change.',
    }

    # [(auth user, kwargs, expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[str, typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        # The owner can comment on this existing submission.
        ('course-owner', other_submission, True, None),

        # A student can comment on their own submission.
        (
            'course-student',
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'assignment_query': lms.model.assignments.AssignmentQuery(name = 'Homework 0'),
                'user_query': lms.model.users.UserQuery(name = 'course-student'),
                'comment': 'Feedback without a grade change.',
            },
            True,
            None,
        ),

        # The other student's submission is in a course this student cannot access.
        ('course-student', other_submission, False, None),

        # A grader cannot resolve a course in which they are not enrolled.
        (
            'course-grader',
            dict(other_submission, course_query = lms.model.courses.CourseQuery(name = 'Extra Course')),
            None,
            'Could not resolve course query:',
        ),

        # Already resolved queries must not bypass the LMS's authorization.
        ('course-grader', other_submission, False, None),
        ('course-admin', other_submission, False, None),
    ]

    try:
        for (user, kwargs, expected, error_substring) in test_cases:
            with test.subTest(user = user, course = str(kwargs['course_query'])):
                test.set_user(user + '@test.edulinq.org')
                test.base_request_test(test.get_backend().courses_assignments_scores_comments_resolve_and_add,
                        [(kwargs, expected, error_substring)])
    finally:
        test.clear_user()
