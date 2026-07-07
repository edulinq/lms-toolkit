import typing

import lms.backend.testing
import lms.model.testdata.courses

def test_courses_list_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of listing courses. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        (
            {},
            [
                lms.model.testdata.courses.COURSES['Course 101'],
                lms.model.testdata.courses.COURSES['Course Using Different Languages'],
                lms.model.testdata.courses.COURSES['Extra Course'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.get_backend().courses_list, test_cases)
