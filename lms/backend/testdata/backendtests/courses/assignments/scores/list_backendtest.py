import lms.backend.testing
import lms.model.testdata.scores

def test_courses_assignments_scores_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing assignments scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_id': '1',
                'assignment_id': '1',
            },
            [
                scores['Course 101']['Homework 0']['course-student'],
            ],
            None,
        ),

        (
            {
                'course_id': '2',
                'assignment_id': '2',
            },
            [
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_scores_list, test_cases)

def test_courses_assignments_scores_resolve_and_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing assignments scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES_RESOLVED

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_id': '1',
                'assignment_query': lms.model.assignments.AssignmentQuery(id = '1'),
            },
            [
                scores['Course 101']['Homework 0']['course-student'],
            ],
            None,
        ),

        (
            {
                'course_id': '2',
                'assignment_query': lms.model.assignments.AssignmentQuery(id = '2'),
            },
            [
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_scores_resolve_and_list, test_cases)
