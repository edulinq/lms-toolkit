import lms.backend.testing

def test_courses_groups_delete_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of deleting groups. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_id': '130000000',
                'groupset_id': '131010100',
                'group_id': '131010101',
            },
            True,
            None,
        ),
        (
            {
                'course_id': '130000000',
                'groupset_id': '131010100',
                'group_id': '999',
            },
            False,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groups_delete, test_cases)
