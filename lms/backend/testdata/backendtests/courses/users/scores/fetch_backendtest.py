import lms.backend.testing
import lms.model.testdata.scores

def test_courses_users_scores_fetch_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of fetching user's scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES_UNRESOLVED

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
                'user_id': '100050000',
            },
            scores['Course 101']['Homework 0']['course-student'],
            None,
        ),

        # Miss
        (
            {
                'course_id': '110000000',
                'assignment_id': '999',
                'user_id': '100050000',
            },
            None,
            None,
        ),
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
                'user_id': '999',
            },
            None,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_scores_fetch, test_cases)
