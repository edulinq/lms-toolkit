import copy
import typing

import lms.backend.testing
import lms.model.testdata.groups

def test_courses_groups_memberships_list_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of listing group memberships. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        (
            {
                'course_id': '110000000',
                'groupset_id': '999',
                'group_id': '999',
            },
            [
            ],
            None,
        ),
        (
            {
                'course_id': '120000000',
                'groupset_id': '999',
                'group_id': '999',
            },
            [
            ],
            None,
        ),
        (
            {
                'course_id': '130000000',
                'groupset_id': '131010100',
                'group_id': '131010101',
            },
            [
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-1'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-2'],
            ],
            None,
        ),
        (
            {
                'course_id': '130000000',
                'groupset_id': '131010100',
                'group_id': '131010102',
            },
            [
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-3'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 1']['extra-course-student-4'],
            ],
            None,
        ),
        (
            {
                'course_id': '130000000',
                'groupset_id': '131020200',
                'group_id': '131020201',
            },
            [
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-1'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-3'],
            ],
            None,
        ),
        (
            {
                'course_id': '130000000',
                'groupset_id': '131020200',
                'group_id': '131020202',
            },
            [
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-2'],
                lms.model.testdata.groups.COURSE_GROUP_MEMBERSHIPS['Extra Course']['Group Set 2']['extra-course-student-4'],
            ],
            None,
        ),
    ]

    def _clean_result(result: typing.Any) -> typing.Any:
        """ Strip down the queries (which may be partially resolved). """

        result = copy.deepcopy(result)

        for item in result:
            item.groupset.name = None
            item.group.name = None
            item.user.name = None
            item.user.email = None

        return result

    test.base_request_test(test.get_backend().courses_groups_memberships_list, test_cases,
            actual_clean_func = _clean_result,
            expected_clean_func = _clean_result)
