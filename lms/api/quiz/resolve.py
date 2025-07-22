import lms.api.quiz.list
import lms.api.resolve

def fetch_and_resolve_quizzes(server, token, course, quiz_queries, fill_missing = False):
    return lms.api.resolve.fetch_and_resolve(server, token, course, quiz_queries,
            list_function = lms.api.quiz.list.request,
            resolve_kwargs = {'fill_missing': fill_missing})

def requires_resolution(quizzes):
    return lms.api.resolve.requires_resolution(quizzes)
