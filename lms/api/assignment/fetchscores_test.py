import lms.api.testing
import lms.api.assignment.fetchscores
import lms.api.assignment.testing

class AssignmentFetchScoresTest(lms.api.testing.HTTPTest):
    """ Test fetching assignment scores. """

    def test_assignment_fetch_scores_base(self):
        """ Test the base functionality of fetching assignment scores. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            (
                {
                    'assignment': '67890',
                },
                [
                    lms.api.assignment.testing.SCORES['67890']['10001'],
                    lms.api.assignment.testing.SCORES['67890']['10002'],
                ],
                None,
            ),

            (
                {
                    'assignment': 'Assignment 1',
                },
                [
                    lms.api.assignment.testing.SCORES['67890']['10001'],
                    lms.api.assignment.testing.SCORES['67890']['10002'],
                ],
                None,
            ),
        ]

        self.base_request_test(lms.api.assignment.fetchscores.request, test_cases)
