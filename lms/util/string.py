import re
import typing

INT_PATTERN: re.Pattern = re.compile(r'^\d+$')

def compare_maybe_ints(a: typing.Union[str, int, None], b: typing.Union[str, int, None]) -> int:
    """
    Perform a standard comparison (-1, 0, 1) on two strings that are presumed to be integers.
    If they are not integers, compare them as strings.
    """

    if ((a is None) or (b is None)):
        if ((a is None) and (b is None)):
            return 0

        if (a is None):
            return -1

        return 1

    values = [a, b]
    has_str = False

    for (i, value) in enumerate(values):
        if (isinstance(value, int)):
            continue

        value = str(value)
        if (INT_PATTERN.match(value) is not None):
            value = int(value)
        else:
            has_str = True

        values[i] = value

    if (has_str):
        values = [str(value) for value in values]

    if (values[0] < values[1]):  # type: ignore[operator]
        return -1

    if (values[0] > values[1]):  # type: ignore[operator]
        return 1

    return 0
