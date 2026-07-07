import typing

import lms.backend.testing
import lms.model.testdata.courses

def test_courses_fetch_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of fetching courses. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        # Base
        (
            {
                'course_id': '110000000',
            },
            lms.model.testdata.courses.COURSES['Course 101'],
            None,
        ),

        # Miss
        (
            {
                'course_id': '999',
            },
            None,
            None,
        ),
    ]

    test.base_request_test(test.get_backend().courses_fetch, test_cases)
