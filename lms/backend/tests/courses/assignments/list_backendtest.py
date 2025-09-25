import lms.backend.testing
import lms.backend.tests.courses.assignments.testing

def test_courses_assignments_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course assignments. """

    # TEST

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {},
            [],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_list, test_cases)
