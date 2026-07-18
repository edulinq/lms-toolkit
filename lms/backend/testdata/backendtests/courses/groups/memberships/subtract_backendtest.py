import copy
import typing

import lms.backend.testing
import lms.model.testdata.groups

def test_courses_groups_memberships_subtract_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of subtracting group memberships. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        (
            {
                'course_id': '130000000',
                'groupset_id': '131010100',
                'group_id': '131010101',
                'user_ids': [
                    '100060000',
                ],
            },
            1,
            None,
        ),
        (
            {
                'course_id': '130000000',
                'groupset_id': '131010100',
                'group_id': '131010101',
                'user_ids': [
                    '100060000',
                    '100070000',
                ],
            },
            2,
            None,
        ),
    ]

    test.base_request_test(test.get_backend().courses_groups_memberships_subtract, test_cases)
