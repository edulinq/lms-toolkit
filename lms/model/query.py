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

    Queries are made up of 2-4 components:
     - an identifier
     - a name
     - an email (optional)
     - a student_id (optional)

    Email and student_id support is decided by child classes.
    By default, ids are assumed to be only digits.

    A query can be represented in text the following ways:
     - LMS ID (`id`)
     - Email (`email`)
     - Full Name (`name`)
     - Student ID (`student_id`)
     - f"{email} ({id})"
     - f"{name} ({id})"
     - f"{name} [{student_id}] ({id})"
    """

    _include_email: bool = True
    """ Control if this class instance supports the email field. """

    _include_student_id: bool = False
    """ Control if this class instance supports the student_id field. """

    def __init__(self,
            id: typing.Union[str, int, None] = None,
            name: typing.Union[str, None] = None,
            email: typing.Union[str, None] = None,
            student_id: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        if (id is not None):
            id = str(id)

        self.id: typing.Union[str, None] = id
        """ The LMS's identifier for this query. """

        self.name: typing.Union[str, None] = name
        """ The display name of this query. """

        self.email: typing.Union[str, None] = email
        """ The email address of this query. """

        self.student_id: typing.Union[str, None] = student_id
        """ The student ID (also known as SIS ID) for this query. """

        if ((self.id is None) and (self.name is None) and (self.email is None) and (self.student_id is None)):
            raise ValueError("Query is empty, it must have at least one piece of information (id, name, email, student_id).")

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
        if (self._include_student_id):
            field_names.append('student_id')

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

        if (self._include_student_id):
            data['student_id'] = self.student_id

        return data

    def _get_comparison_payload(self, include_id: bool) -> typing.Tuple:
        """ Get values for comparison. """

        payload = []

        if (include_id):
            payload.append(self.id)

        payload.append(self.name)

        if (self._include_email):
            payload.append(self.email)

        if (self._include_student_id):
            payload.append(self.student_id)

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

        # Add student ID in brackets if available.
        if (self._include_student_id and (self.student_id is not None)):
            if (text is not None):
                text = f"{text} [{self.student_id}]"
            else:
                text = self.student_id

        # Add LMS ID in parentheses.
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
        - Student ID (`student_id`)
        - f"{email} ({id})"
        - f"{name} ({id})"
        - f"{name} [{student_id}] ({id})"
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
    student_id = None

    # Try to match: "name [student_id] (id)".
    match = re.search(r'^(\S.*)\[([^\]]+)\]\s*\((\d+)\)$', text)
    if (match is not None):
        name = match.group(1).strip()
        student_id = match.group(2).strip()
        id = match.group(3)
    # Try to match: "name (id)".
    elif (match := re.search(r'^(\S.*)\((\d+)\)$', text)) is not None:
        name = match.group(1).strip()
        id = match.group(2)
    # Try to match: just a number (LMS ID).
    elif (re.search(r'^\d+$', text) is not None):
        id = text
    else:
        # It's a name or email.
        name = text

    # Check if the name is actually an email address.
    if (check_email and (name is not None) and ('@' in name)):
        email = name
        name = None

    data = {
        'id': id,
        'name': name,
        'email': email,
        'student_id': student_id,
    }

    return query_type(**data)
