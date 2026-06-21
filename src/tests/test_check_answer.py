import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from quiz_manager import *

reset_runtime()

set_question_count(2)

set_current_answer("A")

print(
    check_answer("A")
)

print(
    get_quiz_state()
)

print(
    check_answer("B")
)

print(
    get_quiz_state()
)

print(
    is_quiz_complete()
)