import lms.api.testing
import lms.api.quiz.fetch
import lms.api.quiz.testing

class QuizFetchTest(lms.api.testing.HTTPTest):
    """ Test fetching course quizzes. """

    def test_quiz_fetch_base(self):
        """ Test the base functionality of fetching quizzes. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Empty

            (
                {},
                [],
                None,
            ),

            # Base

            (
                {
                    'quizzes': ['10000001'],
                },
                [
                    lms.api.quiz.testing.QUIZZES['10000001'],
                ],
                None,
            ),

            (
                {
                    'quizzes': ['Regular Expressions'],
                },
                [
                    lms.api.quiz.testing.QUIZZES['10000001'],
                ],
                None,
            ),
        ]

        self.base_request_test(lms.api.quiz.fetch.request, test_cases)
