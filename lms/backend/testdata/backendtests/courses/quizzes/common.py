import typing

import quizcomp.model.constants
import quizcomp.model.quiz

def _sketch_quiz(raw_quiz: typing.Any) -> typing.Dict[str, typing.Any]:
    """
    Take a quiz and create a "sketch" from it, which vaguely captures its structure.

    Directly checking the contents of a downloaded quiz won't work well because of the internal conversions that LMS do.
    For example, a text in the Quiz Composer is Markdown, then uploaded to Canvas that becomes (deterministic) HTML,
    but then downloading that text again requires approximation to get that text back into Markdown.
    """

    quiz = typing.cast(quizcomp.model.quiz.Quiz, raw_quiz)

    quiz_data = {
        'name': quiz.name,
        'groups': [],
    }

    for group in quiz.get_groups():
        group_data = {
            'name': group.name,
            'pick_count': group.pick_count,
            'points': float(group.points),
            'questions': [],
        }

        for question in group.get_questions():
            # Normalize SA and ESSAY questions to the same type (some LMSs do not support both).
            question_type = question.question_type
            if (question_type in [quizcomp.model.constants.QuestionType.ESSAY, quizcomp.model.constants.QuestionType.SA]):
                question_type = quizcomp.model.constants.QuestionType.ESSAY

            question_data = {
                'question_type': question_type,
                'feedback': question.feedback,
            }

            group_data['questions'].append(question_data)

        quiz_data['groups'].append(group_data)

    return quiz_data
