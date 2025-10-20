# pylint: disable=abstract-method

import typing

import lms.model.backend

class MoodleBackend(lms.model.backend.APIBackend):
    """ An API backend for the Moodle LMS. """

    def __init__(self,
            server: str,
            **kwargs: typing.Any) -> None:
        super().__init__(server, **kwargs)
