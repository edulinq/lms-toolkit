"""
Tests for lms.cli.table (read_table with automatic header detection).
"""

import os
import tempfile
import unittest
import lms.cli.table

class TestReadTable(unittest.TestCase):
    """ Test read_table with various header configurations. """

    def _write_tsv(self, lines: list) -> str:
        """ Write lines to a temporary TSV file and return the path. """

        fd, path = tempfile.mkstemp(suffix = '.tsv')
        with os.fdopen(fd, 'w', encoding = 'utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        self.addCleanup(os.unlink, path)

        return path

    # No Header (Positional)

    def test_no_header(self):
        """ No header row — columns mapped by position. """

        path = self._write_tsv([
            'alice\t95\tGreat',
            'bob\t80',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'], optional_columns = ['comment'])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], {'user': 'alice', 'score': '95', 'comment': 'Great'})
        self.assertEqual(rows[1][1], {'user': 'bob', 'score': '80'})

    # Header — All Columns, In Order

    def test_header_all_columns_in_order(self):
        """ Header with all columns in expected order. """

        path = self._write_tsv([
            'user\tscore\tcomment',
            'alice\t95\tGreat',
            'bob\t80\tOK',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'], optional_columns = ['comment'])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], {'user': 'alice', 'score': '95', 'comment': 'Great'})
        self.assertEqual(rows[1][1], {'user': 'bob', 'score': '80', 'comment': 'OK'})

    # Header — All Columns, Out of Order

    def test_header_all_columns_out_of_order(self):
        """ Header with all columns reordered. """

        path = self._write_tsv([
            'comment\tscore\tuser',
            'Great\t95\talice',
            'OK\t80\tbob',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'], optional_columns = ['comment'])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], {'user': 'alice', 'score': '95', 'comment': 'Great'})
        self.assertEqual(rows[1][1], {'user': 'bob', 'score': '80', 'comment': 'OK'})

    # Header — Missing Optional Columns, In Order

    def test_header_missing_optional_in_order(self):
        """ Header with only required columns (optional missing). """

        path = self._write_tsv([
            'user\tscore',
            'alice\t95',
            'bob\t80',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'], optional_columns = ['comment'])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], {'user': 'alice', 'score': '95'})
        self.assertNotIn('comment', rows[0][1])

    # Header — Missing Optional Columns, Out of Order

    def test_header_missing_optional_out_of_order(self):
        """ Header with required columns reordered, optional missing. """

        path = self._write_tsv([
            'score\tuser',
            '95\talice',
            '80\tbob',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'], optional_columns = ['comment'])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], {'user': 'alice', 'score': '95'})
        self.assertEqual(rows[1][1], {'user': 'bob', 'score': '80'})

    # Header — Extra Columns, In Order

    def test_header_extra_columns_in_order(self):
        """ Header with extra unrecognized columns (silently ignored). """

        path = self._write_tsv([
            'user\tscore\tcomment\tnotes',
            'alice\t95\tGreat\tsome notes',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'], optional_columns = ['comment'])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], {'user': 'alice', 'score': '95', 'comment': 'Great'})
        self.assertNotIn('notes', rows[0][1])

    # Header — Extra Columns, Out of Order

    def test_header_extra_columns_out_of_order(self):
        """ Header with extra columns and reordered. """

        path = self._write_tsv([
            'notes\tcomment\tscore\tuser',
            'some notes\tGreat\t95\talice',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'], optional_columns = ['comment'])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], {'user': 'alice', 'score': '95', 'comment': 'Great'})

    # Skip Rows

    def test_skip_rows(self):
        """ Rows are skipped before header detection. """

        path = self._write_tsv([
            'title row to skip',
            'alice\t95',
            'bob\t80',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'], skip_rows = 1)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], {'user': 'alice', 'score': '95'})

    # Blank Lines

    def test_blank_lines_ignored(self):
        """ Blank lines in the file are ignored. """

        path = self._write_tsv([
            'alice\t95',
            '',
            'bob\t80',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'])
        self.assertEqual(len(rows), 2)

    # Wrong Column Count

    def test_wrong_column_count_raises(self):
        """ Too few or too many columns in positional mode raises ValueError. """

        path = self._write_tsv([
            'alice',
        ])

        with self.assertRaises(ValueError):
            lms.cli.table.read_table(path, ['user', 'score'])

    # Two Required Columns (Memberships)

    def test_memberships_no_header(self):
        """ Two-column table without header (group memberships style). """

        path = self._write_tsv([
            'group-a\talice',
            'group-b\tbob',
        ])

        rows = lms.cli.table.read_table(path, ['group', 'user'])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], {'group': 'group-a', 'user': 'alice'})

    def test_memberships_with_header(self):
        """ Two-column table with header. """

        path = self._write_tsv([
            'group\tuser',
            'group-a\talice',
            'group-b\tbob',
        ])

        rows = lms.cli.table.read_table(path, ['group', 'user'])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], {'group': 'group-a', 'user': 'alice'})

    # Line Numbers

    def test_line_numbers_without_header(self):
        """ Line numbers are correct in positional mode. """

        path = self._write_tsv([
            'alice\t95',
            '',
            'bob\t80',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'])
        self.assertEqual(rows[0][0], 1)
        self.assertEqual(rows[1][0], 3)

    def test_line_numbers_with_header(self):
        """ Line numbers are correct when a header is present. """

        path = self._write_tsv([
            'user\tscore',
            'alice\t95',
            '',
            'bob\t80',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'])
        self.assertEqual(rows[0][0], 2)
        self.assertEqual(rows[1][0], 4)

    # Case-Insensitive Header

    def test_header_case_insensitive(self):
        """ Header detection is case-insensitive. """

        path = self._write_tsv([
            'User\tScore\tComment',
            'alice\t95\tGreat',
        ])

        rows = lms.cli.table.read_table(path, ['user', 'score'], optional_columns = ['comment'])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], {'user': 'alice', 'score': '95', 'comment': 'Great'})


if (__name__ == '__main__'):
    unittest.main()
