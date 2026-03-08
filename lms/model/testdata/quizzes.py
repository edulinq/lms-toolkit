import typing

import lms.model.quizzes

# {course_name: {name: quiz, ...}, ...}
COURSE_QUIZZES: typing.Dict[str, typing.Dict[str, lms.model.quizzes.Quiz]] = {}

# pylint: disable=line-too-long
COURSE_QUIZZES['Course 101'] = {
    'Regular Expressions': lms.model.quizzes.Quiz(
        id = '110000200',
        name = 'Regular Expressions',
        points_possible = 0.0,
        description = '<p></p><div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">This quiz is open note, open book, and open world. Assume all regular expressions are done in Python using the <code style=\"margin-left: 0.25em; margin-right: 0.25em\">re</code> standard library. Good luck!</p></div><p></p><br><hr><p>Version: UNKNOWN</p>'
    ),
}
