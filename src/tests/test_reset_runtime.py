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

start_quiz(["force"])

set_question_count(5)

increment_question()
increment_question()

increment_score()

print(get_quiz_state())

reset_runtime()

print(get_quiz_state())