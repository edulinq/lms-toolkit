import lms.backend.testing
import lms.model.testdata.users

def test_courses_users_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course users. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_id': '110000000',
            },
            [
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-admin'],
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-grader'],
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-other'],
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-owner'],
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-student'],
            ],
            None,
        ),
        (
            {
                'course_id': '120000000',
            },
            [
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-admin'],
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-grader'],
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-other'],
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-owner'],
                lms.model.testdata.users.COURSE_USERS['Course 101']['course-student'],
            ],
            None,
        ),
        (
            {
                'course_id': '130000000',
            },
            [
                lms.model.testdata.users.COURSE_USERS['Extra Course']['course-owner'],
                lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-1'],
                lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-2'],
                lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-3'],
                lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-4'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_list, test_cases)
