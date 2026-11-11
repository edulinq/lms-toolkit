import types
import unittest.mock

import edq.testing.unittest

import lms.backend.canvas.courses.assignments.scores.comments.add

class AddCommentTest(edq.testing.unittest.BaseTest):
    """ Protect the distinction between comment-only and grade-changing requests. """

    def test_comment_only_request(self) -> None:
        """ Send the exact comment and no score, submission, or bulk grade fields. """

        backend = types.SimpleNamespace(server = 'http://localhost:3000', get_standard_headers = unittest.mock.Mock(return_value = {}))
        comment = '  Feedback & questions: why?\nSecond line.  '
        with unittest.mock.patch('lms.backend.canvas.common.make_put_request', return_value = {'score': 7}) as request:
            self.assertTrue(lms.backend.canvas.courses.assignments.scores.comments.add.request(backend, 1, 2, 3, comment))
        request.assert_called_once_with('http://localhost:3000/api/v1/courses/1/assignments/2/submissions/3',
                headers = {}, data = {'comment[text_comment]': comment})
        backend.get_standard_headers.assert_called_once_with(write = True)

    def test_empty_comment_no_request(self) -> None:
        """ Reject empty comments before making any HTTP request. """

        with unittest.mock.patch('lms.backend.canvas.common.make_put_request') as request:
            for comment in ['', ' \n\t']:
                with self.subTest(comment = comment):
                    with self.assertRaisesRegex(ValueError, 'Comment must not be empty.'):
                        lms.backend.canvas.courses.assignments.scores.comments.add.request(None, 1, 2, 3, comment)
        request.assert_not_called()
