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

from quiz_manager import start_quiz
from quiz_manager import set_difficulty
from quiz_manager import set_question_count

quiz = start_quiz("Force")

set_difficulty("Medium")

set_question_count(5)

print(quiz)