import lms.backend.testing
import lms.model.users
import lms.model.testdata.users

def test_courses_users_fetch_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of fetching course users. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'user_id': '6',
            },
            lms.model.testdata.users.COURSE_USERS['1']['course-student@test.edulinq.org'],
            None,
        ),

        # Miss
        (
            {
                'user_id': '999',
            },
            None,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_fetch, test_cases)
