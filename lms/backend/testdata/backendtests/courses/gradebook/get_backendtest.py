import lms.backend.testing
import lms.model.assignments
import lms.model.scores
import lms.model.testdata.scores
import lms.model.users

def test_courses_gradebook_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting a course's gradebook. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES_RESOLVED

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '1',
                'assignment_queries': lms.model.testdata.scores.COURSE_GRADEBOOKS_RESOLVED['Course 101'].assignments,
                'user_queries': lms.model.testdata.scores.COURSE_GRADEBOOKS_RESOLVED['Course 101'].users,
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS_RESOLVED['Course 101'],
            None,
        ),

        # No Queries
        (
            {
                'course_id': '1',
                'assignment_queries': [],
                'user_queries': [],
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS_RESOLVED['Course 101'],
            None,
        ),

        # Miss
        (
            {
                'course_id': '999',
                'assignment_queries': [],
                'user_queries': [],
            },
            lms.model.scores.Gradebook([], []),
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_gradebook_get, test_cases)
