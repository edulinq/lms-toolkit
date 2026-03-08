import lms.backend.testing
import lms.model.quizzes
import lms.model.testdata.quizzes

def test_courses_quizzes_fetch_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of fetching course quizzes. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
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
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_quizzes_fetch, test_cases)
