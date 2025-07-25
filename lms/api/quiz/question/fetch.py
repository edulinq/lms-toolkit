import logging

import lms.api.common
import lms.api.quiz.question.resolve

def request(server = None, token = None, course = None, quiz = None,
        questions = [],
        **kwargs):
    server = lms.api.common.validate_param(server, 'server')
    token = lms.api.common.validate_param(token, 'token')
    course = lms.api.common.validate_param(course, 'course', param_type = int)
    quiz = lms.api.common.validate_param(quiz, 'quiz')

    logging.info("Fetching course ('%s') quiz ('%s') questions (%s) from '%s'." % (
            str(course), str(quiz), ", ".join(map(str, questions)), server))

    if (len(questions) == 0):
        return []

    return lms.api.quiz.question.resolve.fetch_and_resolve_questions(
            server, token, course, quiz, questions)
