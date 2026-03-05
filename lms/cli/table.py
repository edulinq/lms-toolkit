"""
Read table data from TSV files with automatic header detection.
"""

import typing
import edq.util.dirent

def _is_header_row(
        parts: typing.List[str],
        required_columns: typing.List[str],
) -> bool:
    """
    Check if a row is a header by verifying all required column names are present.
    """

    lowered = {part.lower() for part in parts}
    for column in required_columns:
        if (column not in lowered):
            return False

    return True

def read_table(
        path: str,
        columns: typing.List[str],
        skip_rows: int = 0,
        optional_columns: typing.Optional[typing.List[str]] = None,
) -> typing.List[typing.Tuple[int, typing.Dict[str, str]]]:
    """
    Read a TSV file and return rows as (line_number, column_dict) tuples.

    If the first data row contains all required column names (case-insensitive),
    it is treated as a header and used for column mapping.
    Otherwise, columns are mapped positionally in the order given.

    Extra columns in a header row are silently ignored.
    Missing optional columns are omitted from the row dict.
    """

    if (optional_columns is None):
        optional_columns = []

    all_known = set(columns) | set(optional_columns)
    rows: typing.List[typing.Tuple[int, typing.Dict[str, str]]] = []
    header_map: typing.Optional[typing.Dict[str, int]] = None
    checked_header = False

    with open(path, 'r', encoding = edq.util.dirent.DEFAULT_ENCODING) as file:
        lineno = 0
        real_rows = 0
        for line in file:
            lineno += 1

            if (line.strip() == ''):
                continue

            real_rows += 1

            if (real_rows <= skip_rows):
                continue

            parts = [part.strip() for part in line.split("\t")]

            # On the first data row, check for a header.
            if (not checked_header):
                checked_header = True
                if (_is_header_row(parts, columns)):
                    header_map = {}
                    for (i, part) in enumerate(parts):
                        name = part.lower()
                        if (name in all_known):
                            header_map[name] = i
                    continue

            # Build the row dict.
            row: typing.Dict[str, str] = {}

            if (header_map is not None):
                for col in columns:
                    idx = header_map[col]
                    if (idx < len(parts)):
                        row[col] = parts[idx]
                    else:
                        raise ValueError(
                            f"File '{path}' line {lineno} has the incorrect number of values."
                            + f" Expecting at least {max(header_map.values()) + 1},"
                            + f" found {len(parts)}.")

                for col in optional_columns:
                    if (col in header_map):
                        idx = header_map[col]
                        if (idx < len(parts)):
                            row[col] = parts[idx]
            else:
                min_cols = len(columns)
                max_cols = len(columns) + len(optional_columns)
                if (len(parts) < min_cols or len(parts) > max_cols):
                    if (min_cols == max_cols):
                        raise ValueError(
                            f"File '{path}' line {lineno} has the incorrect number of values."
                            + f" Expecting {min_cols}, found {len(parts)}.")

                    raise ValueError(
                        f"File '{path}' line {lineno} has the incorrect number of values."
                        + f" Expecting {min_cols}-{max_cols}, found {len(parts)}.")

                for (i, col) in enumerate(columns):
                    row[col] = parts[i]

                for (i, col) in enumerate(optional_columns, start = len(columns)):
                    if (i < len(parts)):
                        row[col] = parts[i]

            rows.append((lineno, row))

    return rows
