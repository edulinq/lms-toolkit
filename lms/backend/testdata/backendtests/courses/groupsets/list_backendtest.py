import lms.backend.testing
import lms.model.testdata.groupsets

def test_courses_groupsets_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course groupsets. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_id': '110000000',
            },
            [
            ],
            None,
        ),
        (
            {
                'course_id': '120000000',
            },
            [
            ],
            None,
        ),
        (
            {
                'course_id': '130000000',
            },
            [
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'],
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 2'],
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 3'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groupsets_list, test_cases)
