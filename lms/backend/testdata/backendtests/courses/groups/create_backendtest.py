import copy
import typing

import lms.backend.testing
import lms.model.groups

DUMMY_ID: str = '123456789'

def test_courses_groups_create_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of creating groups. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        (
            {
                'course_id': '130000000',
                'groupset_id': '131010100',
                'name': 'test_group_1',
            },
            lms.model.groups.Group(id = DUMMY_ID, name = 'test_group_1'),
            None,
        ),
    ]

    def _clean_result(result: typing.Any) -> typing.Any:
        """ IDs from the backend may be inconsistent. """

        result = copy.deepcopy(result)
        result.id = DUMMY_ID

        return result

    test.base_request_test(test.get_backend().courses_groups_create, test_cases,
            actual_clean_func = _clean_result)
