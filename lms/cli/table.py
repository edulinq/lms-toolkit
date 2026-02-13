"""
Utilities for reading TSV table files with optional headers.
"""

import typing

import edq.util.dirent

class ColumnDef:
    """
    Definition of an expected column in a table file.
    """

    def __init__(self, name: str, required: bool = True):
        self.name = name
        self.required = required

# A row returned by read_table: (line_number, values).
TableRow = typing.Tuple[int, typing.List[typing.Union[str, None]]]

def read_table(
        path: str,
        columns: typing.List[ColumnDef],
        skip_rows: int = 0,
        has_header: bool = False,
        ) -> typing.List[TableRow]:
    """
    Read a TSV file and return rows as (lineno, values) tuples,
    where values are aligned to the given columns order.

    When has_header is True:
      - The first non-empty row is parsed as column names (case-insensitive match).
      - Missing required columns raise a ValueError.
      - Missing optional columns get None in that position.
      - Extra columns (not in the columns list) are ignored.
      - Remaining rows are mapped via header positions.

    When has_header is False:
      - skip_rows non-empty rows are skipped.
      - Rows are mapped positionally (current behavior).
      - Column count must be between the number of required columns and the total number of columns.
    """

    if (has_header and (skip_rows > 0)):
        raise ValueError("Cannot use both --header and --skip-rows.")

    rows: typing.List[TableRow] = []
    column_mapping: typing.Union[typing.List[typing.Union[int, None]], None] = None

    required_count = sum(1 for col in columns if col.required)

    with open(path, 'r', encoding = edq.util.dirent.DEFAULT_ENCODING) as file:
        lineno = 0
        real_rows = 0
        header_parsed = False

        for line in file:
            lineno += 1

            if (line.strip() == ''):
                continue

            real_rows += 1

            parts = [part.strip() for part in line.split("\t")]

            # Parse header row.
            if (has_header and (not header_parsed)):
                header_parsed = True
                column_mapping = _parse_header(path, lineno, parts, columns)
                continue

            # Skip rows (non-header mode).
            if ((not has_header) and (real_rows <= skip_rows)):
                continue

            # Map row to column order.
            if (column_mapping is not None):
                row = _map_row_with_header(path, lineno, parts, columns, column_mapping)
            else:
                row = _map_row_positional(path, lineno, parts, columns, required_count)

            rows.append((lineno, row))

    return rows

def _parse_header(
        path: str,
        lineno: int,
        parts: typing.List[str],
        columns: typing.List[ColumnDef],
        ) -> typing.List[typing.Union[int, None]]:
    """
    Parse a header row and return a column mapping.
    The mapping is a list aligned to the columns list,
    where each entry is the index in the header row for that column (or None if absent).
    """

    known_names = {col.name.lower(): i for (i, col) in enumerate(columns)}

    # Map header values to their positions in the row.
    header_index: typing.Dict[str, int] = {}
    for (i, part) in enumerate(parts):
        normalized = part.lower()
        if (normalized in known_names):
            if (normalized in header_index):
                raise ValueError(f"File '{path}' line {lineno} has a duplicate header column: '{part}'.")
            header_index[normalized] = i

    # Build column mapping: for each defined column, find its index in the header row.
    column_mapping: typing.List[typing.Union[int, None]] = []
    for col in columns:
        col_name = col.name.lower()
        if (col_name in header_index):
            column_mapping.append(header_index[col_name])
        elif (col.required):
            raise ValueError(f"File '{path}' line {lineno} is missing required header column: '{col.name}'.")
        else:
            column_mapping.append(None)

    return column_mapping

def _map_row_with_header(
        path: str,
        lineno: int,
        parts: typing.List[str],
        columns: typing.List[ColumnDef],
        column_mapping: typing.List[typing.Union[int, None]],
        ) -> typing.List[typing.Union[str, None]]:
    """
    Map a data row using the header-derived column mapping.
    """

    row: typing.List[typing.Union[str, None]] = []
    for (i, col_index) in enumerate(column_mapping):
        if (col_index is None):
            row.append(None)
        elif (col_index >= len(parts)):
            if (columns[i].required):
                raise ValueError(f"File '{path}' line {lineno} is missing a value for required column '{columns[i].name}'.")
            row.append(None)
        else:
            row.append(parts[col_index])

    return row

def _map_row_positional(
        path: str,
        lineno: int,
        parts: typing.List[str],
        columns: typing.List[ColumnDef],
        required_count: int,
        ) -> typing.List[typing.Union[str, None]]:
    """
    Map a data row positionally (no header mode).
    """

    if ((len(parts) < required_count) or (len(parts) > len(columns))):
        if (required_count == len(columns)):
            expecting = str(required_count)
        else:
            expecting = f"{required_count}-{len(columns)}"

        raise ValueError(f"File '{path}' line {lineno} has the incorrect number of values."
                + f" Expecting {expecting}, found {len(parts)}.")

    row: typing.List[typing.Union[str, None]] = []
    for i in range(len(columns)):
        if (i < len(parts)):
            row.append(parts[i])
        else:
            row.append(None)

    return row
