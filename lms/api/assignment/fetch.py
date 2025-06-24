import logging

import lms.api.assignment.common
import lms.api.assignment.resolve
import lms.api.common

BASE_ENDPOINT = "/api/v1/courses/{course}/assignments?per_page={page_size}"

def request(server = None, token = None, course = None,
        assignments = [],
        keys = lms.api.assignment.common.DEFAULT_KEYS, **kwargs):
    server = lms.api.common.validate_param(server, 'server')
    token = lms.api.common.validate_param(token, 'token')
    course = lms.api.common.validate_param(course, 'course', param_type = int)

    logging.info("Fetching course ('%s') assignments ('%s') from '%s'." % (
            str(course), ', '.join(map(str, assignments)), server))

    if (len(assignments) == 0):
        return []

    if (lms.api.assignment.resolve.requires_resolution(assignments)):
        return lms.api.assignment.resolve.fetch_and_resolve_assignments(
                server, token, course, assignments,
                keys = keys)

    url = server + BASE_ENDPOINT.format(course = course, page_size = lms.api.common.DEFAULT_PAGE_SIZE)
    headers = lms.api.common.standard_headers(token)

    for assignment in assignments:
        url += "&assignment_ids[]=%s" % (str(assignment))

    return lms.api.assignment.common.list_assignments(url, headers, keys)
