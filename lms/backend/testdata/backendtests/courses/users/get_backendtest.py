import lms.backend.testing
import lms.model.users
import lms.model.testdata.users

def test_courses_users_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting course users. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Empty
        (
            {
                'queries': [],
            },
            [
            ],
            None,
        ),

        # Base - List
        (
            {
                'queries': [
                    lms.model.users.UserQuery(id = '2'),
                    lms.model.users.UserQuery(id = '3'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['1']['course-admin@test.edulinq.org'],
                lms.model.testdata.users.COURSE_USERS['1']['course-grader@test.edulinq.org'],
            ],
            None,
        ),

        # Base - Fetch
        (
            {
                'queries': [
                    lms.model.users.UserQuery(id = '2'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['1']['course-admin@test.edulinq.org'],
            ],
            None,
        ),

        # Query - Name
        (
            {
                'queries': [
                    lms.model.users.UserQuery(name = 'course-admin'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['1']['course-admin@test.edulinq.org'],
            ],
            None,
        ),

        # Query - Email
        (
            {
                'queries': [
                    lms.model.users.UserQuery(email = 'course-admin@test.edulinq.org'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['1']['course-admin@test.edulinq.org'],
            ],
            None,
        ),

        # Query - Label Name
        (
            {
                'queries': [
                    lms.model.users.UserQuery(name = 'course-admin', id = '2'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['1']['course-admin@test.edulinq.org'],
            ],
            None,
        ),

        # Query - Label Email
        (
            {
                'queries': [
                    lms.model.users.UserQuery(email = 'course-admin@test.edulinq.org', id = '2'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['1']['course-admin@test.edulinq.org'],
            ],
            None,
        ),

        # Miss - ID
        (
            {
                'queries': [
                    lms.model.users.UserQuery(id = 999),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Name
        (
            {
                'queries': [
                    lms.model.users.UserQuery(name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Email
        (
            {
                'queries': [
                    lms.model.users.UserQuery(email = 'ZZZ@test.edulinq.org'),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Partial Match
        (
            {
                'queries': [
                    lms.model.users.UserQuery(id = '2', name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),

        # Multiple Match
        (
            {
                'queries': [
                    lms.model.users.UserQuery(id = '2'),
                    lms.model.users.UserQuery(name = 'course-admin'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['1']['course-admin@test.edulinq.org'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_get, test_cases)
