import lms.backend.testing
import lms.model.quizzes
import lms.model.testdata.quizzes

def test_courses_quizzes_questions_fetch_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of fetching course quiz questions. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000201',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['Ice Breaker'],
            None,
        ),

        # Miss
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '999',
            },
            None,
            None,
        ),

        # Tests for each other test question.
        # These are not necessary, but helpful in debugging.
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000202',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['Regular Expression in Programming Languages'],
            None,
        ),
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000203',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['Regular Expression Vocabulary'],
            None,
        ),
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000204',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['Basic Regular Expressions'],
            None,
        ),
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000205',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['Question'],
            None,
        ),
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000206',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['Passage Search'],
            None,
        ),
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000207',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['Quantifiers'],
            None,
        ),
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000208',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['General Quantification 1'],
            None,
        ),
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000209',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['General Quantification 2'],
            None,
        ),
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000210',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['Backreference Matching'],
            None,
        ),
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000211',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['Regex Golf'],
            None,
        ),
        (
            {
                'course_id': '110000000',
                'quiz_id': '110000200',
                'question_id': '110000212',
            },
            lms.model.testdata.quizzes.QUIZ_QUESTIONS['Regular Expressions']['Write a Function'],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_quizzes_questions_fetch, test_cases)
