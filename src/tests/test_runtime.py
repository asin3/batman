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

set_question_count(2)

print(get_quiz_state())

increment_question()

print(
    is_quiz_complete()
)

increment_question()

print(
    is_quiz_complete()
)

increment_score()

print(get_quiz_state())