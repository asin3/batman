"""
============================================================
Batman Student

Module:
runtime_error_boundary.py

Purpose:
Prevent internal Python tracebacks from being shown to students.

Owner:
Batman Runtime Safety

Reads:
-

Writes:
- data/runtime/runtime_errors.log

Governed By:
Batman Constitution
ADR-004 Data Governance
============================================================
"""

from datetime import datetime
import sys
import traceback

from src.config.paths import DATA_DIR


STUDENT_SAFE_ERROR = (
    "I hit a technical issue while continuing that response. "
    "Please try again, or ask the question another way."
)

DEFAULT_LOG_PATH = (
    DATA_DIR
    / "runtime"
    / "runtime_errors.log"
)


def log_runtime_error(
    exc_type,
    exc_value,
    exc_traceback,
    log_path=DEFAULT_LOG_PATH
):

    log_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().isoformat(
        timespec="seconds"
    )

    details = "".join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback
        )
    )

    with open(
        log_path,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n"
            + "=" * 80
            + "\n"
        )

        file.write(
            f"Timestamp: {timestamp}\n"
        )

        file.write(details)


def handle_uncaught_exception(
    exc_type,
    exc_value,
    exc_traceback,
    log_path=DEFAULT_LOG_PATH
):

    if issubclass(
        exc_type,
        KeyboardInterrupt
    ):

        sys.__excepthook__(
            exc_type,
            exc_value,
            exc_traceback
        )

        return

    try:

        log_runtime_error(
            exc_type,
            exc_value,
            exc_traceback,
            log_path=log_path
        )

    except Exception:

        pass

    print()
    print("BATMAN-STUDENT")
    print("-" * 70)
    print(STUDENT_SAFE_ERROR)
    print()


def install_runtime_error_boundary():

    sys.excepthook = handle_uncaught_exception
