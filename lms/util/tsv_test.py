import os
import tempfile

import edq.testing.unittest

import lms.util.tsv

class TestTsv(edq.testing.unittest.BaseTest):
    """
    Test TSV parsing.
    """

    def test_read_tsv_with_header(self):
        """
        Test reading a TSV with a header.
        """

        content = "group\tuser\nGroup A\tUser 1\nGroup B\tUser 2\n"
        expected = [
            {'group': 'Group A', 'user': 'User 1'},
            {'group': 'Group B', 'user': 'User 2'},
        ]

        with tempfile.NamedTemporaryFile(mode = 'w', delete = False) as temp:
            temp.write(content)
            temp_path = temp.name

        try:
            tsv = lms.util.tsv.read_tsv(temp_path, ['group', 'user'])
            actual = tsv.to_dicts()
            self.assertEqual(expected, actual)
            self.assertEqual(['group', 'user'], tsv.headers)
        finally:
            if (os.path.exists(temp_path)):
                os.remove(temp_path)

    def test_read_tsv_without_header(self):
        """
        Test reading a TSV without a header (positional mapping).
        """

        content = "Group A\tUser 1\nGroup B\tUser 2\n"
        expected = [
            {'group': 'Group A', 'user': 'User 1'},
            {'group': 'Group B', 'user': 'User 2'},
        ]

        with tempfile.NamedTemporaryFile(mode = 'w', delete = False) as temp:
            temp.write(content)
            temp_path = temp.name

        try:
            tsv = lms.util.tsv.read_tsv(temp_path, ['group', 'user'])
            actual = tsv.to_dicts()
            self.assertEqual(expected, actual)
            self.assertIsNone(tsv.headers)
            
            self.assertEqual({'group': 0, 'user': 1}, tsv.header_map)
        finally:
            if (os.path.exists(temp_path)):
                os.remove(temp_path)

    def test_read_tsv_out_of_order(self):
        """
        Test that out-of-order columns in the TSV (with headers) are handled correctly.
        """

        content = "user\tgroup\nUser 1\tGroup A\nUser 2\tGroup B\n"
        expected = [
            {'group': 'Group A', 'user': 'User 1'},
            {'group': 'Group B', 'user': 'User 2'},
        ]

        with tempfile.NamedTemporaryFile(mode = 'w', delete = False) as temp:
            temp.write(content)
            temp_path = temp.name

        try:
            tsv = lms.util.tsv.read_tsv(temp_path, ['group', 'user'])
            actual = tsv.to_dicts()
            self.assertEqual(expected, actual)
            self.assertEqual(['user', 'group'], tsv.headers)
        finally:
            if (os.path.exists(temp_path)):
                os.remove(temp_path)

    def test_read_tsv_extra_columns(self):
        """
        Test that extra columns in the TSV (with headers) are ignored.
        """

        content = "group\textra\tuser\nGroup A\tfoo\tUser 1\nGroup B\tbar\tUser 2\n"
        expected = [
            {'group': 'Group A', 'user': 'User 1'},
            {'group': 'Group B', 'user': 'User 2'},
        ]

        with tempfile.NamedTemporaryFile(mode = 'w', delete = False) as temp:
            temp.write(content)
            temp_path = temp.name

        try:
            tsv = lms.util.tsv.read_tsv(temp_path, ['group', 'user'])
            actual = tsv.to_dicts()
            self.assertEqual(expected, actual)
            self.assertEqual(['group', 'extra', 'user'], tsv.headers)
        finally:
            if (os.path.exists(temp_path)):
                os.remove(temp_path)

    def test_read_tsv_missing_columns_in_file(self):
        """
        Test that missing columns in the TSV (with headers) default to an empty string.
        """

        content = "user\nUser 1\nUser 2\n"
        expected = [
            {'group': '', 'user': 'User 1'},
            {'group': '', 'user': 'User 2'},
        ]

        with tempfile.NamedTemporaryFile(mode = 'w', delete = False) as temp:
            temp.write(content)
            temp_path = temp.name

        try:
            tsv = lms.util.tsv.read_tsv(temp_path, ['group', 'user'])
            actual = tsv.to_dicts()
            self.assertEqual(expected, actual)
        finally:
            if (os.path.exists(temp_path)):
                os.remove(temp_path)

    def test_read_tsv_case_insensitive(self):
        """
        Test that header matching is case-insensitive.
        """

        content = "GROUP\tUSER\nGroup A\tUser 1\n"
        expected = [
            {'group': 'Group A', 'user': 'User 1'},
        ]

        with tempfile.NamedTemporaryFile(mode = 'w', delete = False) as temp:
            temp.write(content)
            temp_path = temp.name

        try:
            tsv = lms.util.tsv.read_tsv(temp_path, ['group', 'user'])
            actual = tsv.to_dicts()
            self.assertEqual(expected, actual)
            self.assertEqual(['GROUP', 'USER'], tsv.headers)
        finally:
            if (os.path.exists(temp_path)):
                os.remove(temp_path)

    def test_read_tsv_skip_rows(self):
        """
        Test skipping rows.
        """

        content = "Garbage\nMore Garbage\ngroup\tuser\nGroup A\tUser 1\n"
        expected = [
            {'group': 'Group A', 'user': 'User 1'},
        ]

        with tempfile.NamedTemporaryFile(mode = 'w', delete = False) as temp:
            temp.write(content)
            temp_path = temp.name

        try:
            tsv = lms.util.tsv.read_tsv(temp_path, ['group', 'user'], skip_rows = 2)
            actual = tsv.to_dicts()
            self.assertEqual(expected, actual)
        finally:
            if (os.path.exists(temp_path)):
                os.remove(temp_path)

    def test_read_tsv_blank_lines(self):
        """
        Test that blank lines are skipped.
        """

        content = "group\tuser\n\nGroup A\tUser 1\n\nGroup B\tUser 2\n"
        expected = [
            {'group': 'Group A', 'user': 'User 1'},
            {'group': 'Group B', 'user': 'User 2'},
        ]

        with tempfile.NamedTemporaryFile(mode = 'w', delete = False) as temp:
            temp.write(content)
            temp_path = temp.name

        try:
            tsv = lms.util.tsv.read_tsv(temp_path, ['group', 'user'])
            actual = tsv.to_dicts()
            self.assertEqual(expected, actual)
        finally:
            if (os.path.exists(temp_path)):
                os.remove(temp_path)

    def test_read_tsv_partial_row(self):
        """
        Test rows with fewer columns than expected.
        """

        content = "group\tuser\tcomment\nGroup A\tUser 1\n"
        expected = [
            {'group': 'Group A', 'user': 'User 1', 'comment': ''},
        ]

        with tempfile.NamedTemporaryFile(mode = 'w', delete = False) as temp:
            temp.write(content)
            temp_path = temp.name

        try:
            tsv = lms.util.tsv.read_tsv(temp_path, ['group', 'user', 'comment'])
            actual = tsv.to_dicts()
            self.assertEqual(expected, actual)
        finally:
            if (os.path.exists(temp_path)):
                os.remove(temp_path)
