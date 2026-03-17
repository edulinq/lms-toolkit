import lms.backend.testing
import lms.model.courses
import lms.model.quizzes
import lms.model.testdata.quizzes

def test_courses_quizzes_questions_resolve_and_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and listing course quizzes. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_query': lms.model.quizzes.QuizQuery(id = '110000200'),
            },
            lms.model.testdata.quizzes.ORDERED_QUIZ_QUESTIONS['Regular Expressions'],
            None,
        ),

        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'quiz_query': lms.model.quizzes.QuizQuery(name = 'Regular Expressions'),
            },
            lms.model.testdata.quizzes.ORDERED_QUIZ_QUESTIONS['Regular Expressions'],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_quizzes_questions_resolve_and_list, test_cases)
