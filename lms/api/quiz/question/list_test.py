import lms.api.testing
import lms.api.quiz.question.list
import lms.api.quiz.question.testing

class QuestionListTest(lms.api.testing.HTTPTest):
    """ Test listing course questions. """

    def test_question_list_base(self):
        """ Test the base functionality of listing questions. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Base

            (
                {
                    'quiz': '10000001',
                },
                lms.api.quiz.question.testing.QUESTIONS,
                None,
            ),

            (
                {
                    'quiz': 'Regular Expressions',
                },
                lms.api.quiz.question.testing.QUESTIONS,
                None,
            ),

            # Missing

            (
                {
                    'quiz': 'ZZZ',
                },
                None,
                'Unable to resolve quiz',
            ),
        ]

        self.base_request_test(lms.api.quiz.question.list.request, test_cases)
