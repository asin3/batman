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

from quiz_parser import parse_quiz_request

print(
    parse_quiz_request(
        "Quiz me on Force, Momentum hard 10 questions"
    )
)