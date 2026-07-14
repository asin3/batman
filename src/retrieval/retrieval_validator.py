"""
============================================================

Batman Student

Retrieval Validation Engine

Purpose

Validate retrieval quality using
known test questions.

============================================================
"""

import sys

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(0, str(PROJECT_ROOT))


from retrieval_engine import retrieve


TEST_CASES = [

    {

        "question": "What is neuron?",

        "expected_heading": "10.2.1 Structure of the neuron"

    },

    {

        "question": "Reflex action",

        "expected_heading": "Reflex"

    },

    {

        "question": "Human brain",

        "expected_heading": "Brain"

    },

    {

        "question": "Types of neurons",

        "expected_heading": "Types of neurons"

    },

    {

        "question": "Nervous tissue",

        "expected_heading": "Nervous"

    }

]


passed = 0


print()

print("=" * 60)

print("RETRIEVAL VALIDATION")

print("=" * 60)

print()


for test in TEST_CASES:

    results = retrieve(

        test["question"],

        top_k=1

    )


    heading = results[0]["heading"]


    ok = (

        test["expected_heading"].lower()

        in heading.lower()

    )


    print(

        f"{'PASS' if ok else 'FAIL'} "

        f"{test['question']}"

    )

    print(

        f"Expected : "

        f"{test['expected_heading']}"

    )

    print(

        f"Returned : "

        f"{heading}"

    )

    print()


    if ok:

        passed += 1


print("-" * 60)

print(

    f"Passed : "

    f"{passed}/{len(TEST_CASES)}"

)