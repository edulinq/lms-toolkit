import typing

import lms.model.groupsets

# {course_name: {name: groupset, ...}, ...}
COURSE_GROUPSETS: typing.Dict[str, typing.Dict[str, lms.model.groupsets.GroupSet]] = {}

COURSE_GROUPSETS['Extra Course'] = {
    'Group Set 1': lms.model.groupsets.GroupSet(
        id = '100',
        name = 'Group Set 1',
    ),
    'Group Set 2': lms.model.groupsets.GroupSet(
        id = '200',
        name = 'Group Set 2',
    ),
}
