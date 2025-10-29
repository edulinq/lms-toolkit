import copy

import lms.backend.testing
import lms.model.testdata.groups

def test_courses_groups_memberships_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing group memberships. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
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

    # Strip down the queries (which may be partially resolved).
    def _clean_result(result):
        result = copy.deepcopy(result)

        for item in result:
            item.groupset.name = None
            item.group.name = None
            item.user.name = None
            item.user.email = None

        return result

    test.base_request_test(test.backend.courses_groups_memberships_list, test_cases,
            actual_clean_func = _clean_result,
            expected_clean_func = _clean_result)
