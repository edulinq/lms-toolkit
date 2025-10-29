import typing

import lms.model.assignments

# {course_name: {name: assignment, ...}, ...}
COURSE_ASSIGNMENTS: typing.Dict[str, typing.Dict[str, lms.model.assignments.Assignment]] = {}

COURSE_ASSIGNMENTS['Course 101'] = {
    'Homework 0': lms.model.assignments.Assignment(
        id = '110000100',
        name = 'Homework 0',
        points_possible = 2.0,
    ),
}

COURSE_ASSIGNMENTS['Course Using Different Languages'] = {
    'A Simple Bash Assignment': lms.model.assignments.Assignment(
        id = '120000100',
        name = 'A Simple Bash Assignment',
        points_possible = 10.0,
    ),
    'A Simple C++ Assignment': lms.model.assignments.Assignment(
        id = '120000200',
        name = 'A Simple C++ Assignment',
        points_possible = 10.0,
    ),
    'A Simple Java Assignment': lms.model.assignments.Assignment(
        id = '120000300',
        name = 'A Simple Java Assignment',
        points_possible = 10.0,
    ),
}

COURSE_ASSIGNMENTS['Extra Course'] = {
    'Assignment 1': lms.model.assignments.Assignment(
        id = '130000100',
        name = 'Assignment 1',
        points_possible = 10.0,
    ),
    'Assignment 2': lms.model.assignments.Assignment(
        id = '130000200',
        name = 'Assignment 2',
        points_possible = 20.0,
    ),
    'Assignment 3': lms.model.assignments.Assignment(
        id = '130000300',
        name = 'Assignment 3',
        points_possible = 30.0,
    ),
}
