import typing

import lms.model.assignments

# {course_name: {name: assignment, ...}, ...}
COURSE_ASSIGNMENTS: typing.Dict[str, typing.Dict[str, lms.model.assignments.Assignment]] = {}

COURSE_ASSIGNMENTS['Course 101'] = {
    'Homework 0': lms.model.assignments.Assignment(
        id = '1',
        name = 'Homework 0',
        points_possible = 2.0,
        position = 1,
        group_id = '1',
    ),
}

COURSE_ASSIGNMENTS['Course Using Different Languages'] = {
    'A Simple Bash Assignment': lms.model.assignments.Assignment(
        id = '2',
        name = 'A Simple Bash Assignment',
        points_possible = 10.0,
        position = 1,
        group_id = '2'
    ),
    'A Simple C++ Assignment': lms.model.assignments.Assignment(
        id = '3',
        name = 'A Simple C++ Assignment',
        points_possible = 10.0,
        position = 2,
        group_id = '2'
    ),
    'A Simple Java Assignment': lms.model.assignments.Assignment(
        id = '4',
        name = 'A Simple Java Assignment',
        points_possible = 10.0,
        position = 3,
        group_id = '2'
    ),
}

COURSE_ASSIGNMENTS['Extra Course'] = {
    'Assignment 1': lms.model.assignments.Assignment(
        id = '5',
        name = 'Assignment 1',
        points_possible = 10.0,
        position = 1,
        group_id = '3',
    ),
    'Assignment 2': lms.model.assignments.Assignment(
        id = '6',
        name = 'Assignment 2',
        points_possible = 20.0,
        position = 2,
        group_id = '3',
    ),
    'Assignment 3': lms.model.assignments.Assignment(
        id = '7',
        name = 'Assignment 3',
        points_possible = 30.0,
        position = 3,
        group_id = '3',
    ),
}
