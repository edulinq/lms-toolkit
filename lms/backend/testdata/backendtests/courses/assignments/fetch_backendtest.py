import typing

import lms.backend.testing
import lms.model.testdata.assignments

def test_courses_assignments_fetch_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of fetching course assignments. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        # Base
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
            },
            lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course 101']['Homework 0'],
            None,
        ),

        # Miss
        (
            {
                'course_id': '110000000',
                'assignment_id': '999',
            },
            None,
            None,
        ),
    ]

    test.base_request_test(test.get_backend().courses_assignments_fetch, test_cases)
