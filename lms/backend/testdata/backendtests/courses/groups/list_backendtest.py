import lms.backend.testing
import lms.model.testdata.groups

def test_courses_groups_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing course groups. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_id': '110000000',
                'groupset_id': '999',
            },
            [
            ],
            None,
        ),
        (
            {
                'course_id': '120000000',
                'groupset_id': '999',
            },
            [
            ],
            None,
        ),

        (
            {
                'course_id': '130000000',
                'groupset_id': '131010100',
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'],
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-2'],
            ],
            None,
        ),
        (
            {
                'course_id': '130000000',
                'groupset_id': '131020200',
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 2-1'],
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 2-2'],
            ],
            None,
        ),
        (
            {
                'course_id': '130000000',
                'groupset_id': '131030300',
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 3-1'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groups_list, test_cases)
