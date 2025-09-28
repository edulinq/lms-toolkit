import lms.backend.testing
import testdata.common.model.users

def test_courses_users_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course users. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {},
            [
                testdata.common.model.users.COURSE_USERS['1']['course-admin@test.edulinq.org'],
                testdata.common.model.users.COURSE_USERS['1']['course-grader@test.edulinq.org'],
                testdata.common.model.users.COURSE_USERS['1']['course-other@test.edulinq.org'],
                testdata.common.model.users.COURSE_USERS['1']['course-owner@test.edulinq.org'],
                testdata.common.model.users.COURSE_USERS['1']['course-student@test.edulinq.org'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_list, test_cases)
