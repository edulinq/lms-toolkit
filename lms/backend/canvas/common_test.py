import typing

import edq.testing.unittest

import lms.backend.canvas.common

class TestCanvasCommon(edq.testing.unittest.BaseTest):
    """ Test common Canvas utilities. """

    def test_html_to_markdown_base(self) -> None:
        """ Test converting Canvas HTML to markdown. """

        # [(html, kwargs, expected), ...]
        test_cases: typing.List[typing.Tuple[str, typing.Dict[str, typing.Any], str]] = [
            # Links and Images
            (
                '<p>See the <a href="https://example.com/docs">docs</a>.</p>',
                {},
                'See the [docs](https://example.com/docs).',
            ),
            (
                '<p><img src="https://example.com/diagram.png" alt="diagram"></p>',
                {},
                '![diagram](https://example.com/diagram.png)',
            ),

            # Code
            (
                '<p>Return <code>arr[i]</code>.</p>',
                {},
                'Return `arr[i]`.',
            ),
            (
                '<p>Match <code>[aeiou]+</code>.</p>',
                {},
                'Match `[aeiou]+`.',
            ),

            # Brackets
            (
                '<p>The capital of France is [capital].</p>',
                {},
                'The capital of France is [capital].',
            ),

            # Placeholders
            (
                '<p>The capital of France is [capital].</p>',
                {'replace_placeholders': True},
                'The capital of France is <placeholder>capital</placeholder>.',
            ),
            (
                '<p>See the <a href="https://example.com/docs">docs</a>: [answer]</p>',
                {'replace_placeholders': True},
                'See the [docs](https://example.com/docs): <placeholder>answer</placeholder>',
            ),
            (
                '<p><img src="https://example.com/diagram.png" alt="diagram"> [answer]</p>',
                {'replace_placeholders': True},
                '![diagram](https://example.com/diagram.png) <placeholder>answer</placeholder>',
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (html, kwargs, expected) = test_case

            with self.subTest(msg = f"Case {i} ('{html}'):"):
                actual = lms.backend.canvas.common.html_to_markdown(html, **kwargs)
                self.assertEqual(expected, actual)
