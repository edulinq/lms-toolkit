import lms.backend.testing
import lms.model.quizzes
import lms.model.testdata.quizzes

def test_courses_quizzes_groups_fetch_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of fetching course quiz questions. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'group_id': '110000201',
            },
            lms.model.testdata.quizzes.QUIZ_GROUPS['Regular Expressions']['Ice Breaker'],
            None,
        ),

        # Miss
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'group_id': '999',
            },
            None,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_quizzes_groups_fetch, test_cases)
