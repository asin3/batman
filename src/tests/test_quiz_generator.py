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

from quiz_generator import generate_mcq

context = """
Force is a push or pull.

The SI unit of force is Newton.

Force can change the state of motion.
"""

print(
    generate_mcq(
        context,
        "easy"
    )
)