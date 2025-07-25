import lms.api.quiz.question.list
import lms.api.resolve

def fetch_and_resolve_questions(server, token, course, quiz, question_queries):
    return lms.api.resolve.fetch_and_resolve(server, token, course, question_queries,
            list_function = lms.api.quiz.question.list.request,
            list_function_kwargs = {'quiz': quiz},
            resolve_kwargs = {'allow_multiple_matches': True})
