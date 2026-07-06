import os
import typing

import quizcomp.model.quiz

import lms.model.assignments

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..', '..')
# TEST
# QUIZ_PATH: str = os.path.join(ROOT_DIR, 'testdata', 'lms-docker-canvas-testdata',
#                               'lms-testdata', 'cse-cracks-course', 'quizzes', 'regex', 'quiz.json')
# QUIZ_PATH: str = '/home/eriq/code/cse-cracks-course/quizzes/regex/quiz.json'
QUIZ_PATH: str = '/home/eriq/code/quiz-composer/testdata/cse-cracks-course/quizzes/regex/quiz.json'

# {course_name: {name: quiz metadata, ...}, ...}
COURSE_QUIZZES_METADATA: typing.Dict[str, typing.Dict[str, lms.model.assignments.Assignment]] = {}

# {course_name: {name: quiz, ...}, ...}
COURSE_QUIZZES: typing.Dict[str, typing.Dict[str, quizcomp.model.quiz.Quiz]] = {}

COURSE_QUIZZES_METADATA['Course 101'] = {
    'Regular Expressions': lms.model.assignments.Assignment(
        id = '110000200',
        name = 'Regular Expressions',
        points_possible = 0.0,
        description = (
            'This quiz is open note, open book, and open world.'
            + ' Assume all regular expressions are done in Python using the `re` standard library.'
            + " Good luck!\n\n  \n\n\n* * *\n\nVersion: UNKNOWN"
        ),
    ),
}

COURSE_QUIZZES['Course 101'] = {
    'Regular Expressions': quizcomp.model.quiz.Quiz.from_path(QUIZ_PATH),
}
