import edq.testing.unittest

import lms.model.base
import lms.model.courses
import lms.model.users
import lms.model.assignments

class TestBaseType(edq.testing.unittest.BaseTest):
    """ Test functonality of types derived from the base type. """

    # JSON Dict

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
            (
                lms.model.assignments.Assignment(id = '123', name = 'Assignment 1', extra = 'abc'),
                {},
                {
                    'id': '123',
                    'name': 'Assignment 1',
                    'close_date': None,
                    'description': None,
                    'due_date': None,
                    'open_date': None,
                    'points_possible': None,
                },
            ),
            (
                lms.model.courses.Course(id = '123', name = 'Course 1', extra = 'abc'),
                {},
                {
                    'id': '123',
                    'name': 'Course 1',
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

    def test_from_json_dict_base(self):
        """ Test converting from a JSON dict. """

        # [(input, kwargs, expected), ...]
        test_cases = [
            # Base - User
            (
                {
                    'email': None,
                    'id': '123',
                    'name': 'Alice',
                },
                {},
                lms.model.users.ServerUser(id = '123', name = 'Alice'),
            ),
            (
                {
                    'id': '123',
                    'name': 'Assignment 1',
                },
                {},
                lms.model.assignments.Assignment(id = '123', name = 'Assignment 1'),
            ),
            (
                {
                    'id': '123',
                    'name': 'Course 1',
                },
                {},
                lms.model.courses.Course(id = '123', name = 'Course 1'),
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (value, kwargs, expected) = test_case

            with self.subTest(msg = f"Case {i} ('{value}'):"):
                actual = type(expected).from_json_dict(value, **kwargs)
                self.assertJSONEqual(expected, actual)

    def test_json_dict_cyclic_serialization(self):
        """ Test converting to a JSON dict and back to an object. """

        # [(input, kwargs), ...]
        test_cases = [
            # Base
            (
                lms.model.users.ServerUser(id = '123', name = 'Alice', extra = 'abc'),
                {},
            ),
            (
                lms.model.assignments.Assignment(id = '123', name = 'Assignment 1', extra = 'abc'),
                {},
            ),
            (
                lms.model.courses.Course(id = '123', name = 'Course 1', extra = 'abc'),
                {},
            ),

            # Extra Fields
            (
                lms.model.users.ServerUser(id = '123', name = 'Alice', extra = 'abc'),
                {
                    'include_extra_fields': True,
                },
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (value, kwargs) = test_case

            with self.subTest(msg = f"Case {i} ('{value}'):"):
                json_dict = value.as_json_dict(**kwargs)
                new_value = type(value).from_json_dict(json_dict, **kwargs)
                self.assertJSONEqual(value, new_value)

    # Text Rows

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
            (
                lms.model.assignments.Assignment(id = '123', name = 'Assignment 1', extra = 'abc'),
                {},
                [
                    'id: 123',
                    'name: Assignment 1',
                    'description: ',
                    'open_date: ',
                    'close_date: ',
                    'due_date: ',
                    'points_possible: ',
                ],
            ),
            (
                lms.model.courses.Course(id = '123', name = 'Course 1', extra = 'abc'),
                {},
                [
                    'id: 123',
                    'name: Course 1',
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

    # Table Rows

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
            (
                lms.model.assignments.Assignment(id = '123', name = 'Assignment 1', extra = 'abc'),
                {},
                [[
                    '123',
                    'Assignment 1',
                    '',
                    '',
                    '',
                    '',
                    '',
                ]],
            ),
            (
                lms.model.courses.Course(id = '123', name = 'Course 1', extra = 'abc'),
                {},
                [[
                    '123',
                    'Course 1',
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
