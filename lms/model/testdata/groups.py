import typing

import lms.model.groups
import lms.model.groupsets
import lms.model.testdata.groupsets
import lms.model.testdata.users

# {course_name: {name: group, ...}, ...}
COURSE_GROUPS: typing.Dict[str, typing.Dict[str, lms.model.groups.Group]] = {}

COURSE_GROUPS['Extra Course'] = {
    'Group 1-1': lms.model.groups.Group(
        id = '131010101',
        name = 'Group 1-1',
    ),
    'Group 1-2': lms.model.groups.Group(
        id = '131010102',
        name = 'Group 1-2',
    ),
    'Group 2-1': lms.model.groups.Group(
        id = '131020201',
        name = 'Group 2-1',
    ),
    'Group 2-2': lms.model.groups.Group(
        id = '131020202',
        name = 'Group 2-2',
    ),
    'Group 3-1': lms.model.groups.Group(
        id = '131030301',
        name = 'Group 3-1',
    ),
}

# {course_name: {groupset_name: {user name: membership, ...}, ...}, ...}
COURSE_GROUP_MEMBERSHIPS: typing.Dict[str, typing.Dict[str, typing.Dict[str, lms.model.groupsets.GroupSetMembership]]] = {}

COURSE_GROUP_MEMBERSHIPS['Extra Course'] = {
    'Group Set 1': {
        'extra-course-student-1': lms.model.groupsets.GroupSetMembership(
            groupset = lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'].to_query(),
            group = COURSE_GROUPS['Extra Course']['Group 1-1'].to_query(),
            user = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-1'].to_query(),
        ),
        'extra-course-student-2': lms.model.groupsets.GroupSetMembership(
            groupset = lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'].to_query(),
            group = COURSE_GROUPS['Extra Course']['Group 1-1'].to_query(),
            user = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-2'].to_query(),
        ),
        'extra-course-student-3': lms.model.groupsets.GroupSetMembership(
            groupset = lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'].to_query(),
            group = COURSE_GROUPS['Extra Course']['Group 1-2'].to_query(),
            user = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-3'].to_query(),
        ),
        'extra-course-student-4': lms.model.groupsets.GroupSetMembership(
            groupset = lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'].to_query(),
            group = COURSE_GROUPS['Extra Course']['Group 1-2'].to_query(),
            user = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-4'].to_query(),
        ),
    },
    'Group Set 2': {
        'extra-course-student-1': lms.model.groupsets.GroupSetMembership(
            groupset = lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 2'].to_query(),
            group = COURSE_GROUPS['Extra Course']['Group 2-1'].to_query(),
            user = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-1'].to_query(),
        ),
        'extra-course-student-2': lms.model.groupsets.GroupSetMembership(
            groupset = lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 2'].to_query(),
            group = COURSE_GROUPS['Extra Course']['Group 2-2'].to_query(),
            user = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-2'].to_query(),
        ),
        'extra-course-student-3': lms.model.groupsets.GroupSetMembership(
            groupset = lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 2'].to_query(),
            group = COURSE_GROUPS['Extra Course']['Group 2-1'].to_query(),
            user = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-3'].to_query(),
        ),
        'extra-course-student-4': lms.model.groupsets.GroupSetMembership(
            groupset = lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 2'].to_query(),
            group = COURSE_GROUPS['Extra Course']['Group 2-2'].to_query(),
            user = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-4'].to_query(),
        ),
    },
}
