import logging
import requests

import lms.api.assignment.resolve
import lms.api.common
import lms.api.user.resolve

BASE_ENDPOINT = "/api/v1/courses/{course}/assignments/{assignment}/submissions/update_grades"

def request(server = None, token = None, course = None, assignment = None,
        users = [], scores = [], comments = [],
        **kwargs):
    server = lms.api.common.validate_param(server, 'server')
    token = lms.api.common.validate_param(token, 'token')
    course = lms.api.common.validate_param(course, 'course', param_type = int)
    assignment = lms.api.common.validate_param(assignment, 'assignment')

    logging.info("Uploading %d scores for assignment ('%s' (course '%s')) from '%s'." % (len(users), assignment, str(course), server))

    if (lms.api.assignment.resolve.requires_resolution([assignment])):
        resolved_assignments = lms.api.assignment.resolve.fetch_and_resolve_assignments(server, token, course, [assignment])
        if (len(resolved_assignments) == 0):
            raise ValueError("Unable to resolve assignment query '%s'." % (assignment))

        assignment = resolved_assignments[0]['id']

    if (lms.api.user.resolve.requires_resolution(users)):
        resolved_users = lms.api.user.resolve.fetch_and_resolve_users(server, token, course, users, fill_missing = True)

        new_users = []
        for i in range(len(resolved_users)):
            if (resolved_users[i] is None):
                new_users.append(None)
                logging.warning("User '%s' was not resolved to a LMS user, their grade will not be uploaded." % (users[i]))
            else:
                new_users.append(resolved_users[i]['id'])

        users = new_users

    return direct_request(server, token, course, assignment, users, scores, comments = comments)

# Perform the request with no resolution and minimal validation.
def direct_request(server, token, course, assignment, users, scores, comments = None):
    if ((len(users) != len(scores)) or ((comments is not None) and (len(users) != len(comments)))):
        raise ValueError("Mismatched count of users (%d), scores (%d), and comments (%d)." % (len(users), len(scores), len(comments)))

    score_count = 0
    data = {}
    for i in range(len(users)):
        if ((users[i] is None) or (scores[i] is None)):
            continue

        data["grade_data[%s][posted_grade]" % (users[i])] = scores[i]
        score_count += 1

        if ((comments is None) or (comments[i] is None)):
            continue

        comment = comments[i].strip()
        if (comment == ''):
            continue

        data["grade_data[%s][text_comment]" % (users[i])] = comment

    if (score_count == 0):
        return 0

    url = server + BASE_ENDPOINT.format(course = course, assignment = assignment)
    headers = lms.api.common.standard_headers(token)

    lms.api.common.make_post(url, headers, data)

    return score_count
