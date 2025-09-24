import lms.api.testing
import lms.api.assignment.fetch
import lms.api.assignment.testing

class AssignmentFetchTest(lms.api.testing.HTTPTest):
    """ Test fetching course assignments. """

    def test_assignment_fetch_base(self):
        """ Test the base functionality of fetching assignments. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Empty

            (
                {},
                [],
                None,
            ),

            # Base

            (
                {
                    'assignments': ['67890'],
                },
                [
                    lms.api.assignment.testing.ASSIGNMENTS['67890'],
                ],
                None,
            ),

            (
                {
                    'assignments': ['Assignment 1'],
                },
                [
                    lms.api.assignment.testing.ASSIGNMENTS['67890'],
                ],
                None,
            ),

            (
                {
                    'assignments': ['Assignment 1 (67890)'],
                },
                [
                    lms.api.assignment.testing.ASSIGNMENTS['67890'],
                ],
                None,
            ),

            # Multiple

            (
                {
                    'assignments': [
                        '67890',
                        'ZZZ',
                    ],
                },
                [
                    lms.api.assignment.testing.ASSIGNMENTS['67890'],
                ],
                None,
            ),

            (
                {
                    'assignments': [
                        '67890',
                        'Quiz 1'
                    ],
                },
                [
                    lms.api.assignment.testing.ASSIGNMENTS['67890'],
                    lms.api.assignment.testing.ASSIGNMENTS['67891'],
                ],
                None,
            ),
        ]

        self.base_request_test(lms.api.assignment.fetch.request, test_cases)
