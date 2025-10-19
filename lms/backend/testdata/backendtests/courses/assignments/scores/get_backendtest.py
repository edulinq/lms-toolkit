import lms.backend.testing
import lms.model.assignments
import lms.model.testdata.scores
import lms.model.users

def test_courses_assignments_scores_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting assignments scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Empty
        (
            {
                'course_id': '1',
                'assignment_query': lms.model.assignments.AssignmentQuery(id = '1'),
                'user_queries': [],
            },
            [
            ],
            None,
        ),

        # Base
        (
            {
                'course_id': '1',
                'assignment_query': lms.model.assignments.AssignmentQuery(id = '1'),
                'user_queries': [
                    lms.model.users.UserQuery(id = '6'),
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
                'assignment_query': lms.model.assignments.AssignmentQuery(name = 'Homework 0'),
                'user_queries': [
                    lms.model.users.UserQuery(email = 'course-student@test.edulinq.org'),
                ],
            },
            [
                scores['Course 101']['Homework 0']['course-student'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_scores_get, test_cases)
