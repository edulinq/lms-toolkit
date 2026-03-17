import lms.backend.testing
import lms.model.quizzes
import lms.model.testdata.quizzes

def test_courses_quizzes_groups_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting course quizzes. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Empty
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_query': lms.model.quizzes.QuizQuery(id = '110000200'),
                'group_queries': [],
            },
            [
            ],
            None,
        ),

        # Base
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_query': lms.model.quizzes.QuizQuery(id = '110000200'),
                'group_queries': [
                    lms.model.quizzes.QuestionQuery(id = '110000201'),
                ],
            },
            [
                lms.model.testdata.quizzes.QUIZ_GROUPS['Regular Expressions']['Ice Breaker'],
            ],
            None,
        ),

        # Multiple
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_query': lms.model.quizzes.QuizQuery(id = '110000200'),
                'group_queries': [
                    lms.model.quizzes.QuestionQuery(id = '110000201'),
                    lms.model.quizzes.QuestionQuery(id = '110000202'),
                ],
            },
            [
                lms.model.testdata.quizzes.QUIZ_GROUPS['Regular Expressions']['Ice Breaker'],
                lms.model.testdata.quizzes.QUIZ_GROUPS['Regular Expressions']['Regular Expression in Programming Languages'],
            ],
            None,
        ),


        # Query - Name
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_query': lms.model.quizzes.QuizQuery(id = '110000200'),
                'group_queries': [
                    lms.model.quizzes.QuestionQuery(name = 'Ice Breaker'),
                ],
            },
            [
                lms.model.testdata.quizzes.QUIZ_GROUPS['Regular Expressions']['Ice Breaker'],
            ],
            None,
        ),

        # Query - Label Name
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_query': lms.model.quizzes.QuizQuery(id = '110000200'),
                'group_queries': [
                    lms.model.quizzes.QuestionQuery(name = 'Ice Breaker', id = '110000201'),
                ],
            },
            [
                lms.model.testdata.quizzes.QUIZ_GROUPS['Regular Expressions']['Ice Breaker'],
            ],
            None,
        ),

        # Miss - Course
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '999'),
                'quiz_query': lms.model.quizzes.QuizQuery(id = '110000200'),
                'group_queries': [
                    lms.model.quizzes.QuestionQuery(id = '110000201'),
                ],
            },
            None,
            'Could not resolve course query',
        ),

        # Miss - Quiz
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_query': lms.model.quizzes.QuizQuery(id = '999'),
                'group_queries': [
                    lms.model.quizzes.QuestionQuery(id = '110000201'),
                ],
            },
            None,
            'Could not resolve quiz query',
        ),

        # Miss - ID
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_query': lms.model.quizzes.QuizQuery(id = '110000200'),
                'group_queries': [
                    lms.model.quizzes.QuestionQuery(id = '999'),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Name
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_query': lms.model.quizzes.QuizQuery(id = '110000200'),
                'group_queries': [
                    lms.model.quizzes.QuestionQuery(name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Partial Match
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_query': lms.model.quizzes.QuizQuery(id = '110000200'),
                'group_queries': [
                    lms.model.quizzes.QuestionQuery(id = '110000201', name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_quizzes_groups_get, test_cases)
