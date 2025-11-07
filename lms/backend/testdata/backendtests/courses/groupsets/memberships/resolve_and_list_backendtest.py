import lms.backend.testing
import lms.model.courses
import lms.model.groupsets
import lms.model.testdata.groups

def test_courses_groupsets_memberships_resolve_and_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and listing groupset memberships. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '999'),
            },
            None,
            'Could not resolve group set query',
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '999'),
            },
            None,
            'Could not resolve group set query',
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
            },
            [
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-1'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-2'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-3'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-4'],
            ],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 2'),
            },
            [
                # Note the ordering by group then user.
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-1'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-3'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-2'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-4'],
            ],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 3'),
            },
            [
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groupsets_memberships_resolve_and_list, test_cases)
