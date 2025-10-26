import typing

import lms.model.groups

# {course_name: {name: group, ...}, ...}
COURSE_GROUPS: typing.Dict[str, typing.Dict[str, lms.model.groups.Group]] = {}

COURSE_GROUPS['Extra Course'] = {
    'Group 1-1': lms.model.groups.Group(
        id = '101',
        name = 'Group 1-1',
    ),
    'Group 1-2': lms.model.groups.Group(
        id = '102',
        name = 'Group 1-2',
    ),
    'Group 2-1': lms.model.groups.Group(
        id = '201',
        name = 'Group 2-1',
    ),
    'Group 2-2': lms.model.groups.Group(
        id = '202',
        name = 'Group 2-2',
    ),
}
