import typing

import lms.model.users

CORE_FIELDS: typing.List[str] = [
    'id',
    'email',
]

class CourseUser(lms.model.users.CourseUser):
    """
    A Canvas user associated with a course.

    See: https://developerdocs.instructure.com/services/canvas/resources/users
    """

    def __init__(self,
            sortable_name: typing.Union[str, None] = None,
            last_name: typing.Union[str, None] = None,
            first_name: typing.Union[str, None] = None,
            short_name: typing.Union[str, None] = None,
            sis_user_id: typing.Union[str, None] = None,
            sis_import_id: typing.Union[int, None] = None,
            integration_id: typing.Union[str, None] = None,
            avatar_url: typing.Union[str, None] = None,
            avatar_state: typing.Union[str, None] = None,
            enrollments: typing.Union[typing.Any, None] = None,
            locale: typing.Union[str, None] = None,
            last_login: typing.Union[str, None] = None,
            time_zone: typing.Union[str, None] = None,
            bio: typing.Union[str, None] = None,
            pronouns: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        # Check for important fields.
        for field in CORE_FIELDS:
            if (field not in kwargs):
                raise ValueError(f"Canvas user is missing '{field}'.")

        # Modify specific arguments before sending them to super.
        kwargs['id'] = str(kwargs['id'])
        kwargs['username'] = kwargs.get('login_id', None)

        super().__init__(**kwargs)

        self.sortable_name: typing.Union[str, None] = sortable_name
        """
        The name of the user that is should be used for sorting groups of users, such as in the gradebook.
        """

        self.last_name: typing.Union[str, None] = last_name
        """
        The last name of the user.
        """

        self.first_name: typing.Union[str, None] = first_name
        """
        The first name of the user.
        """

        self.short_name: typing.Union[str, None] = short_name
        """
        A short name the user has selected, for use in conversations or other less formal places through the site.
        """

        self.sis_user_id: typing.Union[str, None] = sis_user_id
        """
        The SIS ID associated with the user
        This field is only included if the user came from a SIS import and has permissions to view SIS information.
        """

        self.sis_import_id: typing.Union[int, None] = sis_import_id
        """
        The id of the SIS import.
        This field is only included if the user came from a SIS import and has permissions to manage SIS information.
        """

        self.integration_id: typing.Union[str, None] = integration_id
        """
        The integration_id associated with the user.
        This field is only included if the user came from a SIS import and has permissions to view SIS information.
        """

        self.avatar_url: typing.Union[str, None] = avatar_url
        """
        If avatars are enabled, this field will be included and contain a url to retrieve the user's avatar.
        """

        self.avatar_state: typing.Union[str, None] = avatar_state
        """
        If avatars are enabled and caller is admin, this field can be requested and will contain the current state of the user's avatar.
        """

        # TODO(eriq) - Resolve type.
        self.enrollments: typing.Union[typing.Any, None] = enrollments
        """
        This field can be requested with certain API calls, and will return a list of the users active enrollments.
        See the List enrollments API for more details about the format of these records.
        """

        self.locale: typing.Union[str, None] = locale
        """
        This field can be requested with certain API calls, and will return the users locale in RFC 5646 format.
        """

        self.last_login: typing.Union[str, None] = last_login
        """
        This field is only returned in certain API calls,
        and will return a timestamp representing the last time the user logged in to canvas.
        """

        self.time_zone: typing.Union[str, None] = time_zone
        """
        This field is only returned in certain API calls, and will return IANA time zone name of the user's preferred timezone.
        """

        self.bio: typing.Union[str, None] = bio
        """
        Optional: The user's bio.
        """

        self.pronouns: typing.Union[str, None] = pronouns
        """
        This field is only returned if pronouns are enabled, and will return the pronouns of the user.
        """
