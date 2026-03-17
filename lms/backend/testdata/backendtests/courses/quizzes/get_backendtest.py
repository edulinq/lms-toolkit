import lms.backend.testing
import lms.model.quizzes
import lms.model.testdata.quizzes

def test_courses_quizzes_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting course quizzes. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Empty
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_queries': [],
            },
            [
            ],
            None,
        ),

        # Base
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_queries': [
                    lms.model.quizzes.QuizQuery(id = '110000200'),
                ],
            },
            [
                lms.model.testdata.quizzes.COURSE_QUIZZES['Course 101']['Regular Expressions'],
            ],
            None,
        ),


        # Query - Name
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_queries': [
                    lms.model.quizzes.QuizQuery(name = 'Regular Expressions'),
                ],
            },
            [
                lms.model.testdata.quizzes.COURSE_QUIZZES['Course 101']['Regular Expressions'],
            ],
            None,
        ),

        # Query - Label Name
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_queries': [
                    lms.model.quizzes.QuizQuery(name = 'Regular Expressions', id = '110000200'),
                ],
            },
            [
                lms.model.testdata.quizzes.COURSE_QUIZZES['Course 101']['Regular Expressions'],
            ],
            None,
        ),

        # Miss - Course
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '999'),
                'quiz_queries': [
                    lms.model.quizzes.QuizQuery(id = '110000200'),
                ],
            },
            None,
            'Could not resolve course query',
        ),

        # Miss - ID
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_queries': [
                    lms.model.quizzes.QuizQuery(id = '999'),
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
                'quiz_queries': [
                    lms.model.quizzes.QuizQuery(name = 'ZZZ'),
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
                'quiz_queries': [
                    lms.model.quizzes.QuizQuery(id = '110000200', name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_quizzes_get, test_cases)
