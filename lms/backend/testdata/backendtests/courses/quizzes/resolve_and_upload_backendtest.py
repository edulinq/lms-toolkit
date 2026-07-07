import typing

import quizcomp.model.constants
import quizcomp.model.quiz

import lms.backend.testing
import lms.model.assignments
import lms.model.testdata.quizzes

def test_courses_quizzes_resolve_and_upload_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of resolving and uploading course quizzes. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        # Base
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz': lms.model.testdata.quizzes.COURSE_QUIZZES['Course 101']['Regular Expressions'],
                'force': True,
            },
            'Regular Expressions',
            None,
        ),
    ]

    test.base_request_test(test.get_backend().courses_quizzes_resolve_and_upload, test_cases,
        disable_server_restart = True,
        actual_clean_func = _get_quiz_name,
    )

def _get_quiz_name(raw_quiz_metadata: typing.Any) -> str:
    """ Get the quiz name from the assignment. """

    quiz_metadata = typing.cast(lms.model.assignments.Assignment, raw_quiz_metadata)
    return str(quiz_metadata.name)
