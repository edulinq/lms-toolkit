import lms.backend.testing
import lms.model.scores
import lms.model.testdata.scores

def test_courses_gradebook_fetch_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of fetching a course's gradebook. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES_RESOLVED

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '1',
                'assignment_ids': ['1'],
                'user_ids': ['6'],
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS['Course 101'],
            None,
        ),

        # Empty
        (
            {
                'course_id': '1',
                'assignment_ids': [],
                'user_ids': [],
            },
            lms.model.scores.Gradebook([], []),
            None,
        ),

        # Miss
        (
            {
                'course_id': '999',
                'assignment_ids': [],
                'user_ids': [],
            },
            lms.model.scores.Gradebook([], []),
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_gradebook_fetch, test_cases)
