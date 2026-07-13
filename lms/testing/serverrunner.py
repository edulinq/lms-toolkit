import logging
import typing

import edq.core.errors
import edq.net.exchange
import edq.net.request
import edq.net.settings
import edq.testing.serverrunner
import edq.util.parse
import edq.util.reflection

import lms.backend.instance
import lms.cli.parser
import lms.model.backend
import lms.model.constants
import lms.util.net

BACKEND_REQUEST_CLEANING_FUNCS: typing.Dict[typing.Union[lms.model.constants.BackendType, None], typing.Callable] = {
    lms.model.constants.BackendType.BLACKBOARD: lms.util.net.clean_blackboard_response,
    lms.model.constants.BackendType.CANVAS: lms.util.net.clean_canvas_response,
    lms.model.constants.BackendType.MOODLE: lms.util.net.clean_moodle_response,
}

BACKEND_EXCHANGE_FINALIZING_FUNCS: typing.Dict[typing.Union[lms.model.constants.BackendType, None], typing.Callable] = {
    lms.model.constants.BackendType.CANVAS: lms.util.net.finalize_canvas_exchange,
    lms.model.constants.BackendType.MOODLE: lms.util.net.finalize_moodle_exchange,
}

class LMSServerRunner(edq.testing.serverrunner.ServerRunner):
    """ A server runner specifically for LMS servers. """

    def __init__(self,
            backend_type: typing.Union[lms.model.constants.BackendType, str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        if (isinstance(backend_type, str)):
            backend_type = lms.model.constants.BackendType(backend_type)

        self.backend_type: typing.Union[lms.model.constants.BackendType, None] = backend_type
        """
        The type of server being run.
        This value will be resolved after the server is started
        (since part of resolution may involve pinging the server.
        """

        self.backend: typing.Union[lms.model.backend.APIBackend, None] = None
        """
        The backend currently being used while this server runner is active.
        This may not always be set.
        """

        self._old_exchanges_clean_response_func: typing.Union[str, None] = None
        """
        The value of edq.net.settings.get_exchanges_clean_response_func() when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_exchanges_finalize_func: typing.Union[str, None] = None
        """
        The value of edq.net.settings.get_exchanges_finalize_func() when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_set_exchanges_clean_response_func: bool = False
        """
        The value of lms.cli.parser._set_exchanges_clean_response_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_request_complete_callback: typing.Union[edq.net.exchange.HTTPExchangeComplete, None] = None
        """
        The value of edq.net.settings.get_request_complete_callback() when start() is called.
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
        self._old_exchanges_clean_response_func = edq.net.settings.get_exchanges_clean_response_func()
        edq.net.settings.set_exchanges_clean_response_func(exchange_clean_func_name)

        self._old_exchanges_finalize_func = edq.net.settings.get_exchanges_finalize_func()
        exchange_finalize_func = BACKEND_EXCHANGE_FINALIZING_FUNCS.get(self.backend_type, None)
        if (exchange_finalize_func is not None):
            exchange_finalize_func_name = edq.util.reflection.get_qualified_name(exchange_finalize_func)
            edq.net.settings.set_exchanges_finalize_func(exchange_finalize_func_name)
        else:
            edq.net.settings.set_exchanges_finalize_func()

        self._old_set_exchanges_clean_response_func = lms.cli.parser._set_exchanges_clean_response_func
        lms.cli.parser._set_exchanges_clean_response_func = False

        def _request_complete_callback(exchange: edq.net.exchange.HTTPExchange) -> None:
            # Restart if the request is a write.
            if (edq.util.parse.boolean(exchange.headers.get(lms.model.constants.HEADER_KEY_WRITE, False))):
                self.restart()

        self._old_request_complete_callback = edq.net.settings.get_request_complete_callback()
        edq.net.settings.set_request_complete_callback(typing.cast(edq.net.exchange.HTTPExchangeComplete, _request_complete_callback))

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

        edq.net.settings.set_exchanges_clean_response_func(self._old_exchanges_clean_response_func)
        self._old_exchanges_clean_response_func = None

        lms.cli.parser._set_exchanges_clean_response_func = self._old_set_exchanges_clean_response_func
        self._old_set_exchanges_clean_response_func = False

        edq.net.settings.set_request_complete_callback(self._old_request_complete_callback)
        self._old_request_complete_callback = None

        edq.net.settings.set_exchanges_finalize_func(self._old_exchanges_finalize_func)
        self._old_exchanges_finalize_func = None

        return True

    def restart(self) -> None:
        super().restart()

        # Inform the backend that a restart happened.
        if (self.backend is not None):
            self.backend.reset_connection()

    def identify_server(self) ->  bool:
        try:
            backend_type = lms.backend.instance.guess_backend_type_from_request(self.server, timeout_secs = self.identify_wait_secs)
        except edq.core.errors.RetryError:
            return False

        return (backend_type is not None)
