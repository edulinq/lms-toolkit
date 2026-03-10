import logging
import re
import typing

import html2text
import quizcomp.question.base

import lms.backend.canvas.common
import lms.model.assignments
import lms.model.backend
import lms.model.courses
import lms.model.groups
import lms.model.groupsets
import lms.model.quizzes
import lms.model.scores
import lms.model.users
import lms.util.parse

_logger = logging.getLogger(__name__)

ENROLLMENT_TYPE_TO_ROLE: typing.Dict[str, lms.model.users.CourseRole] = {
    'ObserverEnrollment': lms.model.users.CourseRole.OTHER,
    'StudentEnrollment': lms.model.users.CourseRole.STUDENT,
    'TaEnrollment': lms.model.users.CourseRole.GRADER,
    'DesignerEnrollment': lms.model.users.CourseRole.ADMIN,
    'TeacherEnrollment': lms.model.users.CourseRole.OWNER,
}
"""
Canvas enrollment types mapped to roles.
This map is ordered by priority/power.
The later in the dict, the more power.
"""

QUESTION_TYPE_MAPPING: typing.Dict[typing.Union[str, None], quizcomp.question.base.QuestionType] = {
    'essay_question': quizcomp.question.base.QuestionType.ESSAY,
    'fill_in_multiple_blanks_question': quizcomp.question.base.QuestionType.FIMB,
    'matching_question': quizcomp.question.base.QuestionType.MATCHING,
    'multiple_answers_question': quizcomp.question.base.QuestionType.MA,
    'multiple_choice_question': quizcomp.question.base.QuestionType.MCQ,
    'multiple_dropdowns_question': quizcomp.question.base.QuestionType.MDD,
    'numerical_question': quizcomp.question.base.QuestionType.NUMERICAL,
    'short_answer_question': quizcomp.question.base.QuestionType.FITB,
    'text_only_question': quizcomp.question.base.QuestionType.TEXT_ONLY,
    'true_false_question': quizcomp.question.base.QuestionType.TF,
}

_testing_override: bool = False  # pylint: disable=invalid-name
""" A special override to signal testing. """

def assignment(data: typing.Dict[str, typing.Any]) -> lms.model.assignments.Assignment:
    """
    Create a Canvas assignment associated with a course.

    See: https://developerdocs.instructure.com/services/canvas/resources/assignments
    """

    _parse_assignment_data(data, 'assignment')
    return lms.model.assignments.Assignment(**data)

def assignment_score(data: typing.Dict[str, typing.Any]) -> lms.model.scores.AssignmentScore:
    """
    Create a Canvas assignment score.

    See: https://developerdocs.instructure.com/services/canvas/resources/scores
    """

    # Check for important fields.
    for field in ['id', 'assignment_id', 'user_id']:
        if (field not in data):
            raise ValueError(f"Canvas assignment score is missing '{field}' field.")

    # Modify specific arguments before creation.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')
    data['score'] = lms.util.parse.optional_float(data.get('score', None), 'score')
    data['points_possible'] = lms.util.parse.optional_float(data.get('points_possible', None), 'points_possible')
    data['submission_date'] = lms.backend.canvas.common.parse_timestamp(data.get('submitted_at', None))
    data['graded_date'] = lms.backend.canvas.common.parse_timestamp(data.get('graded_at', None))

    assignment_id = lms.util.parse.required_string(data.get('assignment_id', None), 'assignment_id')
    data['assignment'] = lms.model.assignments.AssignmentQuery(id = assignment_id)

    user_id = lms.util.parse.required_string(data.get('user_id', None), 'user_id')
    data['user'] = lms.model.users.UserQuery(id = user_id)

    return lms.model.scores.AssignmentScore(**data)

def course(data: typing.Dict[str, typing.Any]) -> lms.model.courses.Course:
    """
    Create a Canvas course.

    See: https://developerdocs.instructure.com/services/canvas/resources/courses
    """

    # Check for important fields.
    for field in ['id']:
        if (field not in data):
            raise ValueError(f"Canvas course is missing '{field}' field.")

    # Modify specific arguments before creation.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')

    return lms.model.courses.Course(**data)

def course_user(backend: lms.model.backend.APIBackend, data: typing.Dict[str, typing.Any]) -> lms.model.users.CourseUser:
    """
    Create a Canvas user associated with a course.

    See: https://developerdocs.instructure.com/services/canvas/resources/users
    """

    # Check for important fields.
    for field in ['id']:
        if (field not in data):
            raise ValueError(f"Canvas user is missing '{field}' field.")

    # Modify specific arguments before sending them to super.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')

    # Canvas sometimes has email under different fields.
    if ((data.get('email', None) is None) or (len(data.get('email', '')) == 0)):
        data['email'] = data.get('login_id', None)

    enrollments = data.get('enrollments', None)
    if (enrollments is not None):
        data['raw_role'] = _parse_role_from_enrollments(enrollments)
        data['role'] = ENROLLMENT_TYPE_TO_ROLE.get(data['raw_role'], None)

        # Canvas has a discontinuity with its default course roles.
        # We need to patch this during testing.
        if ((backend.is_testing() or _testing_override) and data['email'] == 'course-admin@test.edulinq.org'):
            data['role'] = lms.model.users.CourseRole.ADMIN

    return lms.model.users.CourseUser(**data)

def group(data: typing.Dict[str, typing.Any]) -> lms.model.groups.Group:
    """
    Create a Canvas group associated with a course.

    See: https://developerdocs.instructure.com/services/canvas/resources/groups
    """

    # Check for important fields.
    for field in ['id']:
        if (field not in data):
            raise ValueError(f"Canvas group is missing '{field}' field.")

    # Modify specific arguments before creation.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')

    return lms.model.groups.Group(**data)

def group_set(data: typing.Dict[str, typing.Any]) -> lms.model.groupsets.GroupSet:
    """
    Create a Canvas group set associated with a course.

    See: https://developerdocs.instructure.com/services/canvas/resources/group_categories
    """

    # Check for important fields.
    for field in ['id']:
        if (field not in data):
            raise ValueError(f"Canvas group set is missing '{field}' field.")

    # Modify specific arguments before creation.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')

    return lms.model.groupsets.GroupSet(**data)

def quiz(data: typing.Dict[str, typing.Any]) -> lms.model.quizzes.Quiz:
    """
    Create a Canvas quiz associated with a course.

    See: https://developerdocs.instructure.com/services/canvas/resources/quizzes
    """

    _parse_assignment_data(data, 'quiz')
    return lms.model.quizzes.Quiz(**data)

def quiz_question(data: typing.Dict[str, typing.Any]) -> lms.model.quizzes.Question:
    """
    Create a Canvas quiz question.

    See: https://developerdocs.instructure.com/services/canvas/resources/quiz_questions
    """

    # Check for important fields.
    for field in ['id']:
        if (field not in data):
            raise ValueError(f"Canvas quiz question is missing '{field}' field.")

    raw_question_type = data.get('question_type', None)
    if (raw_question_type is None):
        raise ValueError('No question type provided.')

    question_type = QUESTION_TYPE_MAPPING.get(raw_question_type, None)
    if (question_type is None):
        raise ValueError(f"Unknown Canvas question type: '{raw_question_type}'.")

    data['question_type'] = question_type
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')
    data['name'] = lms.util.parse.optional_string(data.get('question_name', None))
    data['prompt'] = _canvas_html_to_markdown(data.get('question_text', None))
    data['points'] = lms.util.parse.optional_float(data.get('points_possible', None), 'points')
    data['raw_answers'] = data.get('answers', None)
    data['answers'] = _parse_quiz_question_answers(data.get('answers', None), question_type)

    return lms.model.quizzes.Question(**data)

def _canvas_html_to_markdown(text: typing.Union[str, None]) -> str:
    """
    Parse the text from a Canvas quiz question into markdown.
    We intend for the resulting markdown to have a little HTML as possible.
    This is an impossible task, but we want to do our best.
    """

    if (text is None):
        return ''

    converter = html2text.HTML2Text()

    converter.body_width = 0
    converter.mark_code = True

    text = converter.handle(text)
    text = text.strip()

    # Replace code tags with fences.
    text = re.sub(r'\[/?code\]', '```', text)

    # Replace placeholders (e.g., for fill in the blank questions).
    text = re.sub(r'\[(\w+?)\]', r'<placeholder>\1</placeholder>', text)

    return text

def _parse_quiz_question_answers(
        raw_answers: typing.Union[typing.List[typing.Any], None],
        question_type: quizcomp.question.base.QuestionType,
        ) -> typing.Union[typing.List[typing.Any], typing.Dict[str, typing.Any]]:
    """ Parse question answers from Canvas responses. """

    if (raw_answers is None):
        return []

    answers: typing.Union[typing.List[typing.Any], typing.Dict[str, typing.Any]] = []

    # Parse answers based on question type.
    if (question_type in {quizcomp.question.base.QuestionType.ESSAY, quizcomp.question.base.QuestionType.TEXT_ONLY}):
        pass
    elif (question_type == quizcomp.question.base.QuestionType.TF):
        if (len(raw_answers) != 2):
            raise ValueError(f"Unexpected length for T/F answers. Expected 2, found {len(raw_answers)}.")

        answers = [
            {"correct": (raw_answers[0]['weight'] > 0), "text": "True"},
            {"correct": (raw_answers[1]['weight'] > 0), "text": "False"},
        ]
    elif (question_type in {quizcomp.question.base.QuestionType.MA, quizcomp.question.base.QuestionType.MCQ}):
        answers = _parse_quiz_question_choices(raw_answers)
    elif (question_type == quizcomp.question.base.QuestionType.MDD):
        # Divide up sections by blank ID (find all the possibilities for each blank).
        # {key: [raw_answer, ...]}
        raw_sections: typing.Dict[str, typing.List[typing.Dict[str, typing.Any]]] = {}
        for raw_answer in raw_answers:
            key = raw_answer.get('blank_id', '')
            if (key not in raw_sections):
                raw_sections[key] = []

            raw_sections[key].append(raw_answer)

        # Parse the choices for each section/blank.
        answers = {}
        for (section_key, section_raw_answers) in raw_sections.items():
            answers[section_key] = {
                'text': section_key,
                'values': _parse_quiz_question_choices(section_raw_answers)
            }
    elif (question_type == quizcomp.question.base.QuestionType.FITB):
        answers = []
        for raw_answer in raw_answers:
            answers.append(_parse_quiz_question_text(raw_answer))
    else:
        _logger.warning("Cannot form question answers, unknown question type: '%s'.", question_type)

    return answers

def _parse_quiz_question_choices(choices: list[typing.Dict[str, typing.Any]]) -> typing.List[typing.Dict[str, typing.Any]]:
    """
    Parse the quiz question choices.
    This works for multiple types, like MCQ and MA.
    """

    results = []
    for choice in choices:
        text = _parse_quiz_question_text(choice)
        results.append({"correct": (choice['weight'] > 0), "text": text})

    return results

def _parse_quiz_question_text(choice: typing.Dict[str, typing.Any]) -> str:
    """ Parse text out of a Canvas question choice field. """

    text = choice.get('text', '').strip()
    if (text is None):
        text = ''

    if (len(text) == 0):
        text = _canvas_html_to_markdown(choice.get('html', None))

    return text

def _parse_assignment_data(data: typing.Dict[str, typing.Any], label: str) -> None:
    """
    Parse core assignment data.
    """

    for field in ['id']:
        if (field not in data):
            raise ValueError(f"Canvas {label} is missing '{field}' field.")

    # Modify specific arguments before creation.
    data['id'] = lms.util.parse.required_string(data.get('id', None), 'id')
    data['due_date'] = lms.backend.canvas.common.parse_timestamp(data.get('due_at', None))
    data['open_date'] = lms.backend.canvas.common.parse_timestamp(data.get('unlock_at', None))
    data['close_date'] = lms.backend.canvas.common.parse_timestamp(data.get('lock_at', None))

    # If there is no name, look for a title.
    if (data.get('name', None) is None):
        data['name'] = lms.util.parse.optional_string(data.get('title', None))

def _parse_role_from_enrollments(enrollments: typing.Any) -> typing.Union[str, None]:
    """
    Try to parse the user's role from their enrollments.
    If multiple roles are discovered, take the "highest" one.

    See: https://developerdocs.instructure.com/services/canvas/resources/enrollments
    """

    if (not isinstance(enrollments, list)):
        return None

    best_role = None
    best_index = -1

    enrollment_types = list(ENROLLMENT_TYPE_TO_ROLE.keys())

    for enrollment in enrollments:
        if (not isinstance(enrollment, dict)):
            continue

        if (enrollment.get('enrollment_state', None) != 'active'):
            continue

        role = enrollment.get('role', None)

        role_index = -1
        if (role in enrollment_types):
            role_index = enrollment_types.index(role)

        if ((best_role is None) or (role_index > best_index)):
            best_role = role
            best_index = role_index

    return best_role
