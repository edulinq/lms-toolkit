import lms.backend.testing
import lms.backend.tests.courses.users.testing

def test_courses_users_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course users. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {},
            [
                lms.backend.tests.courses.users.testing.USERS['10001'],
                lms.backend.tests.courses.users.testing.USERS['10002'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_list, test_cases)
