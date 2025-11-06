import copy

import lms.backend.testing
import lms.model.courses
import lms.model.groups
import lms.model.groupsets
import lms.model.users
import lms.model.testdata.groups

DUMMY_ID: str = '123456789'

def test_courses_groupsets_memberships_resolve_and_add_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and adding group set memberships. """

    created_group_name = 'test_group_1'
    created_group = lms.model.groups.Group(id = DUMMY_ID, name = created_group_name)

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # No Op
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                'memberships': [
                    lms.model.groups.GroupMembership(
                        group = lms.model.groups.GroupQuery(name = 'Group 1-1'),
                        user = lms.model.users.UserQuery(name = 'extra-course-student-1'),
                    ),
                ]
            },
            (
                [],
                {
                    lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'].to_query(): 0,
                },
            ),
            None,
        ),

        # Add Only
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                'memberships': [
                    lms.model.groups.GroupMembership(
                        group = lms.model.groups.GroupQuery(name = 'Group 1-1'),
                        user = lms.model.users.UserQuery(name = 'extra-course-student-3'),
                    ),
                ]
            },
            (
                [],
                {
                    lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'].to_query(): 1,
                },
            ),
            None,
        ),

        # Create Group
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                'memberships': [
                    lms.model.groups.GroupMembership(
                        group = lms.model.groups.GroupQuery(name = created_group_name),
                        user = lms.model.users.UserQuery(name = 'extra-course-student-1'),
                    ),
                ]
            },
            (
                [
                    created_group,
                ],
                {
                    created_group.to_query(): 1,
                },
            ),
            None,
        ),

        # All
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                'memberships': [
                    lms.model.groups.GroupMembership(
                        group = lms.model.groups.GroupQuery(name = 'Group 1-1'),
                        user = lms.model.users.UserQuery(name = 'extra-course-student-1'),
                    ),
                    lms.model.groups.GroupMembership(
                        group = lms.model.groups.GroupQuery(name = 'Group 1-1'),
                        user = lms.model.users.UserQuery(name = 'extra-course-student-3'),
                    ),
                    lms.model.groups.GroupMembership(
                        group = lms.model.groups.GroupQuery(name = created_group_name),
                        user = lms.model.users.UserQuery(name = 'extra-course-student-1'),
                    ),
                ]
            },
            (
                [
                    created_group,
                ],
                {
                    lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'].to_query(): 1,
                    created_group.to_query(): 1,
                },
            ),
            None,
        ),
    ]

    def _assertion_func(expected, actual):
        if (isinstance(expected, list)):
            test.assertJSONListEqual(expected, actual)
            return

        # Convert the non-JSON keys.

        clean_expected = {}
        for (key, value) in expected.items():
            clean_expected[str(key)] = value

        clean_actual = {}
        for (key, value) in actual.items():
            clean_actual[str(key)] = value

        test.assertDictEqual(clean_expected, clean_actual)

    # IDs from the backend may be inconsistent.
    def _clean_result(result):
        result = copy.deepcopy(result)

        # Clean the created groups.
        for group in result[0]:
            group.id = DUMMY_ID

        # Clean the group counts.
        for group in list(result[1].keys()):
            if (group.name == created_group_name):
                group.id = DUMMY_ID

        return result

    test.base_request_test(test.backend.courses_groupsets_memberships_resolve_and_add, test_cases,
            assertion_func = _assertion_func,
            actual_clean_func = _clean_result)
