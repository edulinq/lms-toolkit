import copy

import lms.api.testing
import lms.api.gradebook.fetch
import lms.api.gradebook.testing

class GradebookFetchTest(lms.api.testing.HTTPTest):
    """ Test fetching course gradebooks. """

    def test_gradebook_fetch_base(self):
        """ Test the base functionality of fetching gradebooks. """

        one_count_assignments = copy.deepcopy(lms.api.gradebook.testing.GRADEBOOK_ASSIGNMENTS)
        for info in one_count_assignments.values():
            info['count'] = max(0, info['count'] - 1)

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Empty / All

            (
                {},
                (
                    lms.api.gradebook.testing.GRADEBOOK_ASSIGNMENTS,
                    lms.api.gradebook.testing.GRADEBOOK_GRADES,
                ),
                None,
            ),

            # Users

            (
                {
                    'user_queries': [
                        '10001',
                    ]
                },
                (
                    one_count_assignments,
                    {'aalvarez@ucsc.edu': lms.api.gradebook.testing.GRADEBOOK_GRADES['aalvarez@ucsc.edu']},
                ),
                None,
            ),

            (
                {
                    'user_queries': [
                        'aalvarez@ucsc.edu',
                    ]
                },
                (
                    one_count_assignments,
                    {'aalvarez@ucsc.edu': lms.api.gradebook.testing.GRADEBOOK_GRADES['aalvarez@ucsc.edu']},
                ),
                None,
            ),

            (
                {
                    'user_queries': [
                        'aalvarez@ucsc.edu (10001)',
                    ]
                },
                (
                    one_count_assignments,
                    {'aalvarez@ucsc.edu': lms.api.gradebook.testing.GRADEBOOK_GRADES['aalvarez@ucsc.edu']},
                ),
                None,
            ),

            (
                {
                    'user_queries': [
                        'Alice Alvarez',
                    ]
                },
                (
                    one_count_assignments,
                    {'aalvarez@ucsc.edu': lms.api.gradebook.testing.GRADEBOOK_GRADES['aalvarez@ucsc.edu']},
                ),
                None,
            ),

            (
                {
                    'user_queries': [
                        'Alice Alvarez',
                        'ZZZ',
                    ]
                },
                (
                    one_count_assignments,
                    {'aalvarez@ucsc.edu': lms.api.gradebook.testing.GRADEBOOK_GRADES['aalvarez@ucsc.edu']},
                ),
                None,
            ),

            (
                {
                    'user_queries': [
                        'Alice Alvarez',
                        '10002',
                    ]
                },
                (
                    lms.api.gradebook.testing.GRADEBOOK_ASSIGNMENTS,
                    lms.api.gradebook.testing.GRADEBOOK_GRADES,
                ),
                None,
            ),

            # Errors

            (
                {
                    'user_queries': [
                        'ZZZ',
                    ]
                },
                None,
                'Could not find any users for the gradebook',
            ),
        ]

        self.base_request_test(lms.api.gradebook.fetch.request, test_cases)
