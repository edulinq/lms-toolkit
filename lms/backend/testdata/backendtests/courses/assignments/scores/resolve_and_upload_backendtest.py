import lms.backend.testing
import lms.model.assignments
import lms.model.courses
import lms.model.scores
import lms.model.users

def test_courses_assignments_scores_resolve_and_upload_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and uploading assignments scores. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'assignment_query': lms.model.assignments.AssignmentQuery(id = '110000100'),
                'scores': {
                    lms.model.users.UserQuery(id = '100050000'): lms.model.scores.ScoreFragment(score = 1.0),
                },
            },
            1,
            None,
        ),

        # Comment
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'assignment_query': lms.model.assignments.AssignmentQuery(id = '110000100'),
                'scores': {
                    lms.model.users.UserQuery(id = '100050000'): lms.model.scores.ScoreFragment(score = 1.0, comment = 'foo'),
                },
            },
            1,
            None,
        ),

        # Queries
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'assignment_query': lms.model.assignments.AssignmentQuery(name = 'Homework 0'),
                'scores': {
                    lms.model.users.UserQuery(name = 'course-student'): lms.model.scores.ScoreFragment(score = 1.0),
                },
            },
            1,
            None,
        ),

        # Miss - Course
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'ZZZ'),
                'assignment_query': lms.model.assignments.AssignmentQuery(name = 'Homework 0'),
                'scores': {
                    lms.model.users.UserQuery(name = 'course-student'): lms.model.scores.ScoreFragment(score = 1.0),
                },
            },
            None,
            'Could not resolve course query',
        ),

        # Miss - Assignment
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'assignment_query': lms.model.assignments.AssignmentQuery(name = 'ZZZ'),
                'scores': {
                    lms.model.users.UserQuery(name = 'course-student'): lms.model.scores.ScoreFragment(score = 1.0),
                },
            },
            None,
            'Could not resolve assignment query',
        ),

        # Miss - User
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'assignment_query': lms.model.assignments.AssignmentQuery(name = 'Homework 0'),
                'scores': {
                    lms.model.users.UserQuery(name = 'ZZZ'): lms.model.scores.ScoreFragment(score = 1.0),
                },
            },
            0,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_scores_resolve_and_upload, test_cases)
