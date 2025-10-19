import lms.backend.testing
import lms.model.testdata.scores

def test_courses_users_scores_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing users' scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES_UNRESOLVED

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

        (
            {
                'course_id': '3',
                'user_id': '7',
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-1'],
                scores['Extra Course']['Assignment 2']['extra-course-student-1'],
                scores['Extra Course']['Assignment 3']['extra-course-student-1'],
            ],
            None,
        ),

        (
            {
                'course_id': '3',
                'user_id': '8',
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-2'],
                scores['Extra Course']['Assignment 2']['extra-course-student-2'],
                scores['Extra Course']['Assignment 3']['extra-course-student-2'],
            ],
            None,
        ),

        (
            {
                'course_id': '3',
                'user_id': '9',
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-3'],
                scores['Extra Course']['Assignment 2']['extra-course-student-3'],
                scores['Extra Course']['Assignment 3']['extra-course-student-3'],
            ],
            None,
        ),

        (
            {
                'course_id': '3',
                'user_id': '10',
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-4'],
                scores['Extra Course']['Assignment 2']['extra-course-student-4'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_scores_list, test_cases)

def test_courses_users_scores_resolve_and_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing users' scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES

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

        (
            {
                'course_id': '3',
                'user_query': lms.model.users.UserQuery(id = '7'),
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-1'],
                scores['Extra Course']['Assignment 2']['extra-course-student-1'],
                scores['Extra Course']['Assignment 3']['extra-course-student-1'],
            ],
            None,
        ),

        (
            {
                'course_id': '3',
                'user_query': lms.model.users.UserQuery(id = '8'),
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-2'],
                scores['Extra Course']['Assignment 2']['extra-course-student-2'],
                scores['Extra Course']['Assignment 3']['extra-course-student-2'],
            ],
            None,
        ),

        (
            {
                'course_id': '3',
                'user_query': lms.model.users.UserQuery(id = '9'),
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-3'],
                scores['Extra Course']['Assignment 2']['extra-course-student-3'],
                scores['Extra Course']['Assignment 3']['extra-course-student-3'],
            ],
            None,
        ),

        (
            {
                'course_id': '3',
                'user_query': lms.model.users.UserQuery(id = '10'),
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-4'],
                scores['Extra Course']['Assignment 2']['extra-course-student-4'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_scores_resolve_and_list, test_cases)
