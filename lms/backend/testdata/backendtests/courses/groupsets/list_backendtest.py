import lms.backend.testing
import lms.model.testdata.groupsets

def test_courses_groupsets_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course groupsets. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_id': '1',
            },
            [
            ],
            None,
        ),
        (
            {
                'course_id': '2',
            },
            [
            ],
            None,
        ),
        (
            {
                'course_id': '3',
            },
            [
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'],
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 2'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groupsets_list, test_cases)
