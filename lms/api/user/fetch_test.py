import lms.api.testing
import lms.api.user.fetch

class UserGetTest(lms.api.testing.HTTPTest):
    """ Test getting course users. """

    def test_user_get_base(self):
        """ Test the base functionality of users/get. """

        user_infos = {
            '10001': {
                "email": "aalvarez@ucsc.edu",
                "enrollment": "<unknown>",
                "id": "10001",
                "name": "Alice Alvarez",
                "sis_user_id": "1000001"
            },
            '10002': {
                "email": "bburnquist@ucsc.edu",
                "enrollment": "<unknown>",
                "id": "10002",
                "name": "Bob Burnquist",
                "sis_user_id": "1000002"
            }
        }

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
                [user_infos['10001']],
                None,
            ),

            (
                {
                    'users': ['10001'],
                },
                [user_infos['10001']],
                None,
            ),

            (
                {
                    'users': ['aalvarez@ucsc.edu'],
                },
                [user_infos['10001']],
                None,
            ),

            (
                {
                    'users': ['aalvarez@ucsc.edu (10001)'],
                },
                [user_infos['10001']],
                None,
            ),

            (
                {
                    'users': ['Alice Alvarez'],
                },
                [user_infos['10001']],
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
                    user_infos['10001'],
                    user_infos['10002'],
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
                    user_infos['10001'],
                    user_infos['10002'],
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
                    user_infos['10001'],
                    user_infos['10002'],
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
                    user_infos['10001'],
                    user_infos['10002'],
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
                    user_infos['10001'],
                ],
                None,
            ),
        ]

        self.base_request_test(lms.api.user.fetch.request, test_cases)
