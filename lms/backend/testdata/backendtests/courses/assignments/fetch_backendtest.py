import lms.backend.testing
import lms.model.assignments
import lms.model.testdata.assignments

def test_courses_assignments_fetch_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of fetching course assignments. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'assignment_id': '1',
            },
            lms.model.testdata.assignments.COURSE_ASSIGNMENTS['1']['1'],
            None,
        ),

        # Miss
        (
            {
                'assignment_id': '999',
            },
            None,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_fetch, test_cases)
