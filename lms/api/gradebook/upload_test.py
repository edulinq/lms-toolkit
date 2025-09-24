import copy

import lms.api.testing
import lms.api.gradebook.upload
import lms.api.gradebook.testing

class GradebookUploadTest(lms.api.testing.HTTPTest):
    """ Test uploading course gradebooks. """

    def test_gradebook_upload_base(self):
        """ Test the base functionality of uploading gradebooks. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Empty

            (
                {},
                0,
                None,
            ),

            # Base

            (
                {
                    'assignments': ['67890'],
                    'users': ['10001'],
                    'scores': [[1.0]],
                },
                1,
                None,
            ),

            # Multiple

            (
                {
                    'assignments': ['67890'],
                    'users': ['10001', '10002'],
                    'scores': [[1.0], [0.0]],
                },
                2,
                None,
            ),

            (
                {
                    'assignments': ['67890', '67891'],
                    'users': ['10001'],
                    'scores': [[1.0, 1.0]],
                },
                2,
                None,
            ),

            (
                {
                    'assignments': ['67890', '67891'],
                    'users': ['10001', '10002'],
                    'scores': [[1.0, 1.0], [0.0, 0.0]],
                },
                4,
                None,
            ),

            # Missing

            (
                {
                    'assignments': ['67890', '67891'],
                    'users': ['10001'],
                    'scores': [[None, None]],
                },
                0,
                None,
            ),

            (
                {
                    'assignments': ['67890'],
                    'users': ['10001', '10002'],
                    'scores': [[None], [None]],
                },
                0,
                None,
            ),

            (
                {
                    'assignments': ['67890', '67891'],
                    'users': ['10001', '10002'],
                    'scores': [[1.0, None], [0.0, None]],
                },
                2,
                None,
            ),

            # Errors

            (
                {
                    'assignments': ['67890'],
                    'users': ['10001'],
                    'scores': [[1.0], [0.0]],
                },
                None,
                'does not match the number of users',
            ),

            (
                {
                    'assignments': ['67890'],
                    'users': ['10001'],
                    'scores': [[1.0, 1.0]],
                },
                None,
                'does not match the number of assignment',
            ),

            (
                {
                    'assignments': ['67890', 'Assignment 1'],
                    'users': ['10001'],
                    'scores': [[1.0, 1.0]],
                },
                None,
                'Found duplicates in assignments',
            ),

            (
                {
                    'assignments': ['67890'],
                    'users': ['Alice Alvarez', 'aalvarez@ucsc.edu'],
                    'scores': [[1.0], [1.0]],
                },
                None,
                'Found duplicates in users',
            ),

            (
                {
                    'assignments': ['ZZZ'],
                    'users': ['10001'],
                    'scores': [[1.0]],
                },
                None,
                'Unable to resolve all assignment queries',
            ),

            (
                {
                    'assignments': ['67890'],
                    'users': ['ZZZ'],
                    'scores': [[1.0]],
                },
                None,
                'Unable to resolve all user queries',
            ),
        ]

        self.base_request_test(lms.api.gradebook.upload.request, test_cases)
