"""
Utility for reading and parsing TSV (tab-separated values) files.
"""

import typing

import edq.util.dirent

class TSVRow:
    """ A single row from a TSV file. """

    def __init__(
            self,
            parts: typing.List[str],
            lineno: int,
            effective_lineno: int,
            ) -> None:
        self.parts = parts
        self.lineno = lineno
        self.effective_lineno = effective_lineno

    def raise_error(self, message: str) -> typing.NoReturn:
        """ Raise a ValueError with this row's line context prepended. """

        raise ValueError(
            f"Line {self.lineno}"
            f" (effective {self.effective_lineno}): {message}"
        )

class TSVFile:
    """ A parsed TSV file with header metadata and a column index map. """

    def __init__(
            self,
            headers: typing.Union[typing.List[str], None],
            rows: typing.List[TSVRow],
            header_map: typing.Dict[str, typing.Union[int, None]],
            ) -> None:
        self.headers = headers
        self.rows = rows
        self.header_map = header_map

    def to_dicts(self) -> typing.List[typing.Dict[str, str]]:
        """ Convert the TSV rows to a list of dicts keyed by column name. """

        result = []
        for row in self.rows:
            entry = {}
            for name, index in self.header_map.items():
                entry[name] = _resolve_part(row, index)
            result.append(entry)

        return result

def _resolve_part(row: TSVRow, index: typing.Union[int, None]) -> str:
    """ Return the part at index, or empty string if absent or out of range. """

    if (index is None):
        return ''

    if (index < len(row.parts)):
        return row.parts[index]

    return ''

def parse_tsv_rows(path: str) -> typing.List[TSVRow]:
    """ Parse a TSV file into raw rows, skipping blanks. Parts are stripped. """

    content = edq.util.dirent.read_file(path)
    rows = []
    effective_lineno = 0

    for lineno, line in enumerate(content.splitlines(), start = 1):
        if (line.strip() == ''):
            continue

        effective_lineno += 1
        parts = [part.strip() for part in line.split('\t')]

        rows.append(TSVRow(
            parts = parts,
            lineno = lineno,
            effective_lineno = effective_lineno
        ))

    return rows

def load_tsv_table(
        path: str,
        expected_columns: typing.List[str],
        required_columns: typing.Union[typing.List[str], None] = None,
        skip_rows: int = 0,
        interpret_headers: bool = True,
        ) -> TSVFile:
    """ Interpret a TSV file's rows into a TSVFile with column mapping. """

    if (len(expected_columns) == 0):
        raise ValueError("expected_columns must not be empty.")

    if (skip_rows < 0):
        raise ValueError("skip_rows must be non-negative.")

    if (required_columns is not None):
        expected_lower = {col.lower() for col in expected_columns}
        unknown = []
        for c in required_columns:
            if (c.lower() not in expected_lower):
                unknown.append(c)

        if (len(unknown) > 0):
            raise ValueError(
                f"required_columns contains names not in expected_columns:"
                f" {sorted(unknown)}"
            )

    raw_rows = parse_tsv_rows(path)
    data_rows = raw_rows[skip_rows:]

    default_map: typing.Dict[str, typing.Union[int, None]] = {}
    for i, name in enumerate(expected_columns):
        default_map[name] = i

    if (len(data_rows) == 0):
        return TSVFile(headers = None, rows = [], header_map = default_map)

    if (interpret_headers):
        header_map = _match_header_row(
            data_rows[0].parts,
            expected_columns,
            required_columns or expected_columns,
        )

        if (header_map is not None):
            header_parts = data_rows[0].parts
            data_rows = data_rows[1:]

            return TSVFile(
                headers = header_parts,
                rows = data_rows,
                header_map = header_map
            )

    return TSVFile(headers = None, rows = data_rows, header_map = default_map)

def _match_header_row(
        parts: typing.List[str],
        expected_columns: typing.List[str],
        required_columns: typing.List[str],
        ) -> typing.Union[typing.Dict[str, typing.Union[int, None]], None]:
    """ Return a column index map if all required columns match, else None. """

    normalized_expected = {col.lower(): col for col in expected_columns}
    normalized_required = {col.lower() for col in required_columns}

    header_map: typing.Dict[str, typing.Union[int, None]] = {}
    found = set()

    for col in expected_columns:
        header_map[col] = None

    for i, part in enumerate(parts):
        normalized = part.lower()

        if (normalized in normalized_expected):
            header_map[normalized_expected[normalized]] = i
            found.add(normalized)

    if (normalized_required.issubset(found)):
        return header_map

    return None
