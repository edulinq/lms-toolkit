import lms.backend.testing
import lms.model.testdata.scores

def test_courses_assignments_scores_fetch_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of fetching assignments scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '1',
                'assignment_id': '1',
                'user_id': '6',
            },
            scores['Course 101']['Homework 0']['course-student'],
            None,
        ),

        # Miss
        (
            {
                'course_id': '1',
                'assignment_id': '999',
                'user_id': '6',
            },
            None,
            None,
        ),
        (
            {
                'course_id': '1',
                'assignment_id': '1',
                'user_id': '999',
            },
            None,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_scores_fetch, test_cases)
