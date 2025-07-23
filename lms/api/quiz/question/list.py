import logging

import lms.api.common
import lms.api.quiz.resolve

BASE_ENDPOINT = "/api/v1/courses/{course}/quizzes/{quiz}/questions?per_page={page_size}"

def request(server = None, token = None, course = None, quiz = None,
        keys = None, missing_value = None,
        **kwargs):
    server = lms.api.common.validate_param(server, 'server')
    token = lms.api.common.validate_param(token, 'token')
    course = lms.api.common.validate_param(course, 'course', param_type = int)

    quiz = lms.api.quiz.resolve.fetch_and_resolve_quiz(server, token, course, quiz)
    quiz_id = quiz['id']

    logging.info("Fetching course ('%s') quiz ('%s') questions from '%s'." % (
            str(course), str(quiz_id), server))

    url = server + BASE_ENDPOINT.format(course = course, quiz = quiz_id, page_size = lms.api.common.DEFAULT_PAGE_SIZE)
    headers = lms.api.common.standard_headers(token)

    output = []

    while (url is not None):
        _, url, new_questions = lms.api.common.make_get_request(url, headers)

        for new_question in new_questions:
            if (keys is not None):
                new_question = {key: new_question.get(key, missing_value) for key in keys}

            output.append(new_question)

    return output
