import lms.backend.testing
import lms.model.testdata.scores

def test_courses_assignments_scores_upload_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of uploading assignments scores. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
                'scores': {
                    '6': lms.model.scores.ScoreFragment(score = 1.0),
                },
            },
            1,
            None,
        ),

        # Empty
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
                'scores': {
                    '6': lms.model.scores.ScoreFragment(),
                },
            },
            1,
            None,
        ),

        # Comment
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
                'scores': {
                    '6': lms.model.scores.ScoreFragment(score = 1.0, comment = 'foo'),
                },
            },
            1,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_scores_upload, test_cases)
