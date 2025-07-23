import lms.api.quiz.list
import lms.api.resolve

def fetch_and_resolve_quizzes(server, token, course, quiz_queries):
    return lms.api.resolve.fetch_and_resolve(server, token, course, quiz_queries,
            list_function = lms.api.quiz.list.request)

def fetch_and_resolve_quiz(server, token, course, quiz_query):
    results = fetch_and_resolve_quizzes(server, token, course, [quiz_query])

    if (len(results) == 0):
        raise ValueError(f"Unable to resolve quiz '{quiz_query}': no matching results.")

    if (len(results) > 1):
        raise ValueError(f"Unable to resolve quiz '{quiz_query}': too many matching results ({len(results)}).")

    return results[0]
