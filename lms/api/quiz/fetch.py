import logging

import lms.api.common
import lms.api.quiz.resolve

def request(server = None, token = None, course = None,
        quizzes = [],
        **kwargs):
    server = lms.api.common.validate_param(server, 'server')
    token = lms.api.common.validate_param(token, 'token')
    course = lms.api.common.validate_param(course, 'course', param_type = int)

    logging.info("Fetching course ('%s') quizzes (%s) from '%s'." % (
            str(course), ", ".join(map(str, quizzes)), server))

    if (len(quizzes) == 0):
        return []

    return lms.api.quiz.resolve.fetch_and_resolve_quizzes(
            server, token, course, quizzes)
