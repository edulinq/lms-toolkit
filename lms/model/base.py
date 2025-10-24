import typing

import edq.util.json

import lms.model.constants
import lms.util.string

TEXT_SEPARATOR: str = ': '
TEXT_EMPTY_VALUE: str = ''

T = typing.TypeVar('T', bound = 'BaseType')

class BaseType(edq.util.json.DictConverter):
    """
    The base class for all core LMS types.
    This class ensures that all children have the core functionality necessary for this package.

    The typical structure of types in this package is that types in the model package extend this class.
    Then, backends may declare their own types that extend the other classes from the model package.
    For example: lms.model.base.BaseType -> lms.model.assignments.Assignment -> lms.backend.canvas.model.assignments.Assignment

    General (but less efficient) implementations of core functions will be provided.
    """

    CORE_FIELDS: typing.List[str] = []
    """
    The common fields shared across backends for this type that are used for comparison and other operations.
    Child classes should set this to define how comparisons are made.
    """

    INT_COMPARISON_FIELDS: typing.Set[str] = {'id'}
    """
    Fields that should be compared like ints (even if they are strings).
    By default, this set will include 'id'.
    """

    def __init__(self,
            **kwargs: typing.Any) -> None:
        self.extra_fields: typing.Dict[str, typing.Any] = kwargs.copy()
        """ Additional fields not common to all backends or explicitly used by the creating child backend. """

    def __eq__(self, other: object) -> bool:
        if (not isinstance(other, BaseType)):
            return False

        # Check the specified fields only.
        for field_name in self.CORE_FIELDS:
            if (not hasattr(other, field_name)):
                return False

            value_self = getattr(self, field_name)
            value_other = getattr(other, field_name)

            if (field_name in self.INT_COMPARISON_FIELDS):
                comparison = lms.util.string.compare_maybe_ints(value_self, value_other)
                if (comparison != 0):
                    return False
            elif (value_self != value_other):
                return False

        return True

    def __hash__(self) -> int:
        values = tuple(getattr(self, field_name) for field_name in self.CORE_FIELDS)
        return hash(values)

    def __lt__(self, other: 'BaseType') -> bool:  # type: ignore[override]
        if (not isinstance(other, BaseType)):
            return False

        # Check the specified fields only.
        for field_name in self.CORE_FIELDS:
            if (not hasattr(other, field_name)):
                return False

            value_self = getattr(self, field_name)
            value_other = getattr(other, field_name)

            if (field_name in self.INT_COMPARISON_FIELDS):
                comparison = lms.util.string.compare_maybe_ints(value_self, value_other)
                if (comparison == 0):
                    continue

                return (comparison < 0)

            if (value_self == value_other):
                continue

            return bool(value_self < value_other)

        return False

    def as_text_rows(self,
            skip_headers: bool = False,
            pretty_headers: bool = False,
            **kwargs: typing.Any) -> typing.List[str]:
        """
        Create a representation of this object in the "text" style of this project meant for display.
        A list of rows will be returned.
        """

        rows = []

        for (field_name, row) in self._get_fields(**kwargs).items():
            if (not skip_headers):
                header = field_name
                if (pretty_headers):
                    header = header.replace('_', ' ').title()

                row = f"{header}{TEXT_SEPARATOR}{row}"

            rows.append(row)

        return rows

    def get_headers(self,
            pretty_headers: bool = False,
            **kwargs: typing.Any) -> typing.List[str]:
        """
        Get a list of headers to label the values represented by this object meant for display.
        This method is a companion to as_table_rows(),
        given the same options these two methods will produce rows with the same length and ordering.
        """

        headers = []

        for field_name in self._get_fields(**kwargs):
            header = field_name
            if (pretty_headers):
                header = header.replace('_', ' ').title()

            headers.append(header)

        return headers

    def as_table_rows(self,
            **kwargs: typing.Any) -> typing.List[typing.List[str]]:
        """
        Get a list of the values by this object meant for display.
        This method is a companion to get_headers(),
        given the same options these two methods will produce rows with the same length and ordering.

        Note that the default implementation for this method always return a single row,
        but children may override and return multiple rows per object.
        """

        return [list(self._get_fields(**kwargs).values())]

    def as_json_dict(self,
            **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        """
        Get a dict representation of this object meant for display as JSON.
        (Note that we are not returning JSON, just a dict that is ready to be converted to JSON.)
        Calling this method differs from passing this object to json.dumps() (or any sibling),
        because this method may not include all fields, may flatten or alter fields, and will order fields differently.
        """

        return {field_name: self._get_field_value(field_name) for field_name in self._get_fields(**kwargs)}

    def _get_fields(self,
            include_extra_fields: bool = False,
            **kwargs: typing.Any) -> typing.Dict[str, str]:
        """
        Get a dictionary representing the "target" fields of this object meant for display.
        Keys (field names) will not be modified, but values will be sent to self._value_to_text().
        Keys are placed in the dictionary in a consistent ordering.
        """

        field_names = self.CORE_FIELDS.copy()

        # Append any extra fields after the core fields.
        if (include_extra_fields):
            # First, include any fields that are not in self.extra_fields.
            for extra_name in (list(vars(self).keys()) + list(self.extra_fields.keys())):
                if (extra_name == 'extra_fields'):
                    continue

                if (extra_name not in field_names):
                    field_names.append(extra_name)

        fields = {}
        for field_name in field_names:
            fields[field_name] = self._value_to_text(self._get_field_value(field_name), **kwargs)

        return fields

    def _get_field_value(self, name: str, default: typing.Any = None) -> typing.Any:
        """
        Get the value for a field.
        This is similar to `getattr(self, name, default)`,
        but this will also check `extra_fields` if the field is not found at the top level.
        """

        if (hasattr(self, name)):
            return getattr(self, name)

        if (name in self.extra_fields):
            return self.extra_fields[name]

        return default

    def _value_to_text(self,
            value: typing.Any,
            indent: typing.Union[int, None] = None,
            **kwargs: typing.Any) -> str:
        """
        Convert some arbitrary value (usually found within a BaseType) to a string.
        None values will be returned as `TEXT_EMPTY_VALUE`.
        """

        if (value is None):
            return TEXT_EMPTY_VALUE

        if (hasattr(value, '_to_text')):
            return str(value._to_text())

        if (isinstance(value, (edq.util.json.DictConverter, dict, list, tuple))):
            return str(edq.util.json.dumps(value, indent = indent))

        return str(value)

    @classmethod
    def from_json_dict(cls: typing.Type[T],
            data: typing.Dict[str, typing.Any],
            **kwargs: typing.Any) -> T:
        """
        Create an object from a dict that can be used for JSON.
        This is the inverse of as_json_dict().
        """

        return typing.cast(T, cls.from_dict(data))

def base_list_to_output_format(values: typing.Sequence[BaseType], output_format: str,
        sort: bool = True,
        skip_headers: bool = False,
        pretty_headers: bool = False,
        include_extra_fields: bool = False,
        **kwargs: typing.Any) -> str:
    """
    Convert a list of base types to a string representation.
    The returned string will not include a trailing newline.

    The given list may be modified by this call.
    """

    values = list(values)

    if (sort):
        values.sort()

    output = ''

    if (output_format == lms.model.constants.OUTPUT_FORMAT_JSON):
        output = base_list_to_json(values,
                include_extra_fields = include_extra_fields,
                **kwargs)
    elif (output_format == lms.model.constants.OUTPUT_FORMAT_TABLE):
        output = base_list_to_table(values,
                skip_headers = skip_headers, pretty_headers = pretty_headers,
                include_extra_fields = include_extra_fields,
                **kwargs)
    elif (output_format == lms.model.constants.OUTPUT_FORMAT_TEXT):
        output = base_list_to_text(values,
                skip_headers = skip_headers, pretty_headers = pretty_headers,
                include_extra_fields = include_extra_fields,
                **kwargs)
    else:
        raise ValueError(f"Unknown output format: '{output_format}'.")

    return output

def base_list_to_json(values: typing.Sequence[BaseType],
        indent: int = 4,
        extract_single_list: bool = False,
        **kwargs: typing.Any) -> str:
    """ Convert a list of base types to a JSON string representation. """

    output_values = [value.as_json_dict(**kwargs) for value in values]
    if (extract_single_list and (len(output_values) == 1)):
        output_values = output_values[0]  # type: ignore[assignment]

    return str(edq.util.json.dumps(output_values, indent = indent, sort_keys = False))

def base_list_to_table(values: typing.Sequence[BaseType],
        skip_headers: bool = False,
        delim: str = "\t",
        **kwargs: typing.Any) -> str:
    """ Convert a list of base types to a table string representation. """

    rows = []

    if ((len(values) > 0) and (not skip_headers)):
        rows.append(values[0].get_headers(**kwargs))

    for value in values:
        rows += value.as_table_rows(**kwargs)

    return "\n".join([delim.join(row) for row in rows])

def base_list_to_text(values: typing.Sequence[BaseType],
        **kwargs: typing.Any) -> str:
    """ Convert a list of base types to a text string representation. """

    output = []

    for value in values:
        rows = value.as_text_rows(**kwargs)
        output.append("\n".join(rows))

    return "\n\n".join(output)
