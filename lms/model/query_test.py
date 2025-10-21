import edq.testing.unittest

import lms.model.query

class TestQuery(edq.testing.unittest.BaseTest):
    """ Test queries. """

    def test_parse_int_query_base(self):
        """ Test parsing an int-id query. """

        # [(text, check email, expected), ...]
        test_cases = [
            # None
            (
                None,
                True,
                None,
            ),

            # Empty
            (
                '',
                True,
                None,
            ),

            # Whitespace
            (
                '  ',
                True,
                None,
            ),

            # ID
            (
                '123',
                True,
                lms.model.query.BaseQuery(id = '123'),
            ),

            # Name
            (
                'name',
                True,
                lms.model.query.BaseQuery(name = 'name'),
            ),

            # Email
            (
                'email@test.edulinq.org',
                True,
                lms.model.query.BaseQuery(email = 'email@test.edulinq.org'),
            ),

            # Label - Name
            (
                'name (123)',
                True,
                lms.model.query.BaseQuery(id = '123', name = 'name'),
            ),

            # Label - Email
            (
                'email@test.edulinq.org (123)',
                True,
                lms.model.query.BaseQuery(id = '123', email = 'email@test.edulinq.org'),
            ),

            # Don't Check Email - ID
            (
                '123',
                False,
                lms.model.query.BaseQuery(id = '123'),
            ),

            # Don't Check Email - Name
            (
                'name',
                False,
                lms.model.query.BaseQuery(name = 'name'),
            ),

            # Don't Check Email - Email
            (
                'email@test.edulinq.org',
                False,
                lms.model.query.BaseQuery(name = 'email@test.edulinq.org'),
            ),

            # Don't Check Email - Label - Name
            (
                'name (123)',
                False,
                lms.model.query.BaseQuery(id = '123', name = 'name'),
            ),

            # Don't Check Email - Label - Email
            (
                'email@test.edulinq.org (123)',
                False,
                lms.model.query.BaseQuery(id = '123', name = 'email@test.edulinq.org'),
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (text, check_email, expected) = test_case

            with self.subTest(msg = f"Case {i} ('{text}'):"):
                actual = lms.model.query.parse_int_query(lms.model.query.BaseQuery, text, check_email)
                self.assertJSONEqual(expected, actual)

    def test_match_base(self):
        """ Test base matching. """

        # [(query, target, expected), ...]
        test_cases = [
            # Exact Match
            (
                lms.model.query.BaseQuery(id = '123'),
                lms.model.query.BaseQuery(id = '123'),
                True,
            ),
            (
                lms.model.query.BaseQuery(name = 'name'),
                lms.model.query.BaseQuery(name = 'name'),
                True,
            ),
            (
                lms.model.query.BaseQuery(email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(email = 'email@test.edulinq.org'),
                True,
            ),
            (
                lms.model.query.BaseQuery(id = '123', name = 'name'),
                lms.model.query.BaseQuery(id = '123', name = 'name'),
                True,
            ),
            (
                lms.model.query.BaseQuery(id = '123', email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(id = '123', email = 'email@test.edulinq.org'),
                True,
            ),
            (
                lms.model.query.BaseQuery(name = 'name', email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(name = 'name', email = 'email@test.edulinq.org'),
                True,
            ),
            (
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                True,
            ),

            # Subset Match
            (
                lms.model.query.BaseQuery(id = '123'),
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                True,
            ),
            (
                lms.model.query.BaseQuery(name = 'name'),
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                True,
            ),
            (
                lms.model.query.BaseQuery(email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                True,
            ),

            # Incomplete Mismatch
            (
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(id = '123'),
                False,
            ),
            (
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(name = 'name'),
                False,
            ),
            (
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(email = 'email@test.edulinq.org'),
                False,
            ),

            # Partial Mismatch
            (
                lms.model.query.BaseQuery(id = '999', name = 'name', email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                False,
            ),
            (
                lms.model.query.BaseQuery(id = '123', name = 'ZZZZ', email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                False,
            ),
            (
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'ZZZZZ@test.edulinq.org'),
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                False,
            ),

            # Full Mismatch
            (
                lms.model.query.BaseQuery(id = '123'),
                lms.model.query.BaseQuery(id = '999'),
                False,
            ),
            (
                lms.model.query.BaseQuery(name = 'name'),
                lms.model.query.BaseQuery(name = 'ZZZZ'),
                False,
            ),
            (
                lms.model.query.BaseQuery(email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(email = 'ZZZZZ@test.edulinq.org'),
                False,
            ),
            (
                lms.model.query.BaseQuery(id = '123', name = 'name'),
                lms.model.query.BaseQuery(id = '999', name = 'ZZZZ'),
                False,
            ),
            (
                lms.model.query.BaseQuery(id = '123', email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(id = '999', email = 'ZZZZZ@test.edulinq.org'),
                False,
            ),
            (
                lms.model.query.BaseQuery(name = 'name', email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(name = 'ZZZZ', email = 'ZZZZZ@test.edulinq.org'),
                False,
            ),
            (
                lms.model.query.BaseQuery(id = '123', name = 'name', email = 'email@test.edulinq.org'),
                lms.model.query.BaseQuery(id = '999', name = 'ZZZZ', email = 'ZZZZZ@test.edulinq.org'),
                False,
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (query, target, expected) = test_case

            with self.subTest(msg = f"Case {i} ('{query}' vs '{target}'):"):
                actual = query.match(target)
                self.assertEqual(expected, actual)
