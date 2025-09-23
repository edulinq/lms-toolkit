import lms.api.testing
import lms.api.user.list

class UserListTest(lms.api.testing.HTTPTest):
    """ Test listing course users. """

    def test_user_list_base(self):
        """ Test the base functionality of users/list. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            (
                {},
                [
                    {
                        "email": "aalvarez@ucsc.edu",
                        "enrollment": "<unknown>",
                        "id": "10001",
                        "name": "Alice Alvarez",
                        "sis_user_id": "1000001"
                    },
                    {
                        "email": "bburnquist@ucsc.edu",
                        "enrollment": "<unknown>",
                        "id": "10002",
                        "name": "Bob Burnquist",
                        "sis_user_id": "1000002"
                    }
                ],
                None,
            ),
        ]

        self.base_request_test(lms.api.user.list.request, test_cases)
