import edq.testing.unittest

import lms.model.base
import lms.model.users

class TestBaseType(edq.testing.unittest.BaseTest):
    """ Test functonality of types derived from the base type. """

    def test_as_json_dict_base(self):
        """ Test converting to a JSON dict. """

        # [(input, kwargs, expected), ...]
        test_cases = [
            # Base
            (
                lms.model.users.ServerUser(id = '123', name = 'Alice', extra = 'abc'),
                {},
                {
                    'email': None,
                    'id': '123',
                    'name': 'Alice',
                },
            ),

            # Extra Fields
            (
                lms.model.users.ServerUser(id = '123', name = 'Alice', extra = 'abc'),
                {
                    'include_extra_fields': True,
                },
                {
                    'email': None,
                    'id': '123',
                    'name': 'Alice',
                    'extra': 'abc',
                },
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (value, kwargs, expected) = test_case

            with self.subTest(msg = f"Case {i} ('{value}'):"):
                actual = value.as_json_dict(**kwargs)
                self.assertJSONDictEqual(expected, actual)

    def test_as_text_rows_base(self):
        """ Test converting to text rows. """

        # [(input, kwargs, expected), ...]
        test_cases = [
            # Base
            (
                lms.model.users.ServerUser(id = '123', name = 'Alice', extra = 'abc'),
                {},
                [
                    'id: 123',
                    'name: Alice',
                    'email: ',
                ],
            ),

            # Extra Fields
            (
                lms.model.users.ServerUser(id = '123', name = 'Alice', extra = 'abc'),
                {
                    'include_extra_fields': True,
                },
                [
                    'id: 123',
                    'name: Alice',
                    'email: ',
                    'extra: abc',
                ],
            ),

            # Skip Headers
            (
                lms.model.users.ServerUser(id = '123', name = 'Alice', extra = 'abc'),
                {
                    'skip_headers': True,
                },
                [
                    '123',
                    'Alice',
                    '',
                ],
            ),

            # Pretty Headers
            (
                lms.model.users.ServerUser(id = '123', name = 'Alice', extra = 'abc'),
                {
                    'pretty_headers': True,
                },
                [
                    'Id: 123',
                    'Name: Alice',
                    'Email: ',
                ],
            ),

            # Skip Pretty Headers
            (
                lms.model.users.ServerUser(id = '123', name = 'Alice', extra = 'abc'),
                {
                    'skip_headers': True,
                    'pretty_headers': True,
                },
                [
                    '123',
                    'Alice',
                    '',
                ],
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (value, kwargs, expected) = test_case

            with self.subTest(msg = f"Case {i} ('{value}'):"):
                actual = value.as_text_rows(**kwargs)
                self.assertJSONListEqual(expected, actual)

    def test_as_table_rows_base(self):
        """ Test converting to table rows. """

        # [(input, kwargs, expected), ...]
        test_cases = [
            # Base
            (
                lms.model.users.ServerUser(id = '123', name = 'Alice', extra = 'abc'),
                {},
                [[
                    '123',
                    'Alice',
                    '',
                ]],
            ),

            # Extra Fields
            (
                lms.model.users.ServerUser(id = '123', name = 'Alice', extra = 'abc'),
                {
                    'include_extra_fields': True,
                },
                [[
                    '123',
                    'Alice',
                    '',
                    'abc',
                ]],
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (value, kwargs, expected) = test_case

            with self.subTest(msg = f"Case {i} ('{value}'):"):
                actual = value.as_table_rows(**kwargs)
                self.assertJSONEqual(expected, actual)
