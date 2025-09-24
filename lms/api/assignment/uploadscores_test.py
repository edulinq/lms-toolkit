import lms.api.testing
import lms.api.assignment.uploadscores

class AssignmentUploadScoresTest(lms.api.testing.HTTPTest):
    """ Test uploading assignment scores. """

    def test_assignment_upload_scores_base(self):
        """ Test the base functionality of uploading assignment scores. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Base

            (
                {
                    'assignment': '67890',
                    'users': ['10001'],
                    'scores': [1.0],
                    'comments': [''],
                },
                1,
                None,
            ),

            # Resolution

            (
                {
                    'assignment': 'Assignment 1',
                    'users': ['10001'],
                    'scores': [1.0],
                    'comments': [''],
                },
                1,
                None,
            ),

            (
                {
                    'assignment': '67890',
                    'users': ['aalvarez@ucsc.edu'],
                    'scores': [1.0],
                    'comments': [''],
                },
                1,
                None,
            ),

            (
                {
                    'assignment': 'Assignment 1 (67890)',
                    'users': ['Alice Alvarez'],
                    'scores': [1.0],
                    'comments': [''],
                },
                1,
                None,
            ),

            # Multiple

            (
                {
                    'assignment': '67890',
                    'users': ['10001', '10002'],
                    'scores': [1.0, 0.0],
                    'comments': ['foo', 'bar'],
                },
                2,
                None,
            ),

            (
                {
                    'assignment': 'Assignment 1',
                    'users': ['aalvarez@ucsc.edu', 'Bob Burnquist'],
                    'scores': [1.0, 0.0],
                    'comments': ['foo', 'bar'],
                },
                2,
                None,
            ),

            # Errors

            (
                {
                    'assignment': '67890',
                    'users': ['10001'],
                    'scores': [1.0],
                },
                None,
                'Mismatched count',
            ),
        ]

        self.base_request_test(lms.api.assignment.uploadscores.request, test_cases)
