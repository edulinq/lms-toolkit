import typing

import lms.model.assignments

# {course_name: {name: quiz, ...}, ...}
COURSE_QUIZZES: typing.Dict[str, typing.Dict[str, lms.model.assignments.Assignment]] = {}

# pylint: disable=line-too-long
COURSE_QUIZZES['Course 101'] = {
    'Regular Expressions': lms.model.assignments.Assignment(
        id = '110000200',
        name = 'Regular Expressions',
        points_possible = 0.0,
        description = "This quiz is open note, open book, and open world. Assume all regular expressions are done in Python using the `re` standard library. Good luck!\n\n  \n\n\n* * *\n\nVersion: UNKNOWN",
    ),
}
