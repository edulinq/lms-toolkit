import lms.api.assignment.common
import lms.api.assignment.list
import lms.api.resolve

def fetch_and_resolve_assignments(server, token, course, assignment_queries,
        keys = lms.api.assignment.common.DEFAULT_KEYS):
    return lms.api.resolve.fetch_and_resolve(server, token, course, assignment_queries,
            lms.api.assignment.list.request,
            keys = keys, resolve_kwargs = {'match_email': False, 'label_uses_email': False})

def requires_resolution(assignments):
    return lms.api.resolve.requires_resolution(assignments)
