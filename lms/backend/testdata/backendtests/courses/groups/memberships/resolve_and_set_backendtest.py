import copy

import lms.backend.testing
import lms.model.courses
import lms.model.groups
import lms.model.groupsets
import lms.model.users
import lms.model.testdata.groups

def test_courses_groups_memberships_resolve_and_set_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and seting group memberships. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Only Add
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 3'),
                'group_query': lms.model.groups.GroupQuery(name = 'Group 3-1'),
                'user_queries': [
                    lms.model.users.UserQuery(name = 'extra-course-student-1'),
                ],
            },
            (1, 0, False),
            None,
        ),

        # Only Subtract
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                'group_query': lms.model.groups.GroupQuery(name = 'Group 1-1'),
                'user_queries': [
                ],
            },
            (0, 2, False),
            None,
        ),

        # Add Subtract
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                'group_query': lms.model.groups.GroupQuery(name = 'Group 1-1'),
                'user_queries': [
                    lms.model.users.UserQuery(name = 'extra-course-student-2'),
                    lms.model.users.UserQuery(name = 'extra-course-student-3'),
                ],
            },
            (1, 1, False),
            None,
        ),

        # No Action
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                'group_query': lms.model.groups.GroupQuery(name = 'Group 1-1'),
                'user_queries': [
                    lms.model.users.UserQuery(name = 'extra-course-student-1'),
                    lms.model.users.UserQuery(name = 'extra-course-student-2'),
                ],
            },
            (0, 0, False),
            None,
        ),

        # Subtract, Delete Empty
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                'group_query': lms.model.groups.GroupQuery(name = 'Group 1-1'),
                'delete_empty': True,
                'user_queries': [
                ],
            },
            (0, 2, True),
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groups_memberships_resolve_and_set, test_cases)
