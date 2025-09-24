import lms.api.testing
import lms.api.user.fetch
import lms.api.user.testing

class UserGetTest(lms.api.testing.HTTPTest):
    """ Test getting course users. """

    def test_user_get_base(self):
        """ Test the base functionality of fetching a user. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Empty

            (
                {
                    'users': [],
                },
                [],
                None,
            ),

            # Base

            (
                {
                    'users': ['10001'],
                },
                [lms.api.user.testing.USERS['10001']],
                None,
            ),

            (
                {
                    'users': ['10001'],
                },
                [lms.api.user.testing.USERS['10001']],
                None,
            ),

            (
                {
                    'users': ['aalvarez@ucsc.edu'],
                },
                [lms.api.user.testing.USERS['10001']],
                None,
            ),

            (
                {
                    'users': ['aalvarez@ucsc.edu (10001)'],
                },
                [lms.api.user.testing.USERS['10001']],
                None,
            ),

            (
                {
                    'users': ['Alice Alvarez'],
                },
                [lms.api.user.testing.USERS['10001']],
                None,
            ),

            # Missing

            (
                {
                    'users': ['ZZZ'],
                },
                [],
                None,
            ),

            # Multiple

            (
                {
                    'users': [
                        '10001',
                        '10002',
                    ],
                },
                [
                    lms.api.user.testing.USERS['10001'],
                    lms.api.user.testing.USERS['10002'],
                ],
                None,
            ),

            (
                {
                    'users': [
                        'aalvarez@ucsc.edu',
                        '10002',
                    ],
                },
                [
                    lms.api.user.testing.USERS['10001'],
                    lms.api.user.testing.USERS['10002'],
                ],
                None,
            ),

            (
                {
                    'users': [
                        '10001',
                        'bburnquist@ucsc.edu (10002)',
                    ],
                },
                [
                    lms.api.user.testing.USERS['10001'],
                    lms.api.user.testing.USERS['10002'],
                ],
                None,
            ),

            (
                {
                    'users': [
                        'Alice Alvarez',
                        '10002',
                    ],
                },
                [
                    lms.api.user.testing.USERS['10001'],
                    lms.api.user.testing.USERS['10002'],
                ],
                None,
            ),

            (
                {
                    'users': [
                        '10001',
                        'ZZZ',
                    ],
                },
                [
                    lms.api.user.testing.USERS['10001'],
                ],
                None,
            ),
        ]

        self.base_request_test(lms.api.user.fetch.request, test_cases)
