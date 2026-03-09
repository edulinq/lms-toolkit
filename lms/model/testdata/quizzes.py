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
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">Taking inspiration from the XKCD comic below,\nhow would you save the day using regular expressions?</p><div class=\"qg-block\" style=\"display: flex; flex-direction: column; justify-content: flex-start; align-items: center\"><p style=\"margin-top: 0\"><img src=\"http://127.0.0.1:3000/courses/110000000/files/1/preview\" alt=\"XKCD Comic 208\" width=\"100.00%\" loading=\"lazy\" data-api-endpoint=\"http://127.0.0.1:3000/api/v1/courses/110000000/files/1\" data-api-returntype=\"File\"></p></div></div>",
    ),
    'Regular Expression in Programming Languages': lms.model.quizzes.Question(
        id = '110000202',
        question_type = quizcomp.question.base.QuestionType.TF,
        name = 'Regular Expression in Programming Languages',
        points = 1.0,
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">Regular expressions are implemented as either a core feature or in the standard library of almost every major programming language.</p></div>",
    ),
    'Regular Expression Vocabulary': lms.model.quizzes.Question(
        id = '110000203',
        question_type = quizcomp.question.base.QuestionType.MATCHING,
        name = 'Regular Expression Vocabulary',
        points = 1.0,
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">Match the following terms to their corresponding definitions.</p></div>",
    ),
    'Basic Regular Expressions': lms.model.quizzes.Question(
        id = '110000204',
        question_type = quizcomp.question.base.QuestionType.MCQ,
        name = 'Basic Regular Expressions',
        points = 1.0,
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">Which of the following regular expressions would be best to match a 10-digit phone number formatted as: '123 456-7890'. (Assume any stretch of continuous whitespace is a single space character.)</p></div>",
    ),
    'Question': lms.model.quizzes.Question(
        id = '110000205',
        question_type = quizcomp.question.base.QuestionType.TEXT_ONLY,
        name = 'Question',
        points = 0.0,
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">Below is the opening paragraph (which is actually just one sentence) from\n<em>A Tale Of Two Cities</em> written by Charles Dickens.\nFuture questions may reference this passage as \"the provided passage\".</p><p style=\"margin-top: 0\">\"It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness,\nit was the epoch of belief, it was the epoch of incredulity, it was the season of Light,\nit was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us,\nwe had nothing before us, we were all going direct to Heaven, we were all going direct the other way\n\u2014 in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received,\nfor good or for evil, in the superlative degree of comparison only.\"</p></div>",
    ),
    'Passage Search': lms.model.quizzes.Question(
        id = '110000206',
        question_type = quizcomp.question.base.QuestionType.NUMERICAL,
        name = 'Passage Search',
        points = 1.0,
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">In the provided passage, how many non-specific time periods are mentioned,\ni.e., how many matches are there for the following regular expression:</p><pre><code class=\"language-python\">r'(age|season|epoch)\\s+of\\s+(\\w+)'\n</code></pre></div>",
    ),
    'Quantifiers': lms.model.quizzes.Question(
        id = '110000207',
        question_type = quizcomp.question.base.QuestionType.MDD,
        name = 'Quantifiers',
        points = 1.0,
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">For each scenario, select the quantifier that is most appropriate.</p><p style=\"margin-top: 0\">You want to match the leading zeros for some number. E.g., \"00\" for \"005\".<br>\n\n[PART1]</p><p style=\"margin-top: 0\">You want to match the negative sign for some number. E.g., \"-\" for \"-9\".<br>\n\n[PART2]</p><p style=\"margin-top: 0\">You want to match the main digits (before any decimal point) for a required number,\ne.g., \"123\" for \"123\".<br>\n\n[PART3]</p></div>",
    ),
    'General Quantification 1': lms.model.quizzes.Question(
        id = '110000208',
        question_type = quizcomp.question.base.QuestionType.MA,
        name = 'General Quantification',
        points = 1.0,
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">Which of the following does the regex <code style=\"margin-left: 0.25em; margin-right: 0.25em\">r'Lo{2,3}ng Cat'</code> match? Select all that apply.</p></div>",
    ),
    'General Quantification 2': lms.model.quizzes.Question(
        id = '110000209',
        question_type = quizcomp.question.base.QuestionType.MA,
        name = 'General Quantification',
        points = 1.0,
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">Which of the following does the regex <code style=\"margin-left: 0.25em; margin-right: 0.25em\">r'I'm So{3,4} Hungry!'</code> match? Select all that apply.</p></div>",
    ),
    'Backreference Matching': lms.model.quizzes.Question(
        id = '110000210',
        question_type = quizcomp.question.base.QuestionType.FIMB,
        name = 'Backreference Matching',
        points = 1.0,
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">Suppose that we are trying to write a script extract name information from text and put it into a CSV (comma-separated value) file.\nThe order of the columns in our CSV file are: first name, last name, and title.\nAs part of our script, we have a regular expression that looks for people that have their name's written as \"last, first\".</p><pre><code class=\"language-python\">import re\n\ndef create_csv_line(text_line):\n    regex = r'^\\s*((Dr).?)?\\s*([^,]+)\\s*,\\s*(.+)\\s*$'\n    replacement = MY_REPLACEMENT_STRING\n\n    return re.sub(regex, replacement, text_line)\n</code></pre><p style=\"margin-top: 0\">Fill in the blanks in <code style=\"margin-left: 0.25em; margin-right: 0.25em\">MY_REPLACEMENT_STRING</code> to make the above code work correctly.</p><p style=\"margin-top: 0\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">MY_REPLACEMENT_STRING = r'</code>[A]<code style=\"margin-left: 0.25em; margin-right: 0.25em\">,</code>[B]<code style=\"margin-left: 0.25em; margin-right: 0.25em\">,</code>[C]<code style=\"margin-left: 0.25em; margin-right: 0.25em\">'</code></p></div>",
    ),
    'Regex Golf': lms.model.quizzes.Question(
        id = '110000211',
        question_type = quizcomp.question.base.QuestionType.FITB,
        name = 'Regex Golf',
        points = 1.0,
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">Create a regular expression that matches successfully completes a game a golf with the table below.</p><p style=\"margin-top: 0\">Specifics:</p><ul><li>Match all values in the <code style=\"margin-left: 0.25em; margin-right: 0.25em\">Match</code> column.</li><li>Do not match any values in the <code style=\"margin-left: 0.25em; margin-right: 0.25em\">No Match</code> column.</li><li>Write you regex as a raw string using a single or double quotes (not triple quotes).</li><li>Treat the contents of each table cell as a string (so you do not have the match the quotes).</li><li>You may assume that any contiguous whitespace is a single space character.</li><li>You only need to match (or not match) the values in the table, you do not need to extend this pattern to unseen values.</li></ul><table style=\"border-collapse: collapse; border-style: hidden\"><thead style=\"border-bottom: 1px solid black\"><tr><th style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em; \">Match</th><th style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em; \">No Match</th></tr></thead><tbody><tr><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'12:00 AM'</code></td><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'00:00'</code></td></tr><tr><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'05:30 PM'</code></td><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'17:30'</code></td></tr><tr><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'01:45 AM'</code></td><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'01:65 AM'</code></td></tr><tr><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'10:10 PM'</code></td><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'10:10 ZZ'</code></td></tr><tr><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'12:34 PM'</code></td><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'12:34 pm'</code></td></tr><tr><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'11:59 PM'</code></td><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'23:59'</code></td></tr><tr><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"></td><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'123:45 AM'</code></td></tr><tr><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"></td><td style=\"padding-top: 0.25em; padding-bottom: 0.25em; padding-left: 0.25em; padding-right: 0.25em\"><code style=\"margin-left: 0.25em; margin-right: 0.25em\">'12:345 PM'</code></td></tr></tbody></table></div>",
    ),
    'Write a Function': lms.model.quizzes.Question(
        id = '110000212',
        question_type = quizcomp.question.base.QuestionType.ESSAY,
        name = 'Write a Function',
        points = 1.0,
        prompt = "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">Implement a function with the following signature and description:</p><pre><code>import re\n\ndef compute(text):\n    \"\"\"\n    Compute the result of the binary expression represented in the |text| variable.\n    The possible operators are: \"+\", \"-\", \"*\", and \"/\".\n    Operands may be any real number.\n    If the operation is division, the RHS (denominator) will not be zero.\n    \"\"\"\n\n    return NotImplemented\n</code></pre><p style=\"margin-top: 0\">Specifics:</p><ul><li>Your function must use regular expressions.</li><li>You may not use <code style=\"margin-left: 0.25em; margin-right: 0.25em\">eval()</code> or any other Python ast functionality.</li><li>You may only import modules from the Python standard library.</li><li>You should return a float that is the result of the binary operation represented by <code style=\"margin-left: 0.25em; margin-right: 0.25em\">text</code>.</li><li>The operator will be one of:  <span style=\"margin-left: 0.25em; margin-right: 0.25em\"><span class=\"katex\"><math xmlns=\"http://www.w3.org/1998/Math/MathML\"><semantics><mrow><mo stretchy=\"false\">{</mo><mo>+</mo><mo separator=\"true\">,</mo><mo>\u2212</mo><mo separator=\"true\">,</mo><mo>\u2217</mo><mo separator=\"true\">,</mo><mi mathvariant=\"normal\">/</mi><mo stretchy=\"false\">}</mo></mrow><annotation encoding=\"application/x-tex\">\\{+, -, *, /\\}</annotation></semantics></math></span></span>.</li><li>Operands may be any real number.</li></ul></div>",
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
