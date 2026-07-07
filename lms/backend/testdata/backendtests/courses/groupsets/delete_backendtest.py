import typing

import lms.backend.testing

def test_courses_groupsets_delete_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of deleting group sets. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        (
            {
                'course_id': '130000000',
                'groupset_id': '131010100',
            },
            True,
            None,
        ),
        (
            {
                'course_id': '130000000',
                'groupset_id': '999',
            },
            False,
            None,
        ),
    ]

    test.base_request_test(test.get_backend().courses_groupsets_delete, test_cases)
