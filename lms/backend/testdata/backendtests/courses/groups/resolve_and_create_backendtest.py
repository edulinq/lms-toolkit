import copy
import typing

import lms.backend.testing
import lms.model.groups
import lms.model.groupsets

DUMMY_ID: str = '123456789'

def test_courses_groups_resolve_and_create_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of creating group (with resolution). """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
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

    test.base_request_test(test.get_backend().courses_groups_resolve_and_create, test_cases,
            actual_clean_func = _clean_result)
