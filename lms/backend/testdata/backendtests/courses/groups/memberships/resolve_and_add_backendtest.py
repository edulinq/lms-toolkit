import lms.backend.testing
import lms.model.courses
import lms.model.groups
import lms.model.groupsets
import lms.model.users
import lms.model.testdata.groups

def test_courses_groups_memberships_resolve_and_add_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and adding group memberships. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 3'),
                'group_query': lms.model.groups.GroupQuery(name = 'Group 3-1'),
                'user_queries': [
                    lms.model.users.UserQuery(name = 'extra-course-student-1'),
                ],
            },
            1,
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 3'),
                'group_query': lms.model.groups.GroupQuery(name = 'Group 3-1'),
                'user_queries': [
                    lms.model.users.UserQuery(name = 'extra-course-student-1'),
                    lms.model.users.UserQuery(name = 'extra-course-student-2'),
                ],
            },
            2,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groups_memberships_resolve_and_add, test_cases)
