import glob
import os
import typing

import edq.testing.httpserver
import edq.util.pyimport

import lms.model.backend
import lms.backend.backend

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
TESTS_DIR: str = os.path.join(THIS_DIR, "tests")

TEST_FUNC_NAME_PREFIX: str = 'test_'
TEST_FILENAME_GLOB_PATTERN: str = '*_backendtest.py'

TEST_COURSE_ID: str = '12345'
""" The standard test course ID. """

class BackendTest(edq.testing.httpserver.HTTPServerTest):  # type: ignore[misc]
    """
    A special test suite that is common across all LMS backends.

    This is an HTTP test that will start a test server with exchanges specific to the target backend.

    A common directory (TESTS_DIR) will be searched for any file that starts with TEST_FILENAME_GLOB_PATTERN.
    Then, that file will be checked for any function that starts with TEST_FUNC_NAME_PREFIX and matches BackendTestFunction.
    """

    backend_type: typing.Union[str, None] = None
    """
    The backend type for this test.
    Must be set by the child class.
    """

    exchanges_dir: typing.Union[str, None] = None
    """
    The directory to load HTTP exchanges from.
    Must be set by the child class.
    """

    params_to_skip: typing.List[str] = []
    """ Parameters to skip while looking up exchanges. """

    headers_to_skip: typing.List[str] = []
    """ Headers to skip while looking up exchanges. """

    backend: typing.Union[lms.model.backend.APIBackend, None] = None
    """
    The backend for this test.
    Will be created during setup_server().
    """

    backend_args: typing.Dict[str, typing.Any] = {}
    """
    Any additional arguments to send to get_backend().
    """

    @classmethod
    def setup_server(cls, server: edq.testing.httpserver.HTTPTestServer) -> None:
        if (cls.server_key == ''):
            raise ValueError("BackendTest subclass did not set server key properly.")

        if (cls.backend_type is None):
            raise ValueError("BackendTest subclass did not set backend type properly.")

        if (cls.exchanges_dir is None):
            raise ValueError("BackendTest subclass did not set exchanges dir properly.")

        edq.testing.httpserver.HTTPServerTest.setup_server(server)
        server.load_exchanges_dir(cls.exchanges_dir)

        # Update match options.
        for (key, values) in [('params_to_skip', cls.params_to_skip), ('headers_to_skip', cls.headers_to_skip)]:
            if (key not in server.match_options):
                server.match_options[key] = []

            server.match_options[key] += values

    @classmethod
    def post_start_server(cls, server: edq.testing.httpserver.HTTPTestServer) -> None:
        cls.backend = lms.backend.backend.get_backend(cls.get_server_url(), backend_type = cls.backend_type, **cls.backend_args)

    @classmethod
    def get_base_args(cls) -> typing.Dict[str, typing.Any]:
        """ Get a copy of the base arguments for a request (function). """

        return {
            'course_id': TEST_COURSE_ID,
        }

    def base_request_test(self,
            request_function: typing.Callable,
            test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]],
            stop_on_notimplemented: bool = True,
            ) -> None:
        """
        A common test for the base request functionality.
        Test cases are passed in as: `[(kwargs (and overrides), expected, error substring), ...]`.
        """

        skip_reason = None

        for (i, test_case) in enumerate(test_cases):
            (extra_kwargs, expected, error_substring) = test_case

            with self.subTest(msg = f"Case {i}:"):
                kwargs = self.get_base_args()
                kwargs.update(extra_kwargs)

                try:
                    actual = request_function(**kwargs)
                except NotImplementedError as ex:
                    # We must handle this directly since we are in a subtest.
                    if (stop_on_notimplemented):
                        skip_reason = str(ex)
                        break

                    self.skipTest(f"Backend component not implemented: {str(ex)}.")
                except Exception as ex:
                    error_string = self.format_error_string(ex)
                    if (error_substring is None):
                        self.fail(f"Unexpected error: '{error_string}'.")

                    self.assertIn(error_substring, error_string, 'Error is not as expected.')

                    continue

                if (error_substring is not None):
                    self.fail(f"Did not get expected error: '{error_substring}'.")

                # If we expect a tuple, compare the tuple contents instead of the tuple itself.
                if (isinstance(expected, tuple)):
                    if (not isinstance(actual, tuple)):
                        raise ValueError(f"Expected results to be a tuple, found '{type(actual)}'.")

                    if (len(expected) != len(actual)):
                        raise ValueError(f"Result size mismatch. Expected: {len(expected)}, Actual: {len(actual)}.")
                else:
                    # Wrap the results in a tuple.
                    expected = (expected, )
                    actual = (actual, )

                for i in range(len(expected)):  # pylint: disable=consider-using-enumerate
                    expected_value = expected[i]
                    actual_value = actual[i]

                    if (isinstance(expected_value, dict)):
                        self.assertJSONDictEqual(expected_value, actual_value)
                    elif (isinstance(expected_value, list)):
                        self.assertJSONListEqual(expected_value, actual_value)
                    else:
                        self.assertEqual(expected_value, actual_value)

        if (skip_reason is not None):
            self.skipTest(f"Backend component not implemented: {skip_reason}.")

@typing.runtime_checkable
class BackendTestFunction(typing.Protocol):
    """
    A test function for backend tests.
    A copy of this function will be attached to a test class created for each backend.
    Therefore, `self` will be an instance of BackendTest.
    """

    def __call__(self, test: BackendTest) -> None:
        """
        A unit test for a BackendTest.
        """

def _wrap_test_function(test_function: BackendTestFunction) -> typing.Callable:
    """ Wrap the backend test function in some common code for backend tests. """

    def __method(self: BackendTest) -> None:
        try:
            test_function(self)
        except NotImplementedError as ex:
            # Skip tests for backend component that do not implementations.
            self.skipTest(f"Backend component not implemented: {str(ex)}.")

    return __method

def add_test_path(target_class: type, path: str) -> None:
    """ Add tests from the given test files. """

    test_module = edq.util.pyimport.import_path(path)

    for attr_name in sorted(dir(test_module)):
        if (not attr_name.startswith(TEST_FUNC_NAME_PREFIX)):
            continue

        test_function = getattr(test_module, attr_name)
        setattr(target_class, attr_name, _wrap_test_function(test_function))

def discover_test_cases(target_class: type) -> None:
    """ Look in the text cases directory for any test cases and add them as test methods to the test class. """

    paths = list(sorted(glob.glob(os.path.join(TESTS_DIR, "**", TEST_FILENAME_GLOB_PATTERN), recursive = True)))
    for path in sorted(paths):
        add_test_path(target_class, path)
