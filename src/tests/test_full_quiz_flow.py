import sys
import os
import re

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import chromadb

from quiz_generator import generate_mcq
from quiz_manager import (
    start_quiz,
    set_question_count,
    set_current_answer,
    check_answer,
    get_quiz_state
)

# ---------------------
# START QUIZ
# ---------------------

start_quiz(["force"])

set_question_count(2)

# ---------------------
# RETRIEVE
# ---------------------

db = chromadb.PersistentClient(
    path="./vector_db"
)

collection = db.get_collection(
    "class10_physics"
)

results = collection.query(
    query_texts=["force"],
    n_results=2
)

context = "\n".join(
    results["documents"][0]
)

# ---------------------
# GENERATE MCQ
# ---------------------

mcq = generate_mcq(
    context,
    "easy"
)

print(mcq)

# ---------------------
# EXTRACT ANSWER
# ---------------------

match = re.search(
    r"CORRECT:\s*([ABCD])",
    mcq
)

if match:

    correct_answer = match.group(1)

    set_current_answer(
        correct_answer
    )

    print(
        "\nStored Answer:",
        correct_answer
    )

# ---------------------
# SIMULATE STUDENT
# ---------------------

result = check_answer(
    correct_answer
)

print(
    "\nCorrect?",
    result
)

print(
    "\nQuiz State:"
)

print(
    get_quiz_state()
)