import lms.backend.testing
import lms.model.testdata.assignments

def test_courses_assignments_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course assignments. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {},
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['1']['1'],
            ],
            None,
        ),

        (
            {
                'course_id': '2',
            },
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['2']['2'],
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['2']['3'],
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['2']['4'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_list, test_cases)
