import typing

import lms.backend.testing
import lms.model.courses
import lms.model.groupsets
import lms.model.testdata.groups

def test_courses_groups_resolve_and_list_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of resolving and listing course groups. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '999'),
            },
            [
            ],
            'Could not resolve group set query',
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '999'),
            },
            [
            ],
            'Could not resolve group set query',
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(id = '131010100'),
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-1'],
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 1-2'],
            ],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 2'),
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 2-1'],
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 2-2'],
            ],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 3'),
            },
            [
                lms.model.testdata.groups.COURSE_GROUPS['Extra Course']['Group 3-1'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.get_backend().courses_groups_resolve_and_list, test_cases)
