import lms.backend.testing
import lms.model.testdata.groups

def test_courses_groups_fetch_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of fetching course groups. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '130000000',
                'groupset_id': '131010100',
                'group_id': '131010101',
            },
            lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'],
            None,
        ),

        # Miss - Group Set
        (
            {
                'course_id': '110000000',
                'groupset_id': '999',
                'group_id': '131010101',
            },
            None,
            None,
        ),

        # Miss - Group
        (
            {
                'course_id': '110000000',
                'groupset_id': '131010100',
                'group_id': '999',
            },
            None,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groups_fetch, test_cases)
