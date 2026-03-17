import lms.backend.testing
import lms.model.testdata.quizzes

def test_courses_quizzes_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course quizzes. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_id': '110000000',
            },
            [
                lms.model.testdata.quizzes.COURSE_QUIZZES['Course 101']['Regular Expressions'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_quizzes_list, test_cases)
