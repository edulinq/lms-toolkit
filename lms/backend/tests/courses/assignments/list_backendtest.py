import lms.backend.testing
import testdata.common.model.assignments

def test_courses_assignments_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course assignments. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {},
            [
                testdata.common.model.assignments.COURSE_ASSIGNMENTS['1']['Homework 0'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_list, test_cases)
