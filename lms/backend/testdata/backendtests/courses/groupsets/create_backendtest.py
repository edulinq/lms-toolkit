import copy
import typing

import lms.backend.testing
import lms.model.groupsets

DUMMY_ID: str = '123456789'

def test_courses_groupsets_create_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of creating group sets. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        (
            {
                'course_id': '110000000',
                'name': 'test_groupset_1',
            },
            lms.model.groupsets.GroupSet(id = DUMMY_ID, name = 'test_groupset_1'),
            None,
        ),
    ]

    # IDs from the backend may be inconsistent.
    def _clean_result(result: typing.Any) -> typing.Any:
        """ Clean the result. """

        result = copy.deepcopy(result)
        result.id = DUMMY_ID

        return result

    test.base_request_test(test.get_backend().courses_groupsets_create, test_cases,
            actual_clean_func = _clean_result)
