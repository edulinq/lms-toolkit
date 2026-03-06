"""
Utilities for parsing TSV files.
"""
import typing
import edq.util.dirent

def read_tsv(path: str,
        expected_columns: typing.List[str],
        skip_rows: int = 0,
        ) -> typing.Iterator[typing.Dict[str, typing.Any]]:
    """ Read a TSV file and return its rows with parsed columns and metadata. """

    with open(path, 'r', encoding = edq.util.dirent.DEFAULT_ENCODING) as file:
        lineno = 0
        real_rows = 0
        header_map: typing.Optional[typing.Dict[str, int]] = None
        found_header = False

        for line in file:
            lineno += 1
            line = line.rstrip('\r\n')

            if (line.strip() == ''):
                continue

            real_rows += 1
            if (real_rows <= skip_rows):
                continue

            parts = [part.strip() for part in line.split("\t")]

            if (header_map is None):
                potential_header_map = _parse_header(parts, expected_columns)
                if (potential_header_map is not None):
                    header_map = potential_header_map
                    found_header = True
                    continue

                header_map = {name: i for (i, name) in enumerate(expected_columns)}

            row = {
                '__lineno__': lineno,
                '__has_header__': found_header,
                '__parts__': parts,
            }

            for name in expected_columns:
                index = header_map.get(name)
                if ((index is not None) and (index < len(parts))):
                    value = parts[index]
                else:
                    value = ''

                row[name] = value

            yield row

def _parse_header(parts: typing.List[str], expected_columns: typing.List[str]) -> typing.Optional[typing.Dict[str, int]]:
    """ Check if the given parts represent a header for the expected columns. """

    normalized_expected = [col.lower() for col in expected_columns]
    normalized_parts = [part.lower() for part in parts]
    found_any = False
    header_map = {}

    for i, part in enumerate(normalized_parts):
        if (part in normalized_expected):
            found_any = True
            header_map[expected_columns[normalized_expected.index(part)]] = i

    if (found_any):
        return header_map

    return None
