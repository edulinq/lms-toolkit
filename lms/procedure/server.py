"""
Supporting code for running an LMS server for some larger process
(like generating or verifying test data).
"""

import argparse
import atexit
import logging
import signal
import subprocess
import time
import typing

import edq.util.dirent
import edq.util.net
import edq.util.parse
import edq.util.reflection

import lms.backend.instance
import lms.cli.parser
import lms.model.constants
import lms.util.net

SERVER_STARTUP_INITIAL_WAIT_SECS: float = 0.2
DEFAULT_STARTUP_WAIT_SECS: float = 10.0
SERVER_STOP_WAIT_SECS: float = 5.00

IDENTIFY_MAX_ATTEMPTS: int = 100
IDENTIFY_WAIT_SECS: float = 0.25

BACKEND_REQUEST_CLEANING_FUNCS: typing.Dict[str, typing.Callable] = {
    lms.model.constants.BACKEND_TYPE_CANVAS: lms.util.net.clean_canvas_response,
    lms.model.constants.BACKEND_TYPE_MOODLE: lms.util.net.clean_moodle_response,
}

class ServerRunner():
    """
    A class for running an LMS server for some sort of larger process.
    """

    def __init__(self,
            server: typing.Union[str, None] = None,
            backend_type: typing.Union[str, None] = None,
            server_start_command: typing.Union[str, None] = None,
            server_stop_command: typing.Union[str, None] = None,
            http_exchanges_out_dir: typing.Union[str, None] = None,
            server_output_path: typing.Union[str, None] = None,
            startup_wait_secs: typing.Union[float, None] = None,
            startup_skip_identify: typing.Union[bool, None] = False,
            **kwargs: typing.Any) -> None:
        if (server is None):
            raise ValueError('No server specified.')

        self.server: str = server
        """ The server address to point requests to. """

        if (server_start_command is None):
            raise ValueError('No command to start the server was specified.')

        self.backend_type: typing.Union[str, None] = backend_type
        """
        The type of server being run.
        This value will be resolved after the server is started
        (since part of resolution may involve pinging the server.
        """

        self.server_start_command: str = server_start_command
        """ The server_start_command to run the LMS server. """

        self.server_stop_command: typing.Union[str, None] = server_stop_command
        """ An optional command to stop the server. """

        if (http_exchanges_out_dir is None):
            http_exchanges_out_dir = edq.util.dirent.get_temp_dir(prefix = 'edq-lms-http-exchanges-', rm = False)

        self.http_exchanges_out_dir: str = http_exchanges_out_dir
        """ Where to output the HTTP exchanges. """

        if (server_output_path is None):
            server_output_path = edq.util.dirent.get_temp_path(prefix = 'edq-lms-server-output-', rm = False) + '.txt'

        self.server_output_path: str = server_output_path
        """ Where to write server output (stdout and stderr). """

        if (startup_wait_secs is None):
            startup_wait_secs = DEFAULT_STARTUP_WAIT_SECS

        self.startup_wait_secs = startup_wait_secs
        """ How long to wait after the server start command is run before making requests to the server. """

        if (startup_skip_identify is None):
            startup_skip_identify = False

        self.startup_skip_identify: bool = startup_skip_identify
        """
        Whether to skip trying to identify the server after it has been started.
        This acts as a way to have a variable wait for the server to start.
        When not used, self.startup_wait_secs is the only way to wait for the server to start.
        """

        self._old_exchanges_out_dir: typing.Union[str, None] = None
        """
        The value of edq.util.net._exchanges_out_dir when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_exchanges_clean_func: typing.Union[str, None] = None
        """
        The value of edq.util.net._exchanges_clean_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_set_exchanges_clean_func: bool = False
        """
        The value of lms.util.net._set_exchanges_clean_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_make_request_exchange_complete_func: typing.Union[edq.util.net.HTTPExchangeComplete, None] = None
        """
        The value of lms.util.net._make_request_exchange_complete_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._process: typing.Union[subprocess.Popen, None] = None
        """ The server process. """

        self._server_output_file: typing.Union[typing.IO, None] = None
        """ The file that server output is written to. """

    def start(self) -> None:
        """ Start the server. """

        if (self._process is not None):
            return

        # Ensure stop() is called.
        atexit.register(self.stop)

        def _make_request_callback(exchange: edq.util.net.HTTPExchange) -> None:
            # Restart if the request is a write.
            if (edq.util.parse.boolean(exchange.headers.get(lms.model.constants.HEADER_KEY_WRITE, False))):
                self.restart()

        self._old_make_request_exchange_complete_func = edq.util.net._make_request_exchange_complete_func
        edq.util.net._make_request_exchange_complete_func = typing.cast(edq.util.net.HTTPExchangeComplete, _make_request_callback)

        # Start the server.

        logging.info("Writing HTTP exchanges to '%s'.", self.http_exchanges_out_dir)
        logging.info("Writing server output to '%s'.", self.server_output_path)
        logging.info("Starting the server ('%s') and waiting for it.", self.server)

        self._server_output_file = open(self.server_output_path, 'a', encoding = edq.util.dirent.DEFAULT_ENCODING)  # pylint: disable=consider-using-with

        self._start_server()

        # Resolve the backend type.
        self.backend_type = lms.backend.instance.guess_backend_type(self.server, backend_type = self.backend_type)
        if (self.backend_type is None):
            raise ValueError(f"Unable to determine backend type for server '{self.server}'.")

        # Store and set networking config.

        self._old_set_exchanges_clean_func = lms.cli.parser._set_exchanges_clean_func
        lms.cli.parser._set_exchanges_clean_func = False

        exchange_clean_func = BACKEND_REQUEST_CLEANING_FUNCS.get(self.backend_type, lms.util.net.clean_lms_response)
        exchange_clean_func_name = edq.util.reflection.get_qualified_name(exchange_clean_func)

        self._old_exchanges_out_dir = edq.util.net._exchanges_out_dir
        edq.util.net._exchanges_out_dir = self.http_exchanges_out_dir

        self._old_exchanges_clean_func = edq.util.net._exchanges_clean_func
        edq.util.net._exchanges_clean_func = exchange_clean_func_name

    def _start_server(self) -> None:
        """ Start the server. """

        if (self._process is not None):
            return

        self._process = subprocess.Popen(self.server_start_command,  # pylint: disable=consider-using-with
                shell = True, stdout = self._server_output_file, stderr = subprocess.STDOUT)

        status = None
        try:
            # Wait for a short period for the process to start.
            status = self._process.wait(SERVER_STARTUP_INITIAL_WAIT_SECS)
        except subprocess.TimeoutExpired:
            # Good, the server is running.
            pass

        if (status is not None):
            hint = f"code: '{status}'"
            if (status == 125):
                hint = 'server may already be running'

            raise ValueError(f"Server was unable to start successfully ('{hint}').")

        # Ping the server to check if it has started.
        if (not self.startup_skip_identify):
            for _ in range(IDENTIFY_MAX_ATTEMPTS):
                backend_type = lms.backend.instance.guess_backend_type_from_request(self.server, timeout_secs = IDENTIFY_WAIT_SECS)
                if (backend_type is not None):
                    # The server is running and responding, exit early.
                    return

                time.sleep(IDENTIFY_WAIT_SECS)

        status = None
        try:
            # Ensure the server is running cleanly.
            status = self._process.wait(self.startup_wait_secs)
        except subprocess.TimeoutExpired:
            # Good, the server is running.
            pass

        if (status is not None):
            raise ValueError(f"Server was unable to start successfully ('code: {status}').")

    def stop(self) -> None:
        """ Stop the server. """

        if (self._process is None):
            return

        # Restore networking config.

        lms.cli.parser._set_exchanges_clean_func = self._old_set_exchanges_clean_func
        self._old_set_exchanges_clean_func = False

        edq.util.net._exchanges_out_dir = self._old_exchanges_out_dir
        self._old_exchanges_out_dir = None

        edq.util.net._exchanges_clean_func = self._old_exchanges_clean_func
        self._old_exchanges_clean_func = None

        edq.util.net._make_request_exchange_complete_func = self._old_make_request_exchange_complete_func
        self._old_make_request_exchange_complete_func = None

        # Stop the server.
        logging.info('Stopping the server.')
        self._stop_server()

        if (self._server_output_file is not None):
            self._server_output_file.close()
            self._server_output_file = None

    def restart(self) -> None:
        """ Restart the server. """

        logging.debug('Restarting the server.')
        self._stop_server()
        self._start_server()

    def _stop_server(self) -> typing.Union[int, None]:
        """ Stop the server process and return the exit status. """

        if (self._process is None):
            return None

        # Mark the process as dead, so it can be restarted (if need be).
        current_process = self._process
        self._process = None

        # Check if the process is already dead.
        status = current_process.poll()
        if (status is not None):
            return status

        # If the user provided a special command, try it.
        if (self.server_stop_command is not None):
            subprocess.run(self.server_stop_command,
                    shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL,
                    check = False)

        status = current_process.poll()
        if (status is not None):
            return status

        # Try to end the server gracefully.
        try:
            current_process.send_signal(signal.SIGINT)
            current_process.wait(SERVER_STOP_WAIT_SECS)
        except subprocess.TimeoutExpired:
            pass

        status = current_process.poll()
        if (status is not None):
            return status

        # End the server hard.
        try:
            current_process.kill()
            current_process.wait(SERVER_STOP_WAIT_SECS)
        except subprocess.TimeoutExpired:
            pass

        status = current_process.poll()
        if (status is not None):
            return status

        return None

def modify_parser(parser: argparse.ArgumentParser) -> None:
    """ Modify the parser to add arguments for running a server. """

    parser.add_argument('server_start_command', metavar = 'RUN_SERVER_COMMAND',
        action = 'store', type = str,
        help = 'The command to run the LMS server that will be the target of the data generation commands.')

    parser.add_argument('--startup-skip-identify', dest = 'startup_skip_identify',
        action = 'store_true', default = False,
        help = 'If set, startup will skip trying to identify the server as a means of checking that the server is started.')

    parser.add_argument('--startup-wait', dest = 'startup_wait_secs',
        action = 'store', type = float, default = DEFAULT_STARTUP_WAIT_SECS,
        help = 'The time to wait between starting the server and sending commands (default: %(default)s).')

    parser.add_argument('--server-output-file', dest = 'server_output_path',
        action = 'store', type = str, default = None,
        help = 'Where server output will be written. Defaults to a random temp file.')

    parser.add_argument('--server-stop-command', dest = 'server_stop_command',
        action = 'store', type = str, default = None,
        help = 'An optional command to stop the server. After this the server will be sent a SIGINT and then a SIGKILL.')
