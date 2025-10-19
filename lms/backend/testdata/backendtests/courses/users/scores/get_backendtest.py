import lms.backend.testing
import lms.model.assignments
import lms.model.testdata.scores
import lms.model.users

def test_courses_users_scores_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting users' scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Empty
        (
            {
                'course_id': '1',
                'user_query': lms.model.users.UserQuery(id = '6'),
                'assignment_queries': [],
            },
            [
            ],
            None,
        ),

        # Base
        (
            {
                'course_id': '1',
                'user_query': lms.model.users.UserQuery(id = '6'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(id = '1'),
                ],
            },
            [
                scores['Course 101']['Homework 0']['course-student'],
            ],
            None,
        ),

        # Queries
        (
            {
                'course_id': '1',
                'user_query': lms.model.users.UserQuery(email = 'course-student@test.edulinq.org'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(name = 'Homework 0'),
                ],
            },
            [
                scores['Course 101']['Homework 0']['course-student'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_scores_get, test_cases)
