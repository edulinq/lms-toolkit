import logging
import typing

import edq.net.exchange
import edq.net.request
import edq.testing.serverrunner
import edq.util.parse
import edq.util.reflection

import lms.backend.instance
import lms.cli.parser
import lms.model.constants
import lms.util.net

BACKEND_REQUEST_CLEANING_FUNCS: typing.Dict[typing.Union[str, None], typing.Callable] = {
    lms.model.constants.BACKEND_TYPE_BLACKBOARD: lms.util.net.clean_blackboard_response,
    lms.model.constants.BACKEND_TYPE_CANVAS: lms.util.net.clean_canvas_response,
    lms.model.constants.BACKEND_TYPE_MOODLE: lms.util.net.clean_moodle_response,
}

BACKEND_EXCHANGE_FINALIZING_FUNCS: typing.Dict[typing.Union[str, None], typing.Callable] = {
    lms.model.constants.BACKEND_TYPE_MOODLE: lms.util.net.finalize_moodle_exchange,
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
        The value of edq.net.exchange._exchanges_clean_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_exchanges_finalize_func: typing.Union[str, None] = None
        """
        The value of edq.net.exchange._exchanges_finalize_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_set_exchanges_clean_func: bool = False
        """
        The value of lms.cli.parser._set_exchanges_clean_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_make_request_exchange_complete_func: typing.Union[edq.net.exchange.HTTPExchangeComplete, None] = None
        """
        The value of edq.net.request._make_request_exchange_complete_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_serverrunner_logging_level: typing.Union[int, None] = None
        """
        The logging level for the edq server runner befoe tests are run.
        The original value may be changed in start(), and will be reset in stop().
        """

    def start(self) -> None:
        # Set configs.

        exchange_clean_func = BACKEND_REQUEST_CLEANING_FUNCS.get(self.backend_type, lms.util.net.clean_lms_response)
        exchange_clean_func_name = edq.util.reflection.get_qualified_name(exchange_clean_func)
        self._old_exchanges_clean_func = edq.net.exchange._exchanges_clean_func
        edq.net.exchange._exchanges_clean_func = exchange_clean_func_name

        self._old_exchanges_finalize_func = edq.net.exchange._exchanges_finalize_func
        exchange_finalize_func = BACKEND_EXCHANGE_FINALIZING_FUNCS.get(self.backend_type, None)
        if (exchange_finalize_func is not None):
            exchange_finalize_func_name = edq.util.reflection.get_qualified_name(exchange_finalize_func)
            edq.net.exchange._exchanges_finalize_func = exchange_finalize_func_name
        else:
            edq.net.exchange._exchanges_finalize_func = None

        self._old_set_exchanges_clean_func = lms.cli.parser._set_exchanges_clean_func
        lms.cli.parser._set_exchanges_clean_func = False

        def _make_request_callback(exchange: edq.net.exchange.HTTPExchange) -> None:
            # Restart if the request is a write.
            if (edq.util.parse.boolean(exchange.headers.get(lms.model.constants.HEADER_KEY_WRITE, False))):
                self.restart()

        self._old_make_request_exchange_complete_func = edq.net.request._make_request_exchange_complete_func
        edq.net.request._make_request_exchange_complete_func = typing.cast(edq.net.exchange.HTTPExchangeComplete, _make_request_callback)

        # Disable logging from the runner, since it may disrupt CLI tests.
        logger = logging.getLogger('edq.testing.serverrunner')
        self._old_serverrunner_logging_level = logger.level
        logger.setLevel(logging.WARNING)

        # Start the server.
        super().start()

    def stop(self) -> bool:
        if (self._old_serverrunner_logging_level is not None):
            logger = logging.getLogger('edq.testing.serverrunner')
            logger.setLevel(self._old_serverrunner_logging_level)
            self._old_serverrunner_logging_level = None

        if (not super().stop()):
            return False

        # Restore old configs.

        edq.net.exchange._exchanges_clean_func = self._old_exchanges_clean_func
        self._old_exchanges_clean_func = None

        lms.cli.parser._set_exchanges_clean_func = self._old_set_exchanges_clean_func
        self._old_set_exchanges_clean_func = False

        edq.net.request._make_request_exchange_complete_func = self._old_make_request_exchange_complete_func
        self._old_make_request_exchange_complete_func = None

        return True

    def identify_server(self) ->  bool:
        backend_type = lms.backend.instance.guess_backend_type_from_request(self.server, timeout_secs = self.identify_wait_secs)
        return (backend_type is not None)
