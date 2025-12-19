import glob
import os
import typing

import edq.core.log
import edq.testing.cli
import edq.testing.unittest
import edq.testing.httpserver
import edq.util.pyimport

import lms.model.backend
import lms.model.base
import lms.backend.instance

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
TESTDATA_DIR: str = os.path.join(THIS_DIR, 'testdata')

BACKEND_TESTS_DIR: str = os.path.join(TESTDATA_DIR, 'backendtests')

CLI_TESTDATA_DIR: str = os.path.join(TESTDATA_DIR, 'cli')
CLI_TESTS_DIR: str = os.path.join(CLI_TESTDATA_DIR, 'tests')
CLI_DATA_DIR: str = os.path.join(CLI_TESTDATA_DIR, 'data')
CLI_GLOBAL_CONFG_PATH: str = os.path.join(CLI_DATA_DIR, 'testing-edq-lms.json')

TEST_FUNC_NAME_PREFIX: str = 'test_'
TEST_FILENAME_GLOB_PATTERN: str = '*_backendtest.py'

class BackendTest(edq.testing.httpserver.HTTPServerTest):
    """
    A special test suite that is common across all LMS backends.

    This is an HTTP test that will start a test server with exchanges specific to the target backend.

    A common directory (BACKEND_TESTS_DIR) will be searched for any file that starts with TEST_FILENAME_GLOB_PATTERN.
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

    backend_args: typing.Dict[str, typing.Any] = {
        'testing': True,
    }
    """ Any additional arguments to send to get_backend(). """

    skip_base_request_test: bool = False
    """ Skip any base request tests. """

    allowed_backend: typing.Union[str, None] = None
    """ If set, skip any backend tests that do not match this filter. """

    override_server_url: typing.Union[str, None] = None
    """ If set, return this URL from get_server_url(). """

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(*args, **kwargs)

        self._user_email: typing.Union[str, None] = None
        """
        The email of the current user for this backend.
        Setting the user allows child classes to fetch specific information (like authentication information).
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
        cls.backend = lms.backend.instance.get_backend(cls.get_server_url(), backend_type = cls.backend_type, **cls.backend_args)

    @classmethod
    def get_base_args(cls) -> typing.Dict[str, typing.Any]:
        """ Get a copy of the base arguments for a request (function). """

        return {}

    @classmethod
    def get_server_url(cls) -> str:
        if (cls.override_server_url is not None):
            return cls.override_server_url

        return str(super().get_server_url())

    def setUp(self) -> None:
        edq.core.log.init('ERROR')

        self.clear_user()

    def set_user(self, email: str) -> None:
        """
        Set the current user for this test.
        This can be especially useful for child classes that need to set information based on the user
        (like authentication headers).
        """

        self._user_email = email

    def clear_user(self) -> None:
        """
        Clear the current user for this test.
        This is automatically called before each test method.
        """

        self._user_email = None

    def base_request_test(self,
            request_function: typing.Callable,
            test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]],
            stop_on_notimplemented: bool = True,
            actual_clean_func: typing.Union[typing.Callable, None] = None,
            expected_clean_func: typing.Union[typing.Callable, None] = None,
            assertion_func: typing.Union[typing.Callable, None] = None,
            ) -> None:
        """
        A common test for the base request functionality.
        Test cases are passed in as: `[(kwargs (and overrides), expected, error substring), ...]`.
        """

        if ((self.allowed_backend is not None) and (self.allowed_backend != self.backend_type)):
            self.skipTest(f"Backend {self.backend_type} has been filtered.")

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

                if (actual_clean_func is not None):
                    actual = actual_clean_func(actual)

                if (expected_clean_func is not None):
                    expected = expected_clean_func(expected)

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

                    if (assertion_func is not None):
                        assertion_func(expected_value, actual_value)
                    elif (isinstance(expected_value, lms.model.base.BaseType)):
                        self.assertJSONEqual(expected_value, actual_value)
                    elif (isinstance(expected_value, dict)):
                        self.assertJSONDictEqual(expected_value, actual_value)
                    elif (isinstance(expected_value, list)):
                        self.assertJSONListEqual(expected_value, actual_value)
                    else:
                        self.assertEqual(expected_value, actual_value)

        if (skip_reason is not None):
            self.skipTest(f"Backend component not implemented: {skip_reason}.")

    def modify_cli_test_info(self, test_info: edq.testing.cli.CLITestInfo) -> None:
        """ Adjust the CLI test info to include core info (like server information). """

        test_info.arguments += [
            '--config-global', CLI_GLOBAL_CONFG_PATH,
            '--server', self.get_server_url(),
            '--server-type', str(self.backend_type),
            '--config', 'testing=true',
        ]

        # Mark this CLI test for skipping based on the backend filter.
        if ((self.allowed_backend is not None) and (self.allowed_backend != self.backend_type)):
            test_info.skip_reasons.append(f"Backend {self.backend_type} has been filtered.")

    @classmethod
    def get_test_basename(cls, path: str) -> str:
        """ Get the test's name based off of its filename and location. """

        path = os.path.abspath(path)

        name = os.path.splitext(os.path.basename(path))[0]

        ancestors = os.path.dirname(path).replace(CLI_TESTS_DIR, '')
        prefix = ancestors.replace(os.sep, '_')

        if (prefix.startswith('_')):
            prefix = prefix.replace('_', '', 1)

        if (len(prefix) > 0):
            name =  f"{prefix}_{name}"

        return name

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
            # Skip tests for backend component that do not have implementations.
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

    paths = list(sorted(glob.glob(os.path.join(BACKEND_TESTS_DIR, "**", TEST_FILENAME_GLOB_PATTERN), recursive = True)))
    for path in sorted(paths):
        add_test_path(target_class, path)

def attach_test_cases(target_class: type) -> None:
    """ Attach all the standard test cases to the given class. """

    # Attach backend tests.
    discover_test_cases(target_class)

    # Attach CLI tests.
    edq.testing.cli.discover_test_cases(target_class, CLI_TESTS_DIR, CLI_DATA_DIR, test_method_wrapper = _wrap_cli_test_method)

def _wrap_cli_test_method(test_method: typing.Callable, test_info_path: str) -> typing.Callable:
    """ Wrap the CLI tests to ignore NotImplemented errors. """

    def __method(self: edq.testing.unittest.BaseTest) -> None:
        try:
            test_method(self, reraise_exception_types = (NotImplementedError,))
        except NotImplementedError as ex:
            # Skip tests for backend component that do not have implementations.
            self.skipTest(f"Backend component not implemented: {str(ex)}.")

    return __method
