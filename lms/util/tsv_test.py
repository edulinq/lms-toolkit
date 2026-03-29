import edq.testing.unittest
import edq.util.dirent

import lms.util.tsv

def _write_temp(content: str) -> str:
    """ Write content to a temp file and return its path. """

    path = edq.util.dirent.get_temp_path(suffix = '.tsv')
    with open(path, 'w', encoding = edq.util.dirent.DEFAULT_ENCODING) as f:
        f.write(content)

    return path

def _remove_temp(path: str) -> None:
    """ Remove a temp file if it exists. """

    edq.util.dirent.remove(path)

class TestParseTsvRows(edq.testing.unittest.BaseTest):
    """ Tests for parse_tsv_rows — raw row parsing with no header logic. """

    def test_returns_all_non_blank_rows(self):
        """ Blank lines are skipped and remaining rows are returned. """

        path = _write_temp("foo\tbar\n\nbaz\tqux\n")
        try:
            rows = lms.util.tsv.parse_tsv_rows(path)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0].parts, ['foo', 'bar'])
            self.assertEqual(rows[1].parts, ['baz', 'qux'])
        finally:
            _remove_temp(path)

    def test_only_blank_lines_returns_no_rows(self):
        """ A file containing only blank lines produces an empty list. """

        path = _write_temp("\n\n\n")
        try:
            rows = lms.util.tsv.parse_tsv_rows(path)
            self.assertEqual(rows, [])
        finally:
            _remove_temp(path)

    def test_empty_file_returns_no_rows(self):
        """ An empty file produces an empty list. """

        path = _write_temp('')
        try:
            rows = lms.util.tsv.parse_tsv_rows(path)
            self.assertEqual(rows, [])
        finally:
            _remove_temp(path)

    def test_tracks_real_and_effective_line_numbers(self):
        """ lineno counts blank lines; effective_lineno does not. """

        path = _write_temp("foo\tbar\n\nbaz\tqux\n")
        try:
            rows = lms.util.tsv.parse_tsv_rows(path)
            self.assertEqual(rows[0].lineno, 1)
            self.assertEqual(rows[0].effective_lineno, 1)
            self.assertEqual(rows[1].lineno, 3)
            self.assertEqual(rows[1].effective_lineno, 2)
        finally:
            _remove_temp(path)

    def test_raise_error_includes_line_context(self):
        """ raise_error includes both line numbers and the caller's message. """

        path = _write_temp("foo\tbar\n")
        try:
            rows = lms.util.tsv.parse_tsv_rows(path)
            with self.assertRaises(ValueError) as ctx:
                rows[0].raise_error("something went wrong")
            self.assertIn("Line 1", str(ctx.exception))
            self.assertIn("effective 1", str(ctx.exception))
            self.assertIn("something went wrong", str(ctx.exception))
        finally:
            _remove_temp(path)

class TestLoadTsvTable(edq.testing.unittest.BaseTest):
    """ Tests for load_tsv_table — header detection, column mapping. """

    def test_with_header(self):
        """ Header row is detected and removed from data rows. """

        path = _write_temp("group\tuser\nGroup A\tUser 1\nGroup B\tUser 2\n")
        try:
            tsv = lms.util.tsv.load_tsv_table(path, ['group', 'user'])
            self.assertEqual(tsv.headers, ['group', 'user'])
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'Group A', 'user': 'User 1'},
                {'group': 'Group B', 'user': 'User 2'},
            ])
        finally:
            _remove_temp(path)

    def test_without_header(self):
        """ Columns are mapped positionally when no header row is present. """

        path = _write_temp("Group A\tUser 1\nGroup B\tUser 2\n")
        try:
            tsv = lms.util.tsv.load_tsv_table(path, ['group', 'user'])
            self.assertIsNone(tsv.headers)
            self.assertEqual(tsv.header_map, {'group': 0, 'user': 1})
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'Group A', 'user': 'User 1'},
                {'group': 'Group B', 'user': 'User 2'},
            ])
        finally:
            _remove_temp(path)

    def test_out_of_order_columns(self):
        """ Columns in the file in a different order are mapped correctly. """

        path = _write_temp("user\tgroup\nUser 1\tGroup A\nUser 2\tGroup B\n")
        try:
            tsv = lms.util.tsv.load_tsv_table(path, ['group', 'user'])
            self.assertEqual(tsv.headers, ['user', 'group'])
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'Group A', 'user': 'User 1'},
                {'group': 'Group B', 'user': 'User 2'},
            ])
        finally:
            _remove_temp(path)

    def test_extra_columns_are_ignored(self):
        """ Columns not in expected_columns are silently ignored. """

        content = (
            "group\textra\tuser\n"
            "Group A\tfoo\tUser 1\n"
            "Group B\tbar\tUser 2\n"
        )
        path = _write_temp(content)
        try:
            tsv = lms.util.tsv.load_tsv_table(path, ['group', 'user'])
            self.assertEqual(tsv.headers, ['group', 'extra', 'user'])
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'Group A', 'user': 'User 1'},
                {'group': 'Group B', 'user': 'User 2'},
            ])
        finally:
            _remove_temp(path)

    def test_missing_column_defaults_to_empty_string(self):
        """ A column in expected_columns absent from the file gives ''. """

        path = _write_temp("user\nUser 1\nUser 2\n")
        try:
            tsv = lms.util.tsv.load_tsv_table(
                path, ['group', 'user'], required_columns = ['user'],
            )
            self.assertEqual(tsv.to_dicts(), [
                {'group': '', 'user': 'User 1'},
                {'group': '', 'user': 'User 2'},
            ])
        finally:
            _remove_temp(path)

    def test_header_present_but_no_expected_columns_match(self):
        """ First row matches no expected columns; treated as data row. """

        path = _write_temp("foo\tbar\nGroup A\tUser 1\n")
        try:
            tsv = lms.util.tsv.load_tsv_table(path, ['group', 'user'])
            self.assertIsNone(tsv.headers)
            self.assertEqual(len(tsv.rows), 2)
        finally:
            _remove_temp(path)

    def test_header_matching_is_case_insensitive(self):
        """ Header names match regardless of case. """

        path = _write_temp("GROUP\tUSER\nGroup A\tUser 1\n")
        try:
            tsv = lms.util.tsv.load_tsv_table(path, ['group', 'user'])
            self.assertEqual(tsv.headers, ['GROUP', 'USER'])
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'Group A', 'user': 'User 1'},
            ])
        finally:
            _remove_temp(path)

    def test_skip_rows(self):
        """ Leading rows are discarded before any header or data processing. """

        content = "Garbage\nMore Garbage\ngroup\tuser\nGroup A\tUser 1\n"
        path = _write_temp(content)
        try:
            tsv = lms.util.tsv.load_tsv_table(
                path, ['group', 'user'], skip_rows = 2,
            )
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'Group A', 'user': 'User 1'},
            ])
        finally:
            _remove_temp(path)

    def test_blank_lines_are_skipped(self):
        """ Blank lines between data rows are ignored. """

        content = "group\tuser\n\nGroup A\tUser 1\n\nGroup B\tUser 2\n"
        path = _write_temp(content)
        try:
            tsv = lms.util.tsv.load_tsv_table(path, ['group', 'user'])
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'Group A', 'user': 'User 1'},
                {'group': 'Group B', 'user': 'User 2'},
            ])
        finally:
            _remove_temp(path)

    def test_partial_row_fills_missing_columns_with_empty_string(self):
        """ A row shorter than the header gives '' for missing columns. """

        path = _write_temp("group\tuser\tcomment\nGroup A\tUser 1\n")
        try:
            tsv = lms.util.tsv.load_tsv_table(
                path, ['group', 'user', 'comment'],
            )
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'Group A', 'user': 'User 1', 'comment': ''},
            ])
        finally:
            _remove_temp(path)

    def test_interpret_headers_false_skips_header_detection(self):
        """ With interpret_headers=False columns are always positional. """

        path = _write_temp("group\tuser\nGroup A\tUser 1\n")
        try:
            tsv = lms.util.tsv.load_tsv_table(
                path, ['group', 'user'], interpret_headers = False,
            )
            self.assertIsNone(tsv.headers)
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'group', 'user': 'user'},
                {'group': 'Group A', 'user': 'User 1'},
            ])
        finally:
            _remove_temp(path)

    def test_empty_file_returns_empty_tsv(self):
        """ An empty file produces a TSVFile with no rows. """

        path = _write_temp('')
        try:
            tsv = lms.util.tsv.load_tsv_table(path, ['group', 'user'])
            self.assertIsNone(tsv.headers)
            self.assertEqual(tsv.rows, [])
        finally:
            _remove_temp(path)

    def test_empty_expected_columns_raises(self):
        """ Passing an empty expected_columns raises ValueError. """

        path = _write_temp("group\tuser\n")
        try:
            with self.assertRaises(ValueError):
                lms.util.tsv.load_tsv_table(path, [])
        finally:
            _remove_temp(path)

    def test_required_columns_not_in_expected_raises(self):
        """ required_columns with names outside expected_columns raises. """

        path = _write_temp("group\tuser\n")
        try:
            with self.assertRaises(ValueError):
                lms.util.tsv.load_tsv_table(
                    path,
                    ['group', 'user'],
                    required_columns = ['group', 'user', 'comment'],
                )
        finally:
            _remove_temp(path)

    def test_required_columns_subset_detects_header(self):
        """ Header detected when all required columns match. """

        path = _write_temp("user\tscore\nUser 1\t95\n")
        try:
            tsv = lms.util.tsv.load_tsv_table(
                path,
                ['user', 'score', 'comment'],
                required_columns = ['user', 'score'],
            )
            self.assertEqual(tsv.headers, ['user', 'score'])
            self.assertEqual(tsv.to_dicts(), [
                {'user': 'User 1', 'score': '95', 'comment': ''},
            ])
        finally:
            _remove_temp(path)

    def test_missing_column_out_of_order(self):
        """ Missing column, remaining columns out of order, maps correctly. """

        path = _write_temp("user\tgroup\nUser 1\tGroup A\n")
        try:
            tsv = lms.util.tsv.load_tsv_table(
                path,
                ['group', 'user', 'comment'],
                required_columns = ['group', 'user'],
            )
            self.assertEqual(tsv.headers, ['user', 'group'])
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'Group A', 'user': 'User 1', 'comment': ''},
            ])
        finally:
            _remove_temp(path)

    def test_extra_columns_out_of_order(self):
        """ Extra and out-of-order columns in header are handled correctly. """

        content = (
            "user\textra\tgroup\n"
            "User 1\tfoo\tGroup A\n"
        )
        path = _write_temp(content)
        try:
            tsv = lms.util.tsv.load_tsv_table(path, ['group', 'user'])
            self.assertEqual(tsv.headers, ['user', 'extra', 'group'])
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'Group A', 'user': 'User 1'},
            ])
        finally:
            _remove_temp(path)

    def test_negative_skip_rows_raises(self):
        """ A negative skip_rows value raises ValueError. """

        path = _write_temp("group\tuser\n")
        try:
            with self.assertRaises(ValueError):
                lms.util.tsv.load_tsv_table(
                    path, ['group', 'user'], skip_rows = -1,
                )
        finally:
            _remove_temp(path)

    def test_required_columns_case_insensitive_validation(self):
        """ required_columns validation is case-insensitive. """

        path = _write_temp("GROUP\tUSER\nGroup A\tUser 1\n")
        try:
            tsv = lms.util.tsv.load_tsv_table(
                path,
                ['group', 'user'],
                required_columns = ['Group', 'User'],
            )
            self.assertEqual(tsv.headers, ['GROUP', 'USER'])
        finally:
            _remove_temp(path)

    def test_parts_are_stripped_of_whitespace(self):
        """ Leading and trailing whitespace in field values is stripped. """

        path = _write_temp("group\tuser\n  Group A  \t  User 1  \n")
        try:
            tsv = lms.util.tsv.load_tsv_table(path, ['group', 'user'])
            self.assertEqual(tsv.to_dicts(), [
                {'group': 'Group A', 'user': 'User 1'},
            ])
        finally:
            _remove_temp(path)
