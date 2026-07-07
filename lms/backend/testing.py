import glob
import os
import typing

import edq.core.log
import edq.net.exchangeserver
import edq.testing.cli
import edq.testing.unittest
import edq.testing.httpserver
import edq.util.pyimport
import edq.util.serial

import lms.model.backend
import lms.model.base
import lms.model.constants
import lms.backend.instance
import lms.testing.serverrunner

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

    backend_type: typing.Union[lms.model.constants.BackendType, None] = None
    """
    The backend type for this test.
    Must be set by the child class.
    """

    server_runner: typing.Union[lms.testing.serverrunner.LMSServerRunner, None] = None
    """ If a current server runner for this test (if there is one). """

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

    allowed_backend: typing.Union[lms.model.constants.BackendType, None] = None
    """ If set, skip any backend tests that do not match this filter. """

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(*args, **kwargs)

        self._user_email: typing.Union[str, None] = None
        """
        The email of the current user for this backend.
        Setting the user allows child classes to fetch specific information (like authentication information).
        """

        # Most backends have to modify exchanges in some way that makes these tests unreliable.
        # Instead, exchanges are tested enough through normal testing usage.
        self.skip_test_exchanges_base = True

    @classmethod
    def setup_server(cls, server: edq.net.exchangeserver.HTTPExchangeServer) -> None:
        if (cls.server_key == ''):
            raise ValueError("BackendTest subclass did not set server key properly.")

        edq.testing.httpserver.HTTPServerTest.setup_server(server)

    @classmethod
    def create_server(cls) -> edq.net.exchangeserver.HTTPExchangeServer:
        return LMSHTTPExchangeServer()

    @classmethod
    def post_start_server(cls, server: edq.net.exchangeserver.HTTPExchangeServer) -> None:
        if (cls.backend_type is None):
            raise ValueError("BackendTest subclass did not set backend type properly.")

        if (cls.exchanges_dir is None):
            raise ValueError("BackendTest subclass did not set exchanges dir properly.")

        context = edq.util.serial.SerializationContext(json_options = {
            'strict': True,
        })
        server.load_exchanges_dir(cls.exchanges_dir, context = context, finalize_func = cls._finalize_exchange)

        # Update match options.
        for (key, values) in [('params_to_skip', cls.params_to_skip), ('headers_to_skip', cls.headers_to_skip)]:
            if (key not in server.match_options):
                server.match_options[key] = []

            server.match_options[key] += values

        config_data: typing.Dict[str, typing.Any] = {
            'server': cls.get_server_url(),
            'backend_type': cls.backend_type,
        }
        config_data.update(cls.backend_args)

        config = lms.model.config.Config.from_dict(config_data)
        cls.backend = lms.backend.instance.get_backend(config, **cls.backend_args)

    @classmethod
    def get_base_args(cls) -> typing.Dict[str, typing.Any]:
        """ Get a copy of the base arguments for a request (function). """

        return {}

    def setUp(self) -> None:
        edq.core.log.init('ERROR')

        self.clear_user()

    def get_backend(self) -> lms.model.backend.APIBackend:
        """ Get the backend or fail if there is no backend. """

        if (self.backend is None):
            self.fail("No backend is set.")

        return self.backend

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
            disable_server_restart: bool = False,
            ) -> None:
        """
        A common test for the base request functionality.
        Test cases are passed in as: `[(kwargs (and overrides), expected, error substring), ...]`.
        """

        if ((self.backend_type is not None) and (self.allowed_backend is not None) and (self.allowed_backend != self.backend_type)):
            self.skipTest(f"Backend '{self.backend_type.value}' has been filtered, only allowing '{self.allowed_backend.value}'.")

        skip_reason = None

        for (i, test_case) in enumerate(test_cases):
            (extra_kwargs, expected, error_substring) = test_case

            with self.subTest(msg = f"Case {i}:"):
                kwargs = self.get_base_args()
                kwargs.update(extra_kwargs)

                if (disable_server_restart and (self.server_runner is not None)):
                    self.server_runner.skip_restart = True

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
                finally:
                    if (disable_server_restart and (self.server_runner is not None)):
                        self.server_runner.skip_restart = False
                        self.server_runner.restart()

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
                    elif (isinstance(expected_value, (dict, edq.util.serial.DictConverter))):
                        self.assertJSONDictEqual(expected_value, actual_value)
                    elif (isinstance(expected_value, list)):
                        self.assertJSONListEqual(expected_value, actual_value)
                    elif (isinstance(expected_value, edq.util.serial.PODConverter)):
                        self.assertJSONEqual(expected_value, actual_value)
                    else:
                        self.assertEqual(expected_value, actual_value)

        if (skip_reason is not None):
            self.skipTest(f"Backend component not implemented: {skip_reason}.")

    def modify_cli_test_info(self, test_info: edq.testing.cli.CLITestInfo) -> None:
        """ Adjust the CLI test info to include core info (like server information). """

        if ((self.backend_type is not None) and (self.backend_type.value in test_info.extra_options.get('skip_backends', []))):
            test_info.skip_reasons.append(f"CLI test backend '{self.backend_type.value}' has been skipped by test info.")
            return

        test_info.arguments += [
            '--config-global', CLI_GLOBAL_CONFG_PATH,
            '--server', self.get_server_url(),
            '--config', 'testing=true',
        ]

        if (self.backend_type is not None):
            test_info.arguments += ['--server-type', self.backend_type.value]

        # Mark this CLI test for skipping based on the backend filter.
        if ((self.backend_type is not None) and (self.allowed_backend is not None) and (self.allowed_backend != self.backend_type)):
            test_info.skip_reasons.append(
                    f"CLI test backend '{self.backend_type.value}' has been filtered, only allowing '{self.allowed_backend.value}'.")

    @classmethod
    def get_test_basename(cls, path: str) -> str:
        """ Get the test's name based off of its filename and location. """

        return edq.testing.cli.compute_ancestor_basename(path, CLI_TESTS_DIR)

    @classmethod
    def _finalize_exchange(cls, exchange: edq.net.exchange.HTTPExchange) -> edq.net.exchange.HTTPExchange:
        """
        Finalize an exchange before loading it into the test server.
        """

        # Check for redirect locations with a slug.
        if ('location' in exchange.response_headers):
            location = exchange.response_headers['location'].replace(lms.model.constants.SERVER_SLUG, cls.get_server_url())
            exchange.response_headers['location'] = location

        return exchange

class LMSHTTPExchangeServer(edq.net.exchangeserver.HTTPExchangeServer):
    """ A custom exchange server for our tests. """

    def missing_request(self, query: edq.net.exchange.HTTPExchange) -> typing.Union[edq.net.exchange.HTTPExchange, None]:
        # Specal Canvas patch to handle a multi-stage file upload (which uses redirects).
        if (query.url_path == 'files_api'):
            query.parameters = {'filename': query.parameters['filename']}
            query.files = []

            exchange, _ = self.lookup_exchange(query)
            return exchange

        return None

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
