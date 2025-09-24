import lms.api.testing
import lms.api.quiz.question.fetch
import lms.api.quiz.question.testing

class QuestionFetchTest(lms.api.testing.HTTPTest):
    """ Test fetching course questions. """

    def test_question_fetch_base(self):
        """ Test the base functionality of fetching questions. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Empty

            (
                {
                    'quiz': '10000001',
                },
                [],
                None,
            ),

            (
                {
                    'quiz': 'Regular Expressions',
                    'questions': ['20000001'],
                },
                [
                    lms.api.quiz.question.testing.QUESTIONS[0],
                ],
                None,
            ),

            (
                {
                    'quiz': '10000001',
                    'questions': ['Ice Breaker'],
                },
                [
                    lms.api.quiz.question.testing.QUESTIONS[0],
                ],
                None,
            ),

            # Multiple

            (
                {
                    'quiz': '10000001',
                    'questions': ['20000001', '20000003'],
                },
                [
                    lms.api.quiz.question.testing.QUESTIONS[0],
                    lms.api.quiz.question.testing.QUESTIONS[2],
                ],
                None,
            ),

            # Missing

            (
                {
                    'quiz': 'ZZZ',
                },
                [],
                None,
            ),
        ]

        self.base_request_test(lms.api.quiz.question.fetch.request, test_cases)
