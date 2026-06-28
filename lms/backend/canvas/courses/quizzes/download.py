import logging
import math
import typing

import quizcomp.model.answer
import quizcomp.model.constants
import quizcomp.model.group
import quizcomp.model.question
import quizcomp.model.quiz
import quizcomp.parser.document

import lms.backend.canvas.common
import lms.backend.canvas.courses.quizzes.common
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

DEFAULT_BLANK_ID: str = ''

def request(
        backend: typing.Any,
        course_id: int,
        quiz_id: int,
        ) -> quizcomp.model.quiz.Quiz:
    """ Download a quiz. """

    quiz_metadata = backend.courses_quizzes_fetch(str(course_id), str(quiz_id))
    if (quiz_metadata is None):
        raise ValueError(f"Unable to fetch quiz metadata for quiz ID '{quiz_id}'.")

    questions = _list_questions(backend, course_id, quiz_id)
    groups = _list_groups(backend, course_id, quiz_id, questions)

    return quizcomp.model.quiz.Quiz(
        name = quiz_metadata.name,
        children = groups,
        description = quiz_metadata.description,
        time_limit_mins = quiz_metadata.extra_fields.get('time_limit', None),
        practice = (quiz_metadata.extra_fields.get('quiz_type', None) == lms.backend.canvas.courses.quizzes.common.QUIZ_TYPE_PRACTICE),
        publish = quiz_metadata.extra_fields.get('published', None),
        allowed_attempts = quiz_metadata.extra_fields.get('allowed_attempts', None),
        show_correct_answers = quiz_metadata.extra_fields.get('show_correct_answers', None),
        hide_results = quiz_metadata.extra_fields.get('hide_results', None),
        scoring_policy = quiz_metadata.extra_fields.get('scoring_policy', None),
    )

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
        ) -> typing.Dict[int, quizcomp.model.question.Question]:
    """ List quiz questions grouped by group id. """

    url = backend.server + LIST_QUESTIONS_ENDPOINT.format(
            course_id = course_id, quiz_id = quiz_id, page_size = lms.backend.canvas.common.DEFAULT_PAGE_SIZE)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
            'quiz_id': quiz_id,
        }
        backend.not_found('list quiz questions', identifiers)

        return {}

    questions: typing.Dict[int, quizcomp.model.question.Question] = {}
    for raw_question in raw_objects:
        raw_question_type = raw_question['question_type']
        if (raw_question_type in DISALLOWED_QUESTION_TYPES):
            _logger.warning("Found question ('%s') with disallowed question type '%s', skipping download of that question.",
                    raw_question['question_name'], raw_question_type)
            continue

        if (raw_question_type not in QUESTION_TYPE_MAP):
            _logger.warning("Found question ('%s') with unknown question type '%s', skipping download of that question.",
                    raw_question['question_name'], raw_question_type)
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

def _parse_raw_feedback(raw_question: typing.Dict[str, typing.Any]) -> typing.Union[quizcomp.model.feedback.Feedback, None]:
    """ Try to parse feedback our of a raw question. """

    parts = {
        'general': ('neutral_comments', 'neutral_comments_html'),
        'correct': ('correct_comments', 'correct_comments_html'),
        'incorrect': ('incorrect_comments', 'incorrect_comments_html'),
    }

    feedback_kwargs = {}
    for (feedback_type, (text_key, html_key)) in parts.items():
        feedback_kwargs[feedback_type] = _parse_text(raw_question, text_key, html_key)

    feedback = quizcomp.model.feedback.Feedback(**feedback_kwargs)
    if (feedback.is_empty()):
        return None

    return feedback

def _parse_text(
        raw_data: typing.Dict[str, typing.Any],
        text_key: str,
        html_key: str,
        default_text: typing.Union[str, None] = None,
        ) -> typing.Union[quizcomp.parser.document.ParsedDocument, None]:
    """
    Parse text from raw Canvas data.
    Canvas will often have both text and HTML fields (but only one will usually be filled).
    If both keys are provided, the text one will be check first (and returned if it has content).

    If no text is found and the default text is not None,
    then it will be parsed and returned.
    """

    text_value = raw_data.get(text_key, None)
    if (text_value is None):
        text_value = ''

    text_value = str(text_value).strip()
    if (len(text_value) != 0):
        return quizcomp.parser.document.ParsedDocument.parse_text(text_value)

    html_value = raw_data.get(html_key, None)
    if (html_value is None):
        html_value = ''

    html_value = str(html_value).strip()
    if (len(html_value) != 0):
        text = lms.backend.canvas.common.html_to_markdown(html_value)
        return quizcomp.parser.document.ParsedDocument.parse_text(text)

    if (default_text is not None):
        return quizcomp.parser.document.ParsedDocument.parse_text(default_text)

    return None

def _parse_answers(
        question_type: quizcomp.model.constants.QuestionType,
        raw_question: typing.Dict[str, typing.Any],
        ) -> quizcomp.model.answer.QuestionAnswers:
    """ Parse a question's answer from the raw question. """

    if (question_type is quizcomp.model.constants.QuestionType.ESSAY):
        # Canvas does not store potential answers (e.g., a rubric) for essay questions.
        return quizcomp.model.answer.TextAnswers()
    elif (question_type is quizcomp.model.constants.QuestionType.FIMB):
        parts = {}
        for (blank_id, choices) in _parse_choice_answers(raw_question['answers']).parts.items():
            options = [quizcomp.model.answer.TextOption(choice.text, choice.feedback) for choice in choices.choices]
            parts[blank_id] = quizcomp.model.answer.TextAnswers(options)

        return quizcomp.model.answer.MultiplePartTextAnswers(parts)
    elif (question_type is quizcomp.model.constants.QuestionType.FITB):
        choices = _parse_choice_answers(raw_question['answers']).parts[DEFAULT_BLANK_ID]
        options = [quizcomp.model.answer.TextOption(choice.text, choice.feedback) for choice in choices.choices]
        return quizcomp.model.answer.TextAnswers(options)
    elif (question_type is quizcomp.model.constants.QuestionType.MATCHING):
        return _parse_matching_answers(raw_question)
    elif (question_type is quizcomp.model.constants.QuestionType.MA):
        return _parse_choice_answers(raw_question['answers']).parts[DEFAULT_BLANK_ID]
    elif (question_type is quizcomp.model.constants.QuestionType.MCQ):
        return _parse_choice_answers(raw_question['answers']).parts[DEFAULT_BLANK_ID]
    elif (question_type is quizcomp.model.constants.QuestionType.MDD):
        return _parse_choice_answers(raw_question['answers'])
    elif (question_type is quizcomp.model.constants.QuestionType.NUMERICAL):
        return _parse_numerical_answers(raw_question['answers'])
    elif (question_type is quizcomp.model.constants.QuestionType.TEXT_ONLY):
        return quizcomp.model.answer.TextAnswers()
    elif (question_type is quizcomp.model.constants.QuestionType.TF):
        choices = _parse_choice_answers(raw_question['answers']).parts[DEFAULT_BLANK_ID]
        return quizcomp.model.answer.TFAnswers(choices.choices)
    else:
        raise ValueError(f"Unknown question type: '{question_type.value}'.")

def _parse_choice_answers(
        raw_choices: typing.List[typing.Dict[str, typing.Any]],
        ) -> quizcomp.model.answer.MultiplePartChoiceAnswers:
    """
    Parse choice answers.
    The choices will be keyed by the "blank id", which is used in multipart questions.
    If there is no blank id, then DEFAULT_BLANK_ID will be used.
    """

    all_choices: typing.Dict[str, typing.List[quizcomp.model.answer.Choice]] = {}

    for raw_choice in raw_choices:
        blank_id = raw_choice.get('blank_id', DEFAULT_BLANK_ID)
        if (blank_id not in all_choices):
            all_choices[blank_id] = []

        all_choices[blank_id].append(quizcomp.model.answer.Choice(
            text = _parse_text(raw_choice, 'text', 'html', ''),
            correct = math.isclose(raw_choice['weight'], 100.0),
            feedback = quizcomp.model.feedback.Feedback(general = _parse_text(raw_choice, 'comments', 'comments_html')),
        ))

    parts = {blank_id: quizcomp.model.answer.ChoiceAnswers(choices) for (blank_id, choices) in all_choices.items()}
    return quizcomp.model.answer.MultiplePartChoiceAnswers(parts)

def _parse_numerical_answers(
        raw_options: typing.List[typing.Dict[str, typing.Any]],
        ) -> quizcomp.model.answer.NumericAnswers:
    """
    Parse numerical answers.
    See: https://developerdocs.instructure.com/services/canvas/resources/quiz_questions#answer
    """

    options = []
    for raw_option in raw_options:
        raw_type = raw_option.get('numerical_answer_type', None)
        if (raw_type is None):
            raise ValueError("Numeric answer has no answer type.")

        feedback = quizcomp.model.feedback.Feedback(general = _parse_text(raw_option, 'comments', 'comments_html'))

        if (raw_type == 'exact_answer'):
            options.append(quizcomp.model.answer.NumericOptionExact(
                raw_option['exact'],
                raw_option.get('error_margin', 0.0),
                feedback = feedback,
            ))
        elif (raw_type == 'range_answer'):
            options.append(quizcomp.model.answer.NumericOptionRange(
                raw_option['range_start'],
                raw_option['range_end'],
                feedback = feedback,
            ))
        elif (raw_type == 'precision_answer'):
            options.append(quizcomp.model.answer.NumericOptionPrecision(
                raw_option['approximate'],
                raw_option['precision'],
                feedback = feedback,
            ))
        else:
            raise ValueError(f"Unknown numerical answer type: '{raw_type}'.")

    return quizcomp.model.answer.NumericAnswers(options)

def _parse_matching_answers(
        raw_question: typing.Dict[str, typing.Any],
        ) -> quizcomp.model.answer.NumericAnswers:
    """
    Parse matching answers.
    The Canvas API documentation is not accurate for this question type.
    """

    # {id: text document, ...}.
    rights = {}
    for raw_right in raw_question['matches']:
        rights[raw_right['match_id']] = quizcomp.parser.document.ParsedDocument.parse_text(raw_right['text'])

    # Match each left to a right, removing each matched right.
    pairs = []
    for raw_left in raw_question['answers']:
        feedback = quizcomp.model.feedback.Feedback(general = _parse_text(raw_left, 'comments', 'comments_html'))
        left_document = quizcomp.parser.document.ParsedDocument.parse_text(raw_left['text'])

        right_document = rights.get(raw_left['match_id'], None)
        if (right_document is None):
            raise ValueError("Unable to find matching right-hand component of a matching pair.")

        del rights[raw_left['match_id']]

        pairs.append((quizcomp.model.answer.TextOption(left_document, feedback), quizcomp.model.answer.TextOption(right_document)))

    # For the remaining rights into distractors.
    distractors = [quizcomp.model.answer.TextOption(document) for document in rights.values()]

    return quizcomp.model.answer.MatchingAnswers(pairs, distractors)
