import lms.backend.testing
import lms.model.assignments
import lms.model.testdata.assignments

def test_courses_assignments_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting course assignments. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Empty
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'assignment_queries': [],
            },
            [
            ],
            None,
        ),

        # Course Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(name = 'Homework 0'),
                ],
            },
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course 101']['Homework 0'],
            ],
            None,
        ),

        # Miss - Course Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'ZZZ'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(name = 'Homework 0'),
                ],
            },
            None,
            'Could not resolve course query',
        ),

        # Single
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(id = '120000100'),
                ],
            },
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple Bash Assignment'],
            ],
            None,
        ),

        # Multiple
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(id = '120000100'),
                    lms.model.assignments.AssignmentQuery(id = '120000200'),
                ],
            },
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple Bash Assignment'],
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple C++ Assignment'],
            ],
            None,
        ),

        # Query - Name
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(name = 'A Simple Bash Assignment'),
                ],
            },
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple Bash Assignment'],
            ],
            None,
        ),

        # Query - Label
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(name = 'A Simple Bash Assignment', id = '120000100'),
                ],
            },
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple Bash Assignment'],
            ],
            None,
        ),

        # Miss - ID
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(id = 999),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Partial Match
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(id = '120000100', name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),

        # Multiple Match
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(id = '120000100'),
                    lms.model.assignments.AssignmentQuery(name = 'A Simple Bash Assignment'),
                ],
            },
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple Bash Assignment'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_get, test_cases)
