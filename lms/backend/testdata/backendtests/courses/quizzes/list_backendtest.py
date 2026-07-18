import typing

import lms.backend.testing
import lms.model.testdata.quizzes

def test_courses_quizzes_list_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of listing course quizzes. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        (
            {
                'course_id': '110000000',
            },
            [
                lms.model.testdata.quizzes.COURSE_QUIZZES_METADATA['Course 101']['Regular Expressions'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.get_backend().courses_quizzes_list, test_cases)
