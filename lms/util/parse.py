import typing

def required_int(raw_value: typing.Any, name: str) -> int:
    """ Parse and clean an int value. """

    if (raw_value is None):
        raise ValueError(f"Value '{name}' is None, when it should be an int.")

    return int(raw_value)

def required_string(raw_value: typing.Any, name: str, strip: bool = True) -> str:
    """ Parse and clean a string value. """

    value = optional_string(raw_value, name, strip = strip)

    if (value is None):
        raise ValueError(f"Value '{name}' is None, when it should be a string.")

    return value

def optional_string(raw_value: typing.Any, name: str, strip: bool = True) -> typing.Union[str, None]:
    """ Parse and clean an optional string value. """

    if (raw_value is None):
        return None

    value = str(raw_value)
    if (strip):
        value = value.strip()

    return value
