import typing

def required_int(raw_value: typing.Any, name: str) -> int:
    """ Parse and clean an int value. """

    if (raw_value is None):
        raise ValueError(f"Value '{name}' is None, when it should be an int.")

    return int(raw_value)

def required_string(raw_value: typing.Any, name: str, **kwargs: typing.Any) -> str:
    """ Parse and clean a string value. """

    value = optional_string(raw_value, **kwargs)
    if (value is None):
        raise ValueError(f"Value '{name}' is None, when it should be a string.")

    return value

def optional_string(raw_value: typing.Any,
        strip: bool = True,
        allow_empty: bool = False,
        **kwargs: typing.Any) -> typing.Union[str, None]:
    """ Parse and clean an optional string value. """

    if (raw_value is None):
        return None

    value = str(raw_value)
    if (strip):
        value = value.strip()

    if ((not allow_empty) and (len(value) == 0)):
        return None

    return value

def optional_float(raw_value: typing.Any, label: str = 'field',
        **kwargs: typing.Any) -> typing.Union[float, None]:
    """ Parse and clean an optional float value. """

    if (raw_value is None):
        return None

    if (isinstance(raw_value, (int, float))):
        return float(raw_value)

    str_value = str(raw_value).strip()

    try:
        return float(str_value)
    except ValueError as ex:
        raise ValueError(f"Unable to parse {label} '{raw_value}' ({type(raw_value)}) as a float.") from ex
