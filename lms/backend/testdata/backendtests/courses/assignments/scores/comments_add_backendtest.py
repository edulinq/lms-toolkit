import typing

import lms.backend.testing

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
            True,
            None,
        ),

        # Whitespace
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
                'user_id': '100050000',
                'comment': ' \n\t',
            },
            True,
            None,
        ),
    ]

    test.base_request_test(test.get_backend().courses_assignments_scores_comments_add, test_cases)
