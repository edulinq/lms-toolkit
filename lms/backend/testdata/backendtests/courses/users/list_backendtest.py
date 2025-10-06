import lms.backend.testing
import lms.model.testdata.users

def test_courses_users_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course users. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {},
            [
                lms.model.testdata.users.COURSE_USERS['1']['course-admin@test.edulinq.org'],
                lms.model.testdata.users.COURSE_USERS['1']['course-grader@test.edulinq.org'],
                lms.model.testdata.users.COURSE_USERS['1']['course-other@test.edulinq.org'],
                lms.model.testdata.users.COURSE_USERS['1']['course-owner@test.edulinq.org'],
                lms.model.testdata.users.COURSE_USERS['1']['course-student@test.edulinq.org'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_list, test_cases)
