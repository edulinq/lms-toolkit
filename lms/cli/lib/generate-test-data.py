# pylint: disable=invalid-name

"""
Generate test data by starting the specified server and running all tests in this project.
"""

import argparse
import os
import signal
import subprocess
import sys
import typing

import edq.testing.run

import lms.backend.backend
import lms.backend.testing
import lms.cli.parser

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
PACKAGE_ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..')

DEFAULT_STARTUP_WAIT_SECS: float = 10.0
SERVER_STOP_WAIT_SECS: float = 5.00

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    server = config.get('server', None)
    if (server is None):
        print('ERROR: No server address (e.g., `--server`).')
        return 1

    if (args.http_exchanges_out_dir is None):
        print('ERROR: No HTTP exchange output directory (`--http-exchanges-out-dir`) was supplied.')
        return 2

    # Start the target server.
    # The server must be started before guessing the backend, since the server may need to be pinged.

    print(f"Writing server output to '{args.server_output_path}'.")
    server_output_file = open(args.server_output_path, 'a')

    print(f"Starting the server and waiting {args.startup_wait_secs} seconds.")
    process = _start_server(args, server_output_file)

    backend_type = lms.backend.backend.guess_backend_type(args.server, backend_type = config.get('backend_type', None))
    if (backend_type is None):
        print(f"ERROR: Unable to determine backend type for server ('{server}'), consider setting manually with `--server-type`.")
        return 3

    # Configure backend tests.
    lms.backend.testing.BackendTest.allowed_backend = backend_type
    lms.backend.testing.BackendTest.skip_test_exchanges_base = True
    lms.backend.testing.BackendTest.override_server_url = server

    # Run the tests (which generate the data).
    failure_count = int(edq.testing.run.run())

    # Stop the target server.
    print('Stopping the server.')
    _stop_server(args, process)

    server_output_file.close()

    return failure_count

def _start_server(args: argparse.Namespace, server_output_file: typing.IO) -> subprocess.Popen:
    """ Start and return the server process. """

    process = subprocess.Popen(args.command, shell = True, stdout = server_output_file, stderr = subprocess.STDOUT)

    status = None
    try:
        # Ensure the server is running cleanly.
        status = process.wait(args.startup_wait_secs)
    except subprocess.TimeoutExpired:
        # Good, the server is running.
        pass

    if (status is not None):
        raise ValueError("Server was unable to start successfully (code: '%s')." % (str(status)))

    return process

def _stop_server(args: argparse.Namespace, process: typing.Union[subprocess.Popen, None]) -> typing.Union[int, None]:
    """ Try to stop the server process and return the exit status. """

    if (process is None):
        return None

    # Check if the process is already dead.
    status = process.poll()
    if (status is not None):
        return status

    # If the user provided a special command, try it.
    if (args.server_stop_command is not None):
        subprocess.run(args.server_stop_command, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    status = process.poll()
    if (status is not None):
        return status

    # Try to end the server gracefully.
    try:
        process.send_signal(signal.SIGINT)
        process.wait(SERVER_STOP_WAIT_SECS)
    except subprocess.TimeoutExpired:
        pass

    status = process.poll()
    if (status is not None):
        return status

    # End the server hard.
    try:
        process.kill()
        process.wait(SERVER_STOP_WAIT_SECS)
    except subprocess.TimeoutExpired:
        pass

    status = process.poll()
    if (status is not None):
        return status

    return None

def _reset_server(
        process: typing.Union[subprocess.Popen, None],
        args: argparse.Namespace,
        server_output_file: typing.IO,
        ) -> typing.Tuple[typing.Union[int, None], subprocess.Popen]:
    """ Restart (stop and start) the server. """

    # Stop the previous server.
    status = _stop_server(args, process)

    # Start a new server.
    process = _start_server(args, server_output_file)

    return status, process

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip())

    parser.add_argument('command', metavar = 'RUN_SERVER_COMMAND',
        action = 'store', type = str,
        help = 'The command to run the LMS server that will be the target of the data generation commands.')

    parser.add_argument('--startup-wait', dest = 'startup_wait_secs',
        action = 'store', type = float, default = DEFAULT_STARTUP_WAIT_SECS,
        help = 'The time to wait between starting the server and sending commands (default: %(default)s).')

    parser.add_argument('--server-output-file', dest = 'server_output_path',
        action = 'store', type = str, default = edq.util.dirent.get_temp_path(prefix = 'lms-data-generation-', rm = False),
        help = 'The time to wait between starting the server and sending commands (default: %(default)s).')

    parser.add_argument('--server-stop-command', dest = 'server_stop_command',
        action = 'store', type = str, default = None,
        help = 'An optional command to stop the server. After this the server will be sent a SIGINT and then a SIGKILL.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
