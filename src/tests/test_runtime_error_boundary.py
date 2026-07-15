import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from src.runtime_error_boundary import (
    STUDENT_SAFE_ERROR,
    handle_uncaught_exception,
    log_runtime_error
)


class RuntimeErrorBoundaryTests(unittest.TestCase):

    def test_log_runtime_error_writes_traceback(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            log_path = (
                Path(temp_dir)
                / "runtime_errors.log"
            )

            try:

                raise ValueError(
                    "test failure"
                )

            except ValueError as error:

                log_runtime_error(
                    type(error),
                    error,
                    error.__traceback__,
                    log_path=log_path
                )

            content = log_path.read_text(
                encoding="utf-8"
            )

            self.assertIn(
                "ValueError: test failure",
                content
            )
            self.assertIn(
                "Traceback",
                content
            )

    def test_uncaught_exception_handler_shows_safe_message_only(self):

        output = io.StringIO()

        with tempfile.TemporaryDirectory() as temp_dir:

            log_path = (
                Path(temp_dir)
                / "runtime_errors.log"
            )

            try:

                raise RuntimeError(
                    "student should not see this"
                )

            except RuntimeError as error:

                with redirect_stdout(output):

                    handle_uncaught_exception(
                        type(error),
                        error,
                        error.__traceback__,
                        log_path=log_path
                    )

            log_content = log_path.read_text(
                encoding="utf-8"
            )

            self.assertIn(
                "student should not see this",
                log_content
            )
            self.assertIn(
                "Traceback",
                log_content
            )

        visible_text = output.getvalue()

        self.assertIn(
            STUDENT_SAFE_ERROR,
            visible_text
        )
        self.assertNotIn(
            "Traceback",
            visible_text
        )
        self.assertNotIn(
            "student should not see this",
            visible_text
        )


if __name__ == "__main__":

    unittest.main()
