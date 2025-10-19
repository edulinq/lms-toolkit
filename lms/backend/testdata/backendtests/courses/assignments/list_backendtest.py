import lms.backend.testing
import lms.model.testdata.assignments

def test_courses_assignments_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course assignments. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {},
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course 101']['Homework 0'],
            ],
            None,
        ),
        (
            {
                'course_id': '2',
            },
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple Bash Assignment'],
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple C++ Assignment'],
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course Using Different Languages']['A Simple Java Assignment'],
            ],
            None,
        ),
        (
            {
                'course_id': '3',
            },
            [
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 1'],
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 2'],
                lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 3'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_list, test_cases)
