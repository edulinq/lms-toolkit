import os
import tempfile

import edq.testing.unittest

import lms.cli.table

class TestReadTable(edq.testing.unittest.BaseTest):
    """ Tests for the read_table utility. """

    def _write_temp_file(self, content):
        """ Write content to a temporary file and return the path. """

        temp = tempfile.NamedTemporaryFile(mode = 'w', suffix = '.txt', delete = False, encoding = 'utf-8')
        temp.write(content)
        temp.close()
        return temp.name

    def _get_values(self, rows):
        """ Extract just the values from (lineno, values) tuples. """

        return [values for (_, values) in rows]

    def _columns_with_optional(self):
        return [
            lms.cli.table.ColumnDef("user", required = True),
            lms.cli.table.ColumnDef("score", required = True),
            lms.cli.table.ColumnDef("comment", required = False),
        ]

    def _columns_required_only(self):
        return [
            lms.cli.table.ColumnDef("group", required = True),
            lms.cli.table.ColumnDef("user", required = True),
        ]

    # 1. No header — positional order.

    def test_no_header_positional(self):
        path = self._write_temp_file("alice\t1.0\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_with_optional(), has_header = False))
            self.assertEqual(1, len(rows))
            self.assertEqual(["alice", "1.0", None], rows[0])
        finally:
            os.unlink(path)

    def test_no_header_positional_all_columns(self):
        path = self._write_temp_file("alice\t1.0\tgreat\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_with_optional(), has_header = False))
            self.assertEqual(1, len(rows))
            self.assertEqual(["alice", "1.0", "great"], rows[0])
        finally:
            os.unlink(path)

    def test_no_header_skip_rows(self):
        path = self._write_temp_file("User\tScore\nalice\t1.0\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_with_optional(), skip_rows = 1, has_header = False))
            self.assertEqual(1, len(rows))
            self.assertEqual(["alice", "1.0", None], rows[0])
        finally:
            os.unlink(path)

    # 2. All columns, in order.

    def test_header_all_columns_in_order(self):
        path = self._write_temp_file("User\tScore\tComment\nalice\t1.0\tgreat\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_with_optional(), has_header = True))
            self.assertEqual(1, len(rows))
            self.assertEqual(["alice", "1.0", "great"], rows[0])
        finally:
            os.unlink(path)

    # 3. All columns, out of order.

    def test_header_all_columns_out_of_order(self):
        path = self._write_temp_file("Comment\tScore\tUser\ngreat\t1.0\talice\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_with_optional(), has_header = True))
            self.assertEqual(1, len(rows))
            # Result should be mapped to columns order: user, score, comment.
            self.assertEqual(["alice", "1.0", "great"], rows[0])
        finally:
            os.unlink(path)

    # 4. Missing optional columns, in order.

    def test_header_missing_optional_in_order(self):
        path = self._write_temp_file("User\tScore\nalice\t1.0\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_with_optional(), has_header = True))
            self.assertEqual(1, len(rows))
            self.assertEqual(["alice", "1.0", None], rows[0])
        finally:
            os.unlink(path)

    # 5. Missing optional columns, out of order.

    def test_header_missing_optional_out_of_order(self):
        path = self._write_temp_file("Score\tUser\n1.0\talice\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_with_optional(), has_header = True))
            self.assertEqual(1, len(rows))
            self.assertEqual(["alice", "1.0", None], rows[0])
        finally:
            os.unlink(path)

    # 6. Extra columns, in order.

    def test_header_extra_columns_in_order(self):
        path = self._write_temp_file("User\tScore\tComment\tExtra\nalice\t1.0\tgreat\tignored\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_with_optional(), has_header = True))
            self.assertEqual(1, len(rows))
            self.assertEqual(["alice", "1.0", "great"], rows[0])
        finally:
            os.unlink(path)

    # 7. Extra columns, out of order.

    def test_header_extra_columns_out_of_order(self):
        path = self._write_temp_file("Extra\tComment\tScore\tUser\nignored\tgreat\t1.0\talice\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_with_optional(), has_header = True))
            self.assertEqual(1, len(rows))
            self.assertEqual(["alice", "1.0", "great"], rows[0])
        finally:
            os.unlink(path)

    # Error cases.

    def test_header_missing_required_column(self):
        path = self._write_temp_file("Score\tComment\n1.0\tgreat\n")
        try:
            with self.assertRaises(ValueError):
                lms.cli.table.read_table(path, self._columns_with_optional(), has_header = True)
        finally:
            os.unlink(path)

    def test_no_header_too_few_columns(self):
        path = self._write_temp_file("alice\n")
        try:
            with self.assertRaises(ValueError):
                lms.cli.table.read_table(path, self._columns_with_optional(), has_header = False)
        finally:
            os.unlink(path)

    def test_no_header_too_many_columns(self):
        path = self._write_temp_file("alice\t1.0\tgreat\textra\n")
        try:
            with self.assertRaises(ValueError):
                lms.cli.table.read_table(path, self._columns_with_optional(), has_header = False)
        finally:
            os.unlink(path)

    def test_header_and_skip_rows_mutually_exclusive(self):
        path = self._write_temp_file("User\tScore\nalice\t1.0\n")
        try:
            with self.assertRaises(ValueError):
                lms.cli.table.read_table(path, self._columns_with_optional(), has_header = True, skip_rows = 1)
        finally:
            os.unlink(path)

    def test_header_duplicate_column(self):
        path = self._write_temp_file("User\tUser\nalice\tbob\n")
        try:
            with self.assertRaises(ValueError):
                lms.cli.table.read_table(path, self._columns_required_only(), has_header = True)
        finally:
            os.unlink(path)

    # Empty lines handling.

    def test_empty_lines_skipped(self):
        path = self._write_temp_file("\n\nUser\tScore\n\nalice\t1.0\n\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_with_optional(), has_header = True))
            self.assertEqual(1, len(rows))
            self.assertEqual(["alice", "1.0", None], rows[0])
        finally:
            os.unlink(path)

    # Multiple rows.

    def test_multiple_rows_reordered(self):
        path = self._write_temp_file("User\tGroup\nalice\tGroupA\nbob\tGroupB\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_required_only(), has_header = True))
            self.assertEqual(2, len(rows))
            # Mapped to columns order: group, user.
            self.assertEqual(["GroupA", "alice"], rows[0])
            self.assertEqual(["GroupB", "bob"], rows[1])
        finally:
            os.unlink(path)

    # Case insensitivity.

    def test_header_case_insensitive(self):
        path = self._write_temp_file("USER\tSCORE\tCOMMENT\nalice\t1.0\tgreat\n")
        try:
            rows = self._get_values(lms.cli.table.read_table(path, self._columns_with_optional(), has_header = True))
            self.assertEqual(1, len(rows))
            self.assertEqual(["alice", "1.0", "great"], rows[0])
        finally:
            os.unlink(path)
