import typing

import quizcomp.question.base

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
        question_type = quizcomp.question.base.QuestionType.ESSAY,
        name = 'Ice Breaker',
        points = 1.0,
        prompt = "Taking inspiration from the XKCD comic below, how would you save the day using regular expressions?\n\n![XKCD Comic 208](http://127.0.0.1:3000/courses/110000000/files/1/preview)",
    ),
    'Regular Expression in Programming Languages': lms.model.quizzes.Question(
        id = '110000202',
        question_type = quizcomp.question.base.QuestionType.TF,
        name = 'Regular Expression in Programming Languages',
        points = 1.0,
        prompt = "Regular expressions are implemented as either a core feature or in the standard library of almost every major programming language.",
    ),
    'Regular Expression Vocabulary': lms.model.quizzes.Question(
        id = '110000203',
        question_type = quizcomp.question.base.QuestionType.MATCHING,
        name = 'Regular Expression Vocabulary',
        points = 1.0,
        prompt = "Match the following terms to their corresponding definitions.",
    ),
    'Basic Regular Expressions': lms.model.quizzes.Question(
        id = '110000204',
        question_type = quizcomp.question.base.QuestionType.MCQ,
        name = 'Basic Regular Expressions',
        points = 1.0,
        prompt = "Which of the following regular expressions would be best to match a 10-digit phone number formatted as: '123 456-7890'. (Assume any stretch of continuous whitespace is a single space character.)",
    ),
    'Question': lms.model.quizzes.Question(
        id = '110000205',
        question_type = quizcomp.question.base.QuestionType.TEXT_ONLY,
        name = 'Question',
        points = 0.0,
        prompt = "Below is the opening paragraph (which is actually just one sentence) from _A Tale Of Two Cities_ written by Charles Dickens. Future questions may reference this passage as \"the provided passage\".\n\n\"It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way \u2014 in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only.\"",
    ),
    'Passage Search': lms.model.quizzes.Question(
        id = '110000206',
        question_type = quizcomp.question.base.QuestionType.NUMERICAL,
        name = 'Passage Search',
        points = 1.0,
        prompt = "In the provided passage, how many non-specific time periods are mentioned, i.e., how many matches are there for the following regular expression:\n```\n    r'(age|season|epoch)\\s+of\\s+(\\w+)'\n    \n```",
    ),
    'Quantifiers': lms.model.quizzes.Question(
        id = '110000207',
        question_type = quizcomp.question.base.QuestionType.MDD,
        name = 'Quantifiers',
        points = 1.0,
        prompt = "For each scenario, select the quantifier that is most appropriate.\n\nYou want to match the leading zeros for some number. E.g., \"00\" for \"005\".  \n<placeholder>PART1</placeholder>\n\nYou want to match the negative sign for some number. E.g., \"-\" for \"-9\".  \n<placeholder>PART2</placeholder>\n\nYou want to match the main digits (before any decimal point) for a required number, e.g., \"123\" for \"123\".  \n<placeholder>PART3</placeholder>",
    ),
    'General Quantification 1': lms.model.quizzes.Question(
        id = '110000208',
        question_type = quizcomp.question.base.QuestionType.MA,
        name = 'General Quantification',
        points = 1.0,
        prompt = "Which of the following does the regex `r'Lo{2,3}ng Cat'` match? Select all that apply.",
    ),
    'General Quantification 2': lms.model.quizzes.Question(
        id = '110000209',
        question_type = quizcomp.question.base.QuestionType.MA,
        name = 'General Quantification',
        points = 1.0,
        prompt = "Which of the following does the regex `r'I'm So{3,4} Hungry!'` match? Select all that apply.",
    ),
    'Backreference Matching': lms.model.quizzes.Question(
        id = '110000210',
        question_type = quizcomp.question.base.QuestionType.FIMB,
        name = 'Backreference Matching',
        points = 1.0,
        prompt = "Suppose that we are trying to write a script extract name information from text and put it into a CSV (comma-separated value) file. The order of the columns in our CSV file are: first name, last name, and title. As part of our script, we have a regular expression that looks for people that have their name's written as \"last, first\".\n```\n    import re\n    \n    def create_csv_line(text_line):\n        regex = r'^\\s*((Dr).?)?\\s*([^,]+)\\s*,\\s*(.+)\\s*$'\n        replacement = MY_REPLACEMENT_STRING\n    \n        return re.sub(regex, replacement, text_line)\n    \n```\n\nFill in the blanks in `MY_REPLACEMENT_STRING` to make the above code work correctly.\n\n`MY_REPLACEMENT_STRING = r'`<placeholder>A</placeholder>`,`<placeholder>B</placeholder>`,`<placeholder>C</placeholder>`'`",
    ),
    'Regex Golf': lms.model.quizzes.Question(
        id = '110000211',
        question_type = quizcomp.question.base.QuestionType.FITB,
        name = 'Regex Golf',
        points = 1.0,
        prompt = "Create a regular expression that matches successfully completes a game a golf with the table below.\n\nSpecifics:\n\n  * Match all values in the `Match` column.\n  * Do not match any values in the `No Match` column.\n  * Write you regex as a raw string using a single or double quotes (not triple quotes).\n  * Treat the contents of each table cell as a string (so you do not have the match the quotes).\n  * You may assume that any contiguous whitespace is a single space character.\n  * You only need to match (or not match) the values in the table, you do not need to extend this pattern to unseen values.\n\nMatch| No Match  \n---|---  \n`'12:00 AM'`| `'00:00'`  \n`'05:30 PM'`| `'17:30'`  \n`'01:45 AM'`| `'01:65 AM'`  \n`'10:10 PM'`| `'10:10 ZZ'`  \n`'12:34 PM'`| `'12:34 pm'`  \n`'11:59 PM'`| `'23:59'`  \n| `'123:45 AM'`  \n| `'12:345 PM'`",
    ),
    'Write a Function': lms.model.quizzes.Question(
        id = '110000212',
        question_type = quizcomp.question.base.QuestionType.ESSAY,
        name = 'Write a Function',
        points = 1.0,
        prompt = "Implement a function with the following signature and description:\n```\n    import re\n    \n    def compute(text):\n        \"\"\"\n        Compute the result of the binary expression represented in the |text| variable.\n        The possible operators are: \"+\", \"-\", \"*\", and \"/\".\n        Operands may be any real number.\n        If the operation is division, the RHS (denominator) will not be zero.\n        \"\"\"\n    \n        return NotImplemented\n    \n```\n\nSpecifics:\n\n  * Your function must use regular expressions.\n  * You may not use `eval()` or any other Python ast functionality.\n  * You may only import modules from the Python standard library.\n  * You should return a float that is the result of the binary operation represented by `text`.\n  * The operator will be one of: {+,\u2212,\u2217,/}\\\\{+, -, *, /\\\\}.\n  * Operands may be any real number.",
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
