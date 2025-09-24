import lms.api.testing
import lms.api.user.list
import lms.api.user.testing

class UserListTest(lms.api.testing.HTTPTest):
    """ Test listing course users. """

    def test_user_list_base(self):
        """ Test the base functionality of listing users. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            (
                {},
                [
                    lms.api.user.testing.USERS['10001'],
                    lms.api.user.testing.USERS['10002'],
                ],
                None,
            ),
        ]

        self.base_request_test(lms.api.user.list.request, test_cases)
