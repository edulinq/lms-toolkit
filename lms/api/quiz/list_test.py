import lms.api.testing
import lms.api.quiz.list
import lms.api.quiz.testing

class QuizListTest(lms.api.testing.HTTPTest):
    """ Test listing course quizzes. """

    def test_quiz_list_base(self):
        """ Test the base functionality of listing quizzes. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Base

            (
                {},
                [
                    lms.api.quiz.testing.QUIZZES['10000001'],
                ],
                None,
            ),
        ]

        self.base_request_test(lms.api.quiz.list.request, test_cases)
