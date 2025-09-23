import os
import typing

import edq.testing.httpserver

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
TEST_EXCHANGES_DIR: str = os.path.join(THIS_DIR, "testdata", "http", 'exchanges')

TEST_CANVAS_TOKEN: str = 'TESTING_TOKEN'
""" The standard Canvas API token requests can use. """

TEST_CANVAS_COURSE: int = 12345
""" The standard Canvas course ID. """

PARAMS_TO_SKIP: typing.List[str] = [
    'per_page',
]
""" Parameters to skip while looking up exchanges. """

HEADERS_TO_SKIP: typing.List[str] = [
    'Authorization',
]
""" Headers to skip while looking up exchanges. """

class HTTPTest(edq.testing.httpserver.HTTPServerTest):
    """
    A unit test that requires the testing HTTP server to be running.
    """

    # Share a test server for all Canvas tests.
    server_key: str = 'canvas'
    tear_down_server: bool = False

    token: str = TEST_CANVAS_TOKEN
    """ The API token for these test to use. """

    course: str = str(TEST_CANVAS_COURSE)
    """ The course ID to use. """

    @classmethod
    def get_base_args(cls) -> typing.Dict[str, typing.Any]:
        """ Get a copy of the base arguments for a request (function). """

        return {
            'token': cls.token,
            'server': cls.get_server_url(),
            'course': cls.course,
        }

    @classmethod
    def setup_server(cls, server: edq.testing.httpserver.HTTPTestServer) -> None:
        edq.testing.httpserver.HTTPServerTest.setup_server(server)
        server.load_exchanges_dir(TEST_EXCHANGES_DIR)

        # Update match options.
        for (key, values) in [('params_to_skip', PARAMS_TO_SKIP), ('headers_to_skip', HEADERS_TO_SKIP)]:
            if (key not in server.match_options):
                server.match_options[key] = []

            server.match_options[key] += values

    def base_request_test(self,
            request_function: typing.Callable,
            test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]],
            ) -> None:
        """
        A common test for the base request functionality.
        Test cases are passed in as: `[(kwargs (and overrides), expected, error substring), ...]`.
        """

        for (i, test_case) in enumerate(test_cases):
            (extra_kwargs, expected, error_substring) = test_case

            with self.subTest(msg = f"Case {i}:"):
                kwargs = self.get_base_args()
                kwargs.update(extra_kwargs)

                try:
                    actual = request_function(**kwargs)
                except Exception as ex:
                    error_string = self.format_error_string(ex)
                    if (error_substring is None):
                        self.fail(f"Unexpected error: '{error_string}'.")

                    self.assertIn(error_substring, error_string, 'Error is not as expected.')

                    continue

                if (error_substring is not None):
                    self.fail(f"Did not get expected error: '{error_substring}'.")

                if (isinstance(expected, dict)):
                    self.assertJSONDictEqual(expected, actual)
                elif (isinstance(expected, list)):
                    self.assertJSONListEqual(expected, actual)
                else:
                    self.assertEqual(expected, actual)
