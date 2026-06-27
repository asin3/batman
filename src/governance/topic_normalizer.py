"""
===========================================================
Batman Student

Module:
topic_normalizer.py

Purpose:
Provide a single source of truth for chapter/topic names.

Responsibilities:

• Remove OCR artifacts
• Remove unwanted punctuation
• Normalize spacing
• Normalize capitalization
• Produce consistent topic names across Batman

Owner:
Student Intelligence

Reads:
Raw topic/chapter strings

Writes:
Normalized topic/chapter strings

===========================================================
"""

import re


# ---------------------------------------------------------
# CLEANUP RULES
# ---------------------------------------------------------

COMMON_PREFIXES = [

    "me",

    "the",

    "chapter"

]

PUNCTUATION_PATTERN = r"[,:;]+$"


# ---------------------------------------------------------
# NORMALIZE
# ---------------------------------------------------------

def normalize_topic_name(name):

    if not name:

        return ""

    topic = name.strip()

    # Collapse multiple spaces

    topic = re.sub(

        r"\s+",

        " ",

        topic

    )

    # Remove trailing punctuation

    topic = re.sub(

        PUNCTUATION_PATTERN,

        "",

        topic

    )

    # Lowercase for cleanup

    topic = topic.lower()

# ---------------------------------------------------------
# REMOVE COMMON PREFIXES
# ---------------------------------------------------------

    words = topic.split()

    while words and words[0] in COMMON_PREFIXES:

        words.pop(0)

    topic = " ".join(words)


# ---------------------------------------------------------
# FINAL CLEANUP
# ---------------------------------------------------------

    topic = topic.strip()

    if not topic:

        return ""

    # Title Case

    topic = topic.title()

    return topic


# ---------------------------------------------------------
# BATCH NORMALIZATION
# ---------------------------------------------------------

def normalize_topics(topics):

    normalized = []

    for topic in topics:

        cleaned = normalize_topic_name(topic)

        if cleaned:

            normalized.append(cleaned)

    return normalized


# ---------------------------------------------------------
# COMPARE TOPICS
# ---------------------------------------------------------

def topics_equal(topic1, topic2):

    return (

        normalize_topic_name(topic1)

        ==

        normalize_topic_name(topic2)

    )

# ---------------------------------------------------------
# SAMPLE TEST DATA
# ---------------------------------------------------------

def sample_topics():

    return [

        "me  current ,",

        "ME CURRENT",

        " current ",

        "chapter force",

        "the moment of force",

        "Force",

        " force "

    ]


# ---------------------------------------------------------
# DEMO
# ---------------------------------------------------------

def run_demo():

    print("\n" + "=" * 60)

    print("TOPIC NORMALIZER")

    print("=" * 60)

    print()

    for topic in sample_topics():

        normalized = normalize_topic_name(topic)

        print(f"{topic:<30} -> {normalized}")

    print()

    print("=" * 60)


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

def validate():

    assert topics_equal(

        "me current",

        "Current"

    )

    assert topics_equal(

        "Force",

        " force "

    )

    assert topics_equal(

        "chapter force",

        "FORCE"

    )

    print("Validation Passed.")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    run_demo()

    print()

    validate()


if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print("\nERROR")

        print("-" * 40)

        print(e)

        print("-" * 40)