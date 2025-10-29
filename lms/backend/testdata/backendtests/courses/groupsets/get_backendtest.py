import lms.backend.testing
import lms.model.groupsets
import lms.model.testdata.groupsets

def test_courses_groupsets_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting course groupsets. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Empty
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_queries': [],
            },
            [
            ],
            None,
        ),

        # Course Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_queries': [
                    lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                ],
            },
            [
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'],
            ],
            None,
        ),

        # Miss - Course Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'ZZZ'),
                'groupset_queries': [
                    lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                ],
            },
            None,
            'Could not resolve course query',
        ),

        # Single
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_queries': [
                    lms.model.groupsets.GroupSetQuery(id = '131010100'),
                ],
            },
            [
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'],
            ],
            None,
        ),

        # Multiple
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_queries': [
                    lms.model.groupsets.GroupSetQuery(id = '131010100'),
                    lms.model.groupsets.GroupSetQuery(id = '131020200'),
                ],
            },
            [
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'],
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 2'],
            ],
            None,
        ),

        # Query - Name
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_queries': [
                    lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                ],
            },
            [
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'],
            ],
            None,
        ),

        # Query - Label
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_queries': [
                    lms.model.groupsets.GroupSetQuery(name = 'Group Set 2', id = '131020200'),
                ],
            },
            [
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 2'],
            ],
            None,
        ),

        # Miss - ID
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_queries': [
                    lms.model.groupsets.GroupSetQuery(id = 999),
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
                'groupset_queries': [
                    lms.model.groupsets.GroupSetQuery(name = 'ZZZ'),
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
                'groupset_queries': [
                    lms.model.groupsets.GroupSetQuery(id = '131010100', name = 'ZZZ'),
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
                'groupset_queries': [
                    lms.model.groupsets.GroupSetQuery(id = '131010100'),
                    lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
                ],
            },
            [
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groupsets_get, test_cases)
