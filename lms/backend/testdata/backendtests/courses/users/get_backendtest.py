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
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'user_queries': [],
            },
            [
            ],
            None,
        ),

        # Base - List
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'user_queries': [
                    lms.model.users.UserQuery(id = '100010000'),
                    lms.model.users.UserQuery(id = '100020000'),
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
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'user_queries': [
                    lms.model.users.UserQuery(id = '100010000'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-admin'],
            ],
            None,
        ),

        # Course Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'user_queries': [
                    lms.model.users.UserQuery(id = '100010000'),
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
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
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
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
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
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'user_queries': [
                    lms.model.users.UserQuery(name = 'course-admin', id = '100010000'),
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
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'user_queries': [
                    lms.model.users.UserQuery(email = 'course-admin@test.edulinq.org', id = '100010000'),
                ],
            },
            [
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-admin'],
            ],
            None,
        ),

        # Miss - Course
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '999'),
                'user_queries': [
                    lms.model.users.UserQuery(id = '100010000'),
                ],
            },
            None,
            'Could not resolve course query',
        ),

        # Miss - ID
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'user_queries': [
                    lms.model.users.UserQuery(id = '999'),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Name
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
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
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
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
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'user_queries': [
                    lms.model.users.UserQuery(id = '100010000', name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),

        # Multiple Match
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'user_queries': [
                    lms.model.users.UserQuery(id = '100010000'),
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
