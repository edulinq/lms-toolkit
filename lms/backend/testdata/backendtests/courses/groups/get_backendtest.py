import lms.backend.testing
import lms.model.courses
import lms.model.groups
import lms.model.groupsets
import lms.model.testdata.groups

def test_courses_groups_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting course groups. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Empty
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
                'group_queries': [],
            },
            [
            ],
            None,
        ),

        # Course Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
                'group_queries': [
                    lms.model.groups.GroupQuery(name = 'Group 1-1'),
                ],
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'],
            ],
            None,
        ),

        # Miss - Course Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'ZZZ'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
                'group_queries': [
                    lms.model.groups.GroupQuery(name = 'Group 1-1'),
                ],
            },
            None,
            'Could not resolve course query',
        ),

        # Single
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
                'group_queries': [
                    lms.model.groups.GroupQuery(id = '131010101'),
                ],
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'],
            ],
            None,
        ),

        # Multiple
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131020200'),
                'group_queries': [
                    lms.model.groups.GroupQuery(id = '131020201'),
                    lms.model.groups.GroupQuery(id = '131020202'),
                ],
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 2-1'],
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 2-2'],
            ],
            None,
        ),

        # Query - Name
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
                'group_queries': [
                    lms.model.groups.GroupQuery(name = 'Group 1-1'),
                ],
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'],
            ],
            None,
        ),

        # Query - Label
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
                'group_queries': [
                    lms.model.groups.GroupQuery(name = 'Group 1-2', id = '131010102'),
                ],
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-2'],
            ],
            None,
        ),

        # Miss - ID
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
                'group_queries': [
                    lms.model.groups.GroupQuery(id = '999'),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
                'group_queries': [
                    lms.model.groups.GroupQuery(name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Partial Match
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
                'group_queries': [
                    lms.model.groups.GroupQuery(id = '131010101', name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),

        # Multiple Match
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
                'group_queries': [
                    lms.model.groups.GroupQuery(id = '131010101'),
                    lms.model.groups.GroupQuery(name = 'Group 1-1'),
                ],
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groups_get, test_cases)
