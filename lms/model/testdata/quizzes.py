import typing

import lms.model.quizzes

# {course_name: {name: quiz, ...}, ...}
COURSE_QUIZZES: typing.Dict[str, typing.Dict[str, lms.model.quizzes.Quiz]] = {}

# {quiz_name: {name: question, ...}, ...}
QUIZ_QUESTIONS: typing.Dict[str, typing.Dict[str, lms.model.quizzes.Question]] = {}

# {quiz_name: [question, ...], ...}
ORDERED_QUIZ_QUESTIONS: typing.Dict[str, typing.List[lms.model.quizzes.Question]] = {}

# pylint: disable=line-too-long
COURSE_QUIZZES['Course 101'] = {
    'Regular Expressions': lms.model.quizzes.Quiz(
        id = '110000200',
        name = 'Regular Expressions',
        points_possible = 0.0,
        description = '<p></p><div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">This quiz is open note, open book, and open world. Assume all regular expressions are done in Python using the <code style=\"margin-left: 0.25em; margin-right: 0.25em\">re</code> standard library. Good luck!</p></div><p></p><br><hr><p>Version: UNKNOWN</p>'
    ),
}

QUIZ_QUESTIONS['Regular Expressions'] = {
    'Ice Breaker': lms.model.quizzes.Question(
        id = '110000201',
        name = 'Ice Breaker',
    ),
    'Regular Expression in Programming Languages': lms.model.quizzes.Question(
        id = '110000202',
        name = 'Regular Expression in Programming Languages',
    ),
    'Regular Expression Vocabulary': lms.model.quizzes.Question(
        id = '110000203',
        name = 'Regular Expression Vocabulary',
    ),
    'Basic Regular Expressions': lms.model.quizzes.Question(
        id = '110000204',
        name = 'Basic Regular Expressions',
    ),
    'Question': lms.model.quizzes.Question(
        id = '110000205',
        name = 'Question',
    ),
    'Passage Search': lms.model.quizzes.Question(
        id = '110000206',
        name = 'Passage Search',
    ),
    'Quantifiers': lms.model.quizzes.Question(
        id = '110000207',
        name = 'Quantifiers',
    ),
    'General Quantification 1': lms.model.quizzes.Question(
        id = '110000208',
        name = 'General Quantification',
    ),
    'General Quantification 2': lms.model.quizzes.Question(
        id = '110000209',
        name = 'General Quantification',
    ),
    'Backreference Matching': lms.model.quizzes.Question(
        id = '110000210',
        name = 'Backreference Matching',
    ),
    'Regex Golf': lms.model.quizzes.Question(
        id = '110000211',
        name = 'Regex Golf',
    ),
    'Write a Function': lms.model.quizzes.Question(
        id = '110000212',
        name = 'Write a Function',
    ),
}

ORDERED_QUIZ_QUESTIONS['Regular Expressions'] = [
    QUIZ_QUESTIONS['Regular Expressions']['Ice Breaker'],
    QUIZ_QUESTIONS['Regular Expressions']['Regular Expression in Programming Languages'],
    QUIZ_QUESTIONS['Regular Expressions']['Regular Expression Vocabulary'],
    QUIZ_QUESTIONS['Regular Expressions']['Basic Regular Expressions'],
    QUIZ_QUESTIONS['Regular Expressions']['Question'],
    QUIZ_QUESTIONS['Regular Expressions']['Passage Search'],
    QUIZ_QUESTIONS['Regular Expressions']['Quantifiers'],
    QUIZ_QUESTIONS['Regular Expressions']['General Quantification 1'],
    QUIZ_QUESTIONS['Regular Expressions']['General Quantification 2'],
    QUIZ_QUESTIONS['Regular Expressions']['Backreference Matching'],
    QUIZ_QUESTIONS['Regular Expressions']['Regex Golf'],
    QUIZ_QUESTIONS['Regular Expressions']['Write a Function'],
]
