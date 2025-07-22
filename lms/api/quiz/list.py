import logging

import lms.api.common

BASE_ENDPOINT = "/api/v1/courses/{course}/quizzes?per_page={page_size}"

def request(server = None, token = None, course = None,
        **kwargs):
    server = lms.api.common.validate_param(server, 'server')
    token = lms.api.common.validate_param(token, 'token')
    course = lms.api.common.validate_param(course, 'course', param_type = int)

    logging.info("Fetching course ('%s') quizzes from '%s'." % (str(course), server))

    url = server + BASE_ENDPOINT.format(course = course, page_size = lms.api.common.DEFAULT_PAGE_SIZE)
    headers = lms.api.common.standard_headers(token)

    return list_quizzes(url, headers)

def list_quizzes(url, headers, keys = None, missing_value = None):
    output = []

    while (url is not None):
        _, url, new_quizzes = lms.api.common.make_get_request(url, headers)

        for new_quiz in new_quizzes:
            if (keys is not None):
                new_quiz = {key: new_quiz.get(key, missing_value) for key in keys}

            output.append(new_quiz)

    return output
