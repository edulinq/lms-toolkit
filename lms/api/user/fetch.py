import logging

import lms.api.common
import lms.api.user.common
import lms.api.user.resolve

BASE_ENDPOINT = "/api/v1/courses/{course}/users?per_page={page_size}"

def request(server = None, token = None, course = None,
        users = [],
        include_role = False,
        keys = lms.api.user.common.DEFAULT_KEYS, **kwargs):
    server = lms.api.common.validate_param(server, 'server')
    token = lms.api.common.validate_param(token, 'token')
    course = lms.api.common.validate_param(course, 'course', param_type = int)

    logging.info("Fetching course ('%s') users (%s) from '%s'." % (
            str(course), ", ".join(map(str, users)), server))

    if (len(users) == 0):
        return []

    if (lms.api.user.resolve.requires_resolution(users)):
        return lms.api.user.resolve.fetch_and_resolve_users(
                server, token, course, users,
                keys = keys, include_role = include_role)

    url = server + BASE_ENDPOINT.format(course = course, page_size = lms.api.common.DEFAULT_PAGE_SIZE)
    headers = lms.api.common.standard_headers(token)

    if (include_role):
        url += '&include[]=enrollments'

    for user in users:
        url += "&user_ids[]=%s" % (str(user))

    return lms.api.user.common.list_users(url, headers, keys)
