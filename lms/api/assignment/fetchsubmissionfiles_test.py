import lms.api.testing
import lms.api.assignment.fetchsubmissionfiles
import lms.api.assignment.testing

class AssignmentFetchSubmissionFilesTest(lms.api.testing.HTTPTest):
    """ Test fetching assignment submission files. """

    def test_assignment_fetch_submission_files_base(self):
        """ Test the base functionality of fetching assignment scores. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            (
                {
                    'assignment': '67892',
                },
                ('', 3),
                None,
            ),

            (
                {
                    'assignment': 'Assignment 3',
                },
                ('', 3),
                None,
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (extra_kwargs, expected, error_substring) = test_case

            with self.subTest(msg = f"Case {i}:"):
                kwargs = self.get_base_args()
                kwargs.update(extra_kwargs)

                try:
                    actual = lms.api.assignment.fetchsubmissionfiles.request(**kwargs)
                except Exception as ex:
                    error_string = self.format_error_string(ex)
                    if (error_substring is None):
                        self.fail(f"Unexpected error: '{error_string}'.")

                    self.assertIn(error_substring, error_string, 'Error is not as expected.')

                    continue

                if (error_substring is not None):
                    self.fail(f"Did not get expected error: '{error_substring}'.")

                self.assertEqual(expected[1], actual[1])
