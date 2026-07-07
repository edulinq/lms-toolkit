import typing

import lms.backend.testing
import lms.backend.testdata.backendtests.courses.quizzes.common
import lms.model.testdata.quizzes

def test_courses_quizzes_download_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of downloading course quizzes. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        # Base
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
            },
            lms.model.testdata.quizzes.COURSE_QUIZZES['Course 101']['Regular Expressions'],
            None,
        ),

        # Miss
        (
            {
                'course_id': '110000000',
                'quiz_id': '999',
            },
            None,
            'Unable to fetch quiz metadata for quiz ID',
        ),
    ]

    test.base_request_test(test.get_backend().courses_quizzes_download, test_cases,
        actual_clean_func = lms.backend.testdata.backendtests.courses.quizzes.common._sketch_quiz,
        expected_clean_func = lms.backend.testdata.backendtests.courses.quizzes.common._sketch_quiz,
    )
