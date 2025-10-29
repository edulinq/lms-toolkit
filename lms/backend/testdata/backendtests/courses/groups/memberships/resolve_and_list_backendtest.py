import lms.backend.testing
import lms.model.courses
import lms.model.groups
import lms.model.groupsets
import lms.model.testdata.groups

def test_courses_groups_memberships_resolve_and_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and listing group memberships. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '999'),
                'group_query': lms.model.groups.GroupQuery(id = '999'),
            },
            None,
            'Could not resolve group set query',
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '999'),
                'group_query': lms.model.groups.GroupQuery(id = '999'),
            },
            None,
            'Could not resolve group set query',
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
                'group_query': lms.model.groups.GroupQuery(id = '131010101'),
            },
            [
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-1'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-2'],
            ],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                'group_query': lms.model.groups.GroupQuery(id = '131010102'),
            },
            [
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-3'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-4'],
            ],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131020200'),
                'group_query': lms.model.groups.GroupQuery(name = 'Group 2-1'),
            },
            [
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-1'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-3'],
            ],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 2'),
                'group_query': lms.model.groups.GroupQuery(name = 'Group 2-2'),
            },
            [
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-2'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-4'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groups_memberships_resolve_and_list, test_cases)
