import typing

import edq.util.json

import lms.model.constants

class BaseType(edq.util.json.DictConverter):  # type: ignore[misc]
    """
    The base class for all core LMS types.
    This class ensures that all children have the core functionality necessary for this package.

    The typical structure of types in this package is that types in the model package extend this class.
    Then, backends make declare their own types that extend the other classes from the model package.
    For example: lms.model.base.BaseType -> lms.model.users.CourseUser -> lms.backend.canvas.model.users.CourseUser

    General (but less efficient) implementations of core functions will be provided.
    """

    CORE_FIELDS: list[str] = []
    """
    The common fields shared across backends for this type that are used for comparison and other operations.
    Child classes should set this to define how comparisons are made.
    """

    def __eq__(self, other: object) -> bool:
        if (not isinstance(other, BaseType)):
            return False

        # Check the specified fields only.
        for field_name in self.CORE_FIELDS:
            if (not hasattr(other, field_name)):
                return False

            if (getattr(self, field_name) != getattr(other, field_name)):
                return False

        return True

    def __hash__(self) -> int:
        values = tuple(getattr(self, field_name) for field_name in self.CORE_FIELDS)
        return hash(values)

    def __lt__(self, other: 'BaseType') -> bool:
        if (not isinstance(other, BaseType)):
            return False

        # Check the specified fields only.
        for field_name in self.CORE_FIELDS:
            if (not hasattr(other, field_name)):
                return False

            self_value = getattr(self, field_name)
            other_value = getattr(other, field_name)

            if (self_value == other_value):
                continue

            return bool(self_value < other_value)

        return False

    # TEST - Have a key (CLI option) for the full representation (use all the fields).
    def as_text_rows(self,
            skip_headers: bool = False,
            pretty_headers: bool = False,
            separator: str = ': ',
            empty_value: str = '',
            **kwargs: typing.Any) -> typing.List[str]:
        """
        Create a representation of this object in the "text" style of this project.
        A list of rows will be returned.
        """

        rows = []

        for field_name in self.CORE_FIELDS:
            value = getattr(self, field_name)
            row = _value_to_text(value, empty_value = empty_value)

            if (not skip_headers):
                header = field_name
                if (pretty_headers):
                    header = header.replace('_', ' ').title()

                row = f"{header}{separator}{row}"

            rows.append(row)

        return rows

    # TEST - Have a key (CLI option) for the full representation (use all the fields).
    def get_headers(self,
            pretty_headers: bool = False,
            **kwargs: typing.Any) -> typing.List[str]:
        """
        Get a list of headers to label the values represented by this object.
        This method is a companion to as_table_row(),
        given the same options these two methods will produce rows with the same length and ordering.
        """

        headers = []

        for field_name in self.CORE_FIELDS:
            header = field_name
            if (pretty_headers):
                header = header.replace('_', ' ').title()

            headers.append(header)

        return headers

    # TEST - Have a key (CLI option) for the full representation (use all the fields).
    def as_table_row(self,
            empty_value: str = '',
            **kwargs: typing.Any) -> typing.List[str]:
        """
        Get a list of the values by this object.
        This method is a companion to get_headers(),
        given the same options these two methods will produce rows with the same length and ordering.
        """

        return [_value_to_text(getattr(self, field_name), empty_value = empty_value) for field_name in self.CORE_FIELDS]

def _value_to_text(value: typing.Any,
        empty_value: str = '',
        indent: typing.Union[int, None] = None,
        ) -> str:
    """
    Convert some arbitrary value (usually found within a BaseType) to a string.
    None values will be returned as `empty_value`.
    """

    if (value is None):
        return empty_value

    if (isinstance(value, (edq.util.json.DictConverter, dict, list, tuple))):
        return str(edq.util.json.dumps(value, indent = indent))

    return str(value)

def base_list_to_output_format(values: typing.List[BaseType], output_format: str,
        sort: bool = True,
        skip_headers: bool = False,
        pretty_headers: bool = False,
        empty_value: str = '',
        **kwargs: typing.Any) -> str:
    """
    Convert a list of base types to a string representation.
    The returned string will not include a trailing newline.

    The given list may be modified by this call.
    """

    if (sort):
        values.sort()

    output = ''

    if (output_format == lms.model.constants.OUTPUT_FORMAT_JSON):
        output = base_list_to_json(values, **kwargs)
    elif (output_format == lms.model.constants.OUTPUT_FORMAT_TABLE):
        output = base_list_to_table(values, skip_headers = skip_headers, pretty_headers = pretty_headers, **kwargs)
    elif (output_format == lms.model.constants.OUTPUT_FORMAT_TEXT):
        output = base_list_to_text(values, skip_headers = skip_headers, pretty_headers = pretty_headers, **kwargs)
    else:
        raise ValueError(f"Unknown output format: '{output_format}'.")

    return output

def base_list_to_json(values: typing.List[BaseType],
        indent: int = 4,
        **kwargs: typing.Any) -> str:
    """ Convert a list of base types to a JSON string representation. """

    return str(edq.util.json.dumps(values, indent = indent, **kwargs))

def base_list_to_table(values: typing.List[BaseType],
        skip_headers: bool = False,
        pretty_headers: bool = False,
        empty_value: str = '',
        delim: str = "\t",
        **kwargs: typing.Any) -> str:
    """ Convert a list of base types to a table string representation. """

    rows = []

    if ((len(values) > 0) and (not skip_headers)):
        rows.append(values[0].get_headers(pretty_headers = pretty_headers))

    for value in values:
        rows.append(value.as_table_row(empty_value = empty_value))

    return "\n".join([delim.join(row) for row in rows])

def base_list_to_text(values: typing.List[BaseType],
        skip_headers: bool = False,
        pretty_headers: bool = False,
        empty_value: str = '',
        **kwargs: typing.Any) -> str:
    """ Convert a list of base types to a text string representation. """

    output = []

    for value in values:
        rows = value.as_text_rows(skip_headers = skip_headers, pretty_headers = pretty_headers, empty_value = empty_value)
        output.append("\n".join(rows))

    return "\n\n".join(output)
