import copy

import lms.backend.testing
import lms.model.courses
import lms.model.groups
import lms.model.groupsets
import lms.model.users
import lms.model.testdata.groups

def test_courses_groupsets_memberships_resolve_and_subtract_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and subtracting group set memberships. """

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
                        user = lms.model.users.UserQuery(name = 'extra-course-student-3'),
                    ),
                ]
            },
            {
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'].to_query(): 0,
            },
            None,
        ),

        # Sub Only
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
            {
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'].to_query(): 1,
            },
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
                        group = lms.model.groups.GroupQuery(name = 'Group 1-2'),
                        user = lms.model.users.UserQuery(name = 'extra-course-student-1'),
                    ),
                ]
            },
            {
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'].to_query(): 1,
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-2'].to_query(): 0,
            },
            None,
        ),
    ]

    def _assertion_func(expected, actual):
        # Convert the non-JSON keys.

        clean_expected = {}
        for (key, value) in expected.items():
            clean_expected[str(key)] = value

        clean_actual = {}
        for (key, value) in actual.items():
            clean_actual[str(key)] = value

        test.assertDictEqual(clean_expected, clean_actual)

    test.base_request_test(test.backend.courses_groupsets_memberships_resolve_and_subtract, test_cases,
            assertion_func = _assertion_func)
