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
                'assignment_queries': [],
            },
            [
            ],
            None,
        ),

        # Base - List
        (
            {
                'course_id': '2',
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(id = '2'),
                    lms.model.assignments.AssignmentQuery(id = '3'),
                ],
            },
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple Bash Assignment'],
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple C++ Assignment'],
            ],
            None,
        ),

        # Base - Fetch
        (
            {
                'course_id': '2',
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(id = '2'),
                ],
            },
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple Bash Assignment'],
            ],
            None,
        ),

        # Query - Name
        (
            {
                'course_id': '2',
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
                'course_id': '2',
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(name = 'A Simple Bash Assignment', id = '2'),
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
                'course_id': '2',
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
                'course_id': '2',
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
                'course_id': '2',
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(id = '2', name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),

        # Multiple Match
        (
            {
                'course_id': '2',
                'assignment_queries': [
                    lms.model.assignments.AssignmentQuery(id = '2'),
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
