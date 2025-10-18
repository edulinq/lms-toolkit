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
                'user_queries': [],
            },
            [
            ],
            None,
        ),

        # Base - List
        (
            {
                'user_queries': [
                    lms.model.users.UserQuery(id = '2'),
                    lms.model.users.UserQuery(id = '3'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-admin'],
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-grader'],
            ],
            None,
        ),

        # Base - Fetch
        (
            {
                'user_queries': [
                    lms.model.users.UserQuery(id = '2'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-admin'],
            ],
            None,
        ),

        # Query - Name
        (
            {
                'user_queries': [
                    lms.model.users.UserQuery(name = 'course-admin'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-admin'],
            ],
            None,
        ),

        # Query - Email
        (
            {
                'user_queries': [
                    lms.model.users.UserQuery(email = 'course-admin@test.edulinq.org'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-admin'],
            ],
            None,
        ),

        # Query - Label Name
        (
            {
                'user_queries': [
                    lms.model.users.UserQuery(name = 'course-admin', id = '2'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-admin'],
            ],
            None,
        ),

        # Query - Label Email
        (
            {
                'user_queries': [
                    lms.model.users.UserQuery(email = 'course-admin@test.edulinq.org', id = '2'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-admin'],
            ],
            None,
        ),

        # Miss - ID
        (
            {
                'user_queries': [
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
                'user_queries': [
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
                'user_queries': [
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
                'user_queries': [
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
                'user_queries': [
                    lms.model.users.UserQuery(id = '2'),
                    lms.model.users.UserQuery(name = 'course-admin'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-admin'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_get, test_cases)
