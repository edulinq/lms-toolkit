import re
import typing

import edq.util.json

import lms.model.base
import lms.util.string

T = typing.TypeVar('T')

class BaseQuery(edq.util.json.DictConverter):
    """
    Queries are ways that users can attempt to refer to some object with uncertainty.
    This allows users to refer to objects by name, for example, instead of by id.

    Queries are made up of 2-3 components:
     - an identifier
     - a name
     - an email (optional)

    Email support is decided by child classes.
    By default, ids are assumed to be only digits.

    A query can be represented in text the following ways:
     - LMS ID (`id`)
     - Email (`email`)
     - Full Name (`name`)
     - f"{email} ({id})"
     - f"{name} ({id})"
    """

    _include_email: bool = True
    """ Control if this class instance supports the email field. """

    def __init__(self,
            id: typing.Union[str, int, None] = None,
            name: typing.Union[str, None] = None,
            email: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        if (id is not None):
            id = str(id)

        self.id: typing.Union[str, None] = id
        """ The LMS's identifier for this query. """

        self.name: typing.Union[str, None] = name
        """ The display name of this query. """

        self.email: typing.Union[str, None] = email
        """ The email address of this query. """

        if ((self.id is None) and (self.name is None) and (self.email is None)):
            raise ValueError("Query is empty, it must have at least one piece of information (id, name, email).")

    def match(self, target: typing.Union[typing.Any, 'BaseQuery', None]) -> bool:
        """
        Check if this query matches the given target.
        A missing field in the query means that field will not be checked.
        A missing field in the target is seen as empty and mill by checked against.
        """

        if (target is None):
            return False

        field_names = ['id', 'name']
        if (self._include_email):
            field_names.append('email')

        for field_name in field_names:
            self_value = getattr(self, field_name, None)
            target_value = getattr(target, field_name, None)

            if (self_value is None):
                continue

            if (self_value != target_value):
                return False

        return True

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        data = {
            'id': self.id,
            'name': self.name,
        }

        if (self._include_email):
            data['email'] = self.email

        return data

    def _get_comparison_payload(self, include_id: bool) -> typing.Tuple:
        """ Get values for comparison. """

        payload = []

        if (include_id):
            payload.append(self.id)

        payload.append(self.name)

        if (self._include_email):
            payload.append(self.email)

        return tuple(payload)

    def __eq__(self, other: object) -> bool:
        if (not isinstance(other, BaseQuery)):
            return False

        # Check the ID specially.
        comparison = lms.util.string.compare_maybe_ints(self.id, other.id)
        if (comparison != 0):
            return False

        return self._get_comparison_payload(False) == other._get_comparison_payload(False)

    def __lt__(self, other: object) -> bool:
        if (not isinstance(other, BaseQuery)):
            return False

        # Check the ID specially.
        comparison = lms.util.string.compare_maybe_ints(self.id, other.id)
        if (comparison != 0):
            return (comparison < 0)

        return self._get_comparison_payload(False) < other._get_comparison_payload(False)

    def __hash__(self) -> int:
        return hash(self._get_comparison_payload(True))

    def __str__(self) -> str:
        text = self.email
        if ((not self._include_email) or (text is None)):
            text = self.name

        if (self.id is not None):
            if (text is not None):
                text = f"{text} ({self.id})"
            else:
                text = self.id

        if (text is None):
            return '<unknown>'

        return text

    def _to_text(self) -> str:
        """ Represent this query as a string. """

        return str(self)

class ResolvedBaseQuery(BaseQuery):
    """
    A BaseQuery that has been resolved (verified) from a real instance.
    """

    def __init__(self,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        if (self.id is None):
            raise ValueError("A resolved query cannot be created without an ID.")

    def get_id(self) -> str:
        """ Get the ID (which must exists) for this query. """

        if (self.id is None):
            raise ValueError("A resolved query cannot be created without an ID.")

        return self.id

def parse_int_query(query_type: typing.Type[T], text: typing.Union[str, None],
        check_email: bool = True,
        ) -> typing.Union[T, None]:
    """
    Parse a query with the assumption that LMS ids are ints.

    Accepts queries are in the following forms:
        - LMS ID (`id`)
        - Email (`email`)
        - Name (`name`)
        - f"{email} ({id})"
        - f"{name} ({id})"
    """

    if (text is None):
        return None

    # Clean whitespace.
    text = re.sub(r'\s+', ' ', str(text)).strip()
    if (len(text) == 0):
        return None

    id = None
    email = None
    name = None

    match = re.search(r'^(\S.*)\((\d+)\)$', text)
    if (match is not None):
        # Query has both text and id.
        name = match.group(1).strip()
        id = match.group(2)
    elif (re.search(r'^\d+$', text) is not None):
        # Query must be an ID.
        id = text
    else:
        name = text

    # Check if the name is actually an email address.
    if (check_email and (name is not None) and ('@' in name)):
        email = name
        name = None

    data = {
        'id': id,
        'name': name,
        'email': email,
    }

    return query_type(**data)
