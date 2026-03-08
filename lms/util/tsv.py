"""
Utilities for parsing TSV files.
"""

import typing
from dataclasses import dataclass, field

import edq.util.dirent


@dataclass
class TsvRow:

    parts: typing.List[str]
    lineno: int


@dataclass
class TsvFile:

    headers: typing.Optional[typing.List[str]]
    rows: typing.List[TsvRow] = field(default_factory = list)
    header_map: typing.Dict[str, typing.Optional[int]] = field(default_factory = dict)

    def to_dicts(self) -> typing.List[typing.Dict[str, str]]:
        """ Convert the TSV entries to dicts. """

        if (not self.header_map):
            return []

        resolved = {
            name: self.header_map.get(name)
            for name in self.header_map
        }
        return [
            {
                name: (row.parts[index] if (index is not None and index < len(row.parts)) else '')
                for name, index in resolved.items()
            }
            for row in self.rows
        ]


def parse_tsv(path: str) -> typing.List[TsvRow]:
    """ Parse the TSV entries from the file. """

    rows = []
    with open(path, 'r', encoding = edq.util.dirent.DEFAULT_ENCODING) as file:
        for lineno, line in enumerate(file, start=1):
            line = line.rstrip('\r\n')
            if (line.strip() == ''):
                continue
            parts = [part.strip() for part in line.split('\t')]
            rows.append(TsvRow(parts = parts, lineno = lineno))
    return rows


def read_tsv(
        path: str,
        expected_columns: typing.List[str],
        skip_rows: int = 0,
        ) -> TsvFile:
    """ Read the TSV file. """

    raw_rows = parse_tsv(path)
    data_rows = raw_rows[skip_rows:]

    default_map: typing.Dict[str, typing.Optional[int]] = {
        name: i for i, name in enumerate(expected_columns)
    }

    if (not data_rows):
        return TsvFile(headers = None, rows = [], header_map = default_map)

    header_parts: typing.Optional[typing.List[str]] = None
    header_map = _parse_header(data_rows[0].parts, expected_columns)

    if (header_map is not None):
        header_parts = data_rows[0].parts
        data_rows = data_rows[1:]
        return TsvFile(headers = header_parts, rows = data_rows, header_map = header_map)

    return TsvFile(headers = None, rows = data_rows, header_map = default_map)


def _parse_header(
        parts: typing.List[str],
        expected_columns: typing.List[str],
        ) -> typing.Optional[typing.Dict[str, typing.Optional[int]]]:
    """ Parse the TSV header. """

    normalized_expected = {col.lower(): col for col in expected_columns}
    header_map: typing.Dict[str, typing.Optional[int]] = {col: None for col in expected_columns}
    found_any = False
    for i, part in enumerate(part.lower() for part in parts):
        if (part in normalized_expected):
            header_map[normalized_expected[part]] = i
            found_any = True
    return header_map if (found_any) else None