import lms.backend.testing
import lms.model.assignments
import lms.model.courses
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
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'assignment_query': lms.model.assignments.AssignmentQuery(id = '110000100'),
                'user_queries': [],
            },
            [
            ],
            None,
        ),

        # Base
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'assignment_query': lms.model.assignments.AssignmentQuery(id = '110000100'),
                'user_queries': [
                    lms.model.users.UserQuery(id = '100050000'),
                ],
            },
            [
                scores['Course 101']['Homework 0']['course-student'],
            ],
            None,
        ),

        # Course Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'assignment_query': lms.model.assignments.AssignmentQuery(id = '110000100'),
                'user_queries': [
                    lms.model.users.UserQuery(id = '100050000'),
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
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
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
