import copy

import lms.backend.testing
import lms.model.groups
import lms.model.groupsets

DUMMY_ID: str = '123456789'

def test_courses_groups_resolve_and_create_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of creating group (with resolution). """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
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

    # IDs from the backend may be inconsistent.
    def _clean_result(result):
        result = copy.deepcopy(result)
        result.id = DUMMY_ID

        return result

    test.base_request_test(test.backend.courses_groups_resolve_and_create, test_cases,
            actual_clean_func = _clean_result)
