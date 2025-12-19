import logging
import typing

import edq.testing.serverrunner
import edq.util.net
import edq.util.parse
import edq.util.reflection

import lms.backend.instance
import lms.cli.parser
import lms.model.constants
import lms.util.net

BACKEND_REQUEST_CLEANING_FUNCS: typing.Dict[str, typing.Callable] = {
    lms.model.constants.BACKEND_TYPE_BLACKBOARD: lms.util.net.clean_blackboard_response,
    lms.model.constants.BACKEND_TYPE_CANVAS: lms.util.net.clean_canvas_response,
    lms.model.constants.BACKEND_TYPE_MOODLE: lms.util.net.clean_moodle_response,
}

class LMSServerRunner(edq.testing.serverrunner.ServerRunner):
    """ A server runner specifically for LMS servers. """

    def __init__(self,
            backend_type: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.backend_type: typing.Union[str, None] = backend_type
        """
        The type of server being run.
        This value will be resolved after the server is started
        (since part of resolution may involve pinging the server.
        """

        self._old_exchanges_clean_func: typing.Union[str, None] = None
        """
        The value of edq.util.net._exchanges_clean_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_set_exchanges_clean_func: bool = False
        """
        The value of lms.cli.parser._set_exchanges_clean_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_make_request_exchange_complete_func: typing.Union[edq.util.net.HTTPExchangeComplete, None] = None
        """
        The value of edq.util.net._make_request_exchange_complete_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_serverrunner_logging_level: typing.Union[int, None] = None
        """
        The logging level for the edq server runner befoe tests are run.
        The original value may be changed in start(), and will be reset in stop().
        """

    def start(self) -> None:
        super().start()

        # Resolve the backend type.
        self.backend_type = lms.backend.instance.guess_backend_type(self.server, backend_type = self.backend_type)
        if (self.backend_type is None):
            raise ValueError(f"Unable to determine backend type for server '{self.server}'.")

        # Set configs.

        exchange_clean_func = BACKEND_REQUEST_CLEANING_FUNCS.get(self.backend_type, lms.util.net.clean_lms_response)
        exchange_clean_func_name = edq.util.reflection.get_qualified_name(exchange_clean_func)

        self._old_exchanges_clean_func = edq.util.net._exchanges_clean_func
        edq.util.net._exchanges_clean_func = exchange_clean_func_name

        self._old_set_exchanges_clean_func = lms.cli.parser._set_exchanges_clean_func
        lms.cli.parser._set_exchanges_clean_func = False

        def _make_request_callback(exchange: edq.util.net.HTTPExchange) -> None:
            # Restart if the request is a write.
            if (edq.util.parse.boolean(exchange.headers.get(lms.model.constants.HEADER_KEY_WRITE, False))):
                self.restart()

        self._old_make_request_exchange_complete_func = edq.util.net._make_request_exchange_complete_func
        edq.util.net._make_request_exchange_complete_func = typing.cast(edq.util.net.HTTPExchangeComplete, _make_request_callback)

        # Disable logging from the runner, since it may disrupt CLI tests.
        logger = logging.getLogger('edq.testing.serverrunner')
        self._old_serverrunner_logging_level = logger.level
        logger.setLevel(logging.WARNING)

    def stop(self) -> bool:
        if (self._old_serverrunner_logging_level is not None):
            logger = logging.getLogger('edq.testing.serverrunner')
            logger.setLevel(self._old_serverrunner_logging_level)
            self._old_serverrunner_logging_level = None

        if (not super().stop()):
            return False

        # Restore old configs.

        edq.util.net._exchanges_clean_func = self._old_exchanges_clean_func
        self._old_exchanges_clean_func = None

        lms.cli.parser._set_exchanges_clean_func = self._old_set_exchanges_clean_func
        self._old_set_exchanges_clean_func = False

        edq.util.net._make_request_exchange_complete_func = self._old_make_request_exchange_complete_func
        self._old_make_request_exchange_complete_func = None

        return True

    def identify_server(self) ->  bool:
        backend_type = lms.backend.instance.guess_backend_type_from_request(self.server, timeout_secs = self.identify_wait_secs)
        return (backend_type is not None)
