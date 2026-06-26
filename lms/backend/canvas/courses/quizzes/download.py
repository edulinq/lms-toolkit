import logging
import typing

import quizcomp.model.answer
import quizcomp.model.constants
import quizcomp.model.group
import quizcomp.model.question
import quizcomp.model.quiz
import quizcomp.parser.document

import lms.backend.canvas.common
import lms.model.constants

_logger = logging.getLogger(__name__)

LIST_GROUPS_ENDPOINT = "/api/v1/courses/{course_id}/quizzes/{quiz_id}/groups"
LIST_QUESTIONS_ENDPOINT = "/api/v1/courses/{course_id}/quizzes/{quiz_id}/questions?per_page={page_size}"

QUESTION_TYPE_MAP: typing.Dict[str, quizcomp.model.constants.QuestionType] = {
    'essay_question': quizcomp.model.constants.QuestionType.ESSAY,
    'fill_in_multiple_blanks_question': quizcomp.model.constants.QuestionType.FIMB,
    'matching_question': quizcomp.model.constants.QuestionType.MATCHING,
    'multiple_answers_question': quizcomp.model.constants.QuestionType.MA,
    'multiple_choice_question': quizcomp.model.constants.QuestionType.MCQ,
    'multiple_dropdowns_question': quizcomp.model.constants.QuestionType.MDD,
    'numerical_question': quizcomp.model.constants.QuestionType.NUMERICAL,
    'short_answer_question': quizcomp.model.constants.QuestionType.FITB,
    'text_only_question': quizcomp.model.constants.QuestionType.TEXT_ONLY,
    'true_false_question': quizcomp.model.constants.QuestionType.TF,
}

DISALLOWED_QUESTION_TYPES: typing.Set[str] = {
    'calculated_question',
    'file_upload_question',
}

# TEST - Rewrite image links.

def request(
        backend: typing.Any,
        course_id: int,
        quiz_id: int,
        ) -> quizcomp.model.quiz.Quiz:
    """ Download a quiz. """

    quiz_metadata = backend.courses_quizzes_fetch(str(course_id), str(quiz_id))
    if (quiz_metadata is None):
        raise ValueError(f"Unable to fetch quiz metadata for quiz ID '{quiz_id}'.")

    # TEST - Do questions first and form groups with questions.

    questions = _list_questions(backend, course_id, quiz_id)

    groups = _list_groups(backend, course_id, quiz_id, questions)

    # TEST
    return quizcomp.model.quiz.Quiz(name = 'TEST', children = groups)

    ''' TEST
    url = backend.server + BASE_ENDPOINT.format(course_id = course_id, quiz_id = quiz_id)
    headers = backend.get_standard_headers()

    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    lms.backend.canvas.common.make_delete_request(url, headers = headers)
    '''

def _list_groups(
        backend: typing.Any,
        course_id: int,
        quiz_id: int,
        questions: typing.Dict[int, quizcomp.model.question.Question],
        ) -> typing.List[quizcomp.model.group.Group]:
    """ List quiz question groups. """

    url = backend.server + LIST_GROUPS_ENDPOINT.format(course_id = course_id, quiz_id = quiz_id)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
            'quiz_id': quiz_id,
        }
        backend.not_found('list quiz question groups', identifiers)

        return []

    groups = []
    for raw_group in raw_objects.get('quiz_groups', []):
        groups.append(quizcomp.model.group.Group(
            name = raw_group['name'],
            children = questions.get(raw_group['id'], []),
            lms_id = str(raw_group['id']),
            pick_count = raw_group['pick_count'],
            position = raw_group['position'],
            points = raw_group['pick_count'] * raw_group['question_points'],
        ))

    return groups

def _list_questions(
        backend: typing.Any,
        course_id: int,
        quiz_id: int,
        ) -> typing.List[quizcomp.model.question.Question]:
    """ List quiz questions. """

    url = backend.server + LIST_QUESTIONS_ENDPOINT.format(course_id = course_id, quiz_id = quiz_id, page_size = lms.backend.canvas.common.DEFAULT_PAGE_SIZE)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
            'quiz_id': quiz_id,
        }
        backend.not_found('list quiz questions', identifiers)

        return {}

    questions = {}
    for raw_question in raw_objects:
        raw_question_type = raw_question['question_type']
        if (raw_question_type in DISALLOWED_QUESTION_TYPES):
            _logger.warning("Found question ('%s') with disallowed question type '%s', skipping download of that question.", raw_question['question_name'], raw_question_type)
            continue

        if (raw_question_type not in QUESTION_TYPE_MAP):
            _logger.warning("Found question ('%s') with unknown question type '%s', skipping download of that question.", raw_question['question_name'], raw_question_type)
            continue

        question_type = QUESTION_TYPE_MAP[raw_question_type]

        prompt_text = lms.backend.canvas.common.html_to_markdown(raw_question['question_text'])

        question = quizcomp.model.question.Question(
            lms_id = raw_question['id'],
            name = raw_question['question_name'],
            question_type = question_type,
            prompt = quizcomp.parser.document.ParsedDocument.parse_text(prompt_text),
            points = raw_question['points_possible'],
            feedback = _parse_raw_feedback(raw_question),
            answers = _parse_answers(question_type, raw_question),
        )

        group_id = raw_question['quiz_group_id']
        if (group_id not in questions):
            questions[group_id] = []

        questions[group_id].append(question)

    return questions

    # TEST
    print('---')
    import edq.util.json
    print(edq.util.json.dumps(raw_objects, indent = 4))
    print('---')
    return {}

def _parse_raw_feedback(raw_question: typing.Dict[str, typing.Any]) -> typing.Union[quizcomp.model.feedback.Feedback, None]:
    """ Try to parse feedback our of a raw question. """

    parts = {
        'general': ('neutral_comments', 'neutral_comments_html'),
        'correct': ('correct_comments', 'correct_comments_html'),
        'incorrect': ('incorrect_comments', 'incorrect_comments_html'),
    }

    feedback_kwargs = {}
    for (feedback_type, (text_key, html_key)) in parts.items():
        text_value = raw_question.get(text_key, None)
        if (text_value is None):
            text_value = ''

        text_value = str(text_value).strip()
        if (len(text_value) != 0):
            feedback_kwargs[feedback_type] = quizcomp.parser.document.ParsedDocument.parse_text(text_value)
            continue

        html_value = raw_question.get(html_key, None)
        if (html_value is None):
            html_value = ''

        html_value = str(html_value).strip()
        if (len(html_value) != 0):
            text = lms.backend.canvas.common.html_to_markdown(html_value)
            feedback_kwargs[feedback_type] = quizcomp.parser.document.ParsedDocument.parse_text(text)

    feedback = quizcomp.model.feedback.Feedback(**feedback_kwargs)
    if (feedback.is_empty()):
        return None

    return feedback

# TEST
'''
    {
        "answer_tolerance": null,
        "answers": [],
        "assessment_question_id": 110000201,
        "correct_comments": "",
        "correct_comments_html": "",
        "created_at": "2026-06-12T14:07:28Z",
        "formula_decimal_places": null,
        "formulas": null,
        "id": 110000201,
        "incorrect_comments": "",
        "incorrect_comments_html": "",
        "matches": null,
        "matching_answer_incorrect_matches": null,
        "neutral_comments": "",
        "neutral_comments_html": "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">You can have any answer you want.</p></div>",
        "points_possible": 1.0,
        "position": null,
        "question_name": "Ice Breaker",
        "question_text": "<div class=\"qg-root-block qg-block\"><p style=\"margin-top: 0\">Taking inspiration from the XKCD comic below,\nhow would you save the day using regular expressions?</p><div class=\"qg-block\" style=\"display: flex; flex-direction: column; justify-content: flex-start; align-items: center\"><p style=\"margin-top: 0\"><img src=\"http://127.0.0.1:3000/courses/110000000/files/1/preview\" alt=\"XKCD Comic 208\" width=\"100.00%\" loading=\"lazy\" data-api-endpoint=\"http://127.0.0.1:3000/api/v1/courses/110000000/files/1\" data-api-returntype=\"File\"></p></div></div>",
        "question_type": "essay_question",
        "quiz_group_id": 110000201,
        "quiz_id": 110000200,
        "variables": null
    },
'''

def _parse_answers(
        question_type: quizcomp.model.constants.QuestionType,
        raw_question: typing.Dict[str, typing.Any],
        ) -> quizcomp.model.answer.QuestionAnswers:
    """ Parse a question's answer from the raw question. """

    if (question_type is quizcomp.model.constants.QuestionType.ESSAY):
        # TEST
        pass
    elif (question_type is quizcomp.model.constants.QuestionType.FIMB):
        # TEST
        pass
    elif (question_type is quizcomp.model.constants.QuestionType.FITB):
        # TEST
        pass
    elif (question_type is quizcomp.model.constants.QuestionType.MATCHING):
        # TEST
        pass
    elif (question_type is quizcomp.model.constants.QuestionType.MA):
        # TEST
        pass
    elif (question_type is quizcomp.model.constants.QuestionType.MCQ):
        # TEST
        pass
    elif (question_type is quizcomp.model.constants.QuestionType.MDD):
        # TEST
        pass
    elif (question_type is quizcomp.model.constants.QuestionType.NUMERICAL):
        # TEST
        pass
    elif (question_type is quizcomp.model.constants.QuestionType.TEXT_ONLY):
        # TEST
        pass
    elif (question_type is quizcomp.model.constants.QuestionType.TF):
        # TEST
        pass
    else:
        raise ValueError(f"Unknown question type: '{question_type.value}'.")

    # TEST
    print('---')
    import edq.util.json
    print(edq.util.json.dumps(raw_question, indent = 4))
    print('---')
    return quizcomp.model.answer.TextAnswers()
