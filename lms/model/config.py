import typing

import edq.config.app
import edq.util.crypto

import lms.model.constants

class Config(edq.config.app.BaseApplicationConfig):
    """
    An application config for the LMS Toolkit.
    """

    def __init__(self,
            server: typing.Union[str, None] = None,
            backend_type: typing.Union[str, None] = None,
            auth_user: typing.Union[str, None] = None,
            auth_password: typing.Union[edq.util.crypto.Secret, None] = None,
            auth_token: typing.Union[edq.util.crypto.Secret, None] = None,
            course: typing.Union[str, None] = None,
            assignment: typing.Union[str, None] = None,
            quiz: typing.Union[str, None] = None,
            user: typing.Union[str, None] = None,
            group: typing.Union[str, None] = None,
            groupset: typing.Union[str, None] = None,
            output_format: typing.Union[lms.model.constants.OutputFormat, None] = None,
            include_extra_fields: typing.Union[bool, None] = None,
            pretty_headers: typing.Union[bool, None] = None,
            skip_headers: typing.Union[bool, None] = None,
            skip_rows: typing.Union[int, None] = None,
            strict: typing.Union[bool, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.server: typing.Union[str, None] = server
        """ The address of the LMS server to connect to. """

        self.backend_type: typing.Union[str, None] = backend_type
        """ The type of LMS being connected to (this can normally be guessed from the server address). """

        self.auth_user: typing.Union[str, None] = auth_user
        """ The user to authenticate with. """

        self.auth_password: typing.Union[edq.util.crypto.Secret, None] = auth_password
        """ The password to authenticate with. """

        self.auth_token: typing.Union[edq.util.crypto.Secret, None] = auth_token
        """ The token to authenticate with. """

        self.course: typing.Union[str, None] = course
        """ The course to target for this operation. """

        self.assignment: typing.Union[str, None] = assignment
        """ The assignment to target for this operation. """

        self.quiz: typing.Union[str, None] = quiz
        """ The quiz to target for this operation. """

        self.user: typing.Union[str, None] = user
        """ The user to target for this operation. """

        self.group: typing.Union[str, None] = group
        """ The group to target for this operation. """

        self.groupset: typing.Union[str, None] = groupset
        """ The group set to target for this operation. """

        self.output_format: typing.Union[lms.model.constants.OutputFormat, None] = output_format
        """ The format to display the output as. """

        self.include_extra_fields: typing.Union[bool, None] = include_extra_fields
        """ Include non-common (usually LMS-specific) fields in results. """

        self.pretty_headers: typing.Union[bool, None] = pretty_headers
        """ When displaying headers, try to make them look "pretty". """

        self.skip_headers: typing.Union[bool, None] = skip_headers
        """ Skip headers when outputting results, will not apply to all formats. """

        self.skip_rows: typing.Union[int, None] = skip_rows
        """ The number of header rows to skip. """

        self.strict: typing.Union[bool, None] = strict
        """ Enable strict mode, which is stricter about what counts as an error. """

        # TEST - testing?
