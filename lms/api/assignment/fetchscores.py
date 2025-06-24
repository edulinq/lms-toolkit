import logging
import requests

import lms.api.assignment.common
import lms.api.assignment.fetch
import lms.api.common
import lms.api.user.common
import lms.api.user.list

BASE_ENDPOINT = "/api/v1/courses/{course}/assignments/{assignment}/submissions?per_page={page_size}"

DEFAULT_KEYS = [
    'id',
    'grade',
    'score',
    'submitted_at',
    'graded_at',
]

def request(server = None, token = None, course = None, assignment = None,
        keys = DEFAULT_KEYS,
        assignment_keys = lms.api.assignment.common.DEFAULT_KEYS, user_keys = lms.api.user.common.DEFAULT_KEYS,
        **kwargs):
    server = lms.api.common.validate_param(server, 'server')
    token = lms.api.common.validate_param(token, 'token')
    course = lms.api.common.validate_param(course, 'course', param_type = int)
    assignment = lms.api.common.validate_param(assignment, 'assignment')

    logging.info("Fetching information for assignement ('%s' (course '%s')) from '%s'." % (assignment, str(course), server))

    resolved_assignments = lms.api.assignment.fetch.request(server = server, token = token, course = course,
            assignments = [assignment], keys = assignment_keys)

    if (len(resolved_assignments) == 0):
        raise ValueError("Unable to resolve assignment query '%s'." % (assignment))

    assignment_info = resolved_assignments[0]

    all_users = _fetch_users(server, token, course)

    url = server + BASE_ENDPOINT.format(course = course, assignment = assignment_info['id'],
            page_size = lms.api.common.DEFAULT_PAGE_SIZE)
    headers = lms.api.common.standard_headers(token)

    submissions = []

    while (url is not None):
        _, url, items = lms.api.common.make_get_request(url, headers)

        for item in items:
            user_id = item.get('user_id', None)
            if (user_id is None):
                continue

            if (user_id not in all_users):
                continue

            item = {key: item.get(key, None) for key in keys}
            user = {key: all_users[user_id].get(key, None) for key in user_keys}

            item['user'] = user
            item['assignment'] = assignment_info

            submissions.append(item)

    return submissions

def _fetch_users(server, token, course):
    users = lms.api.user.list.request(server = server, token = token, course = course)
    return {user['id']: user for user in users}
