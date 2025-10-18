import lms.backend.testing
import lms.model.testdata.scores

def test_courses_users_scores_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing users' scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_id': '1',
                'user_id': '6',
            },
            [
                scores['Course 101']['Homework 0']['course-student'],
            ],
            None,
        ),

        (
            {
                'course_id': '2',
                'user_id': '6',
            },
            [
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_scores_list, test_cases)

def test_courses_users_scores_resolve_and_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing users' scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES_RESOLVED

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_id': '1',
                'user_query': lms.model.users.UserQuery(id = '6'),
            },
            [
                scores['Course 101']['Homework 0']['course-student'],
            ],
            None,
        ),

        (
            {
                'course_id': '2',
                'user_query': lms.model.users.UserQuery(id = '6'),
            },
            [
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_scores_resolve_and_list, test_cases)
