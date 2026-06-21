import re


def parse_quiz_request(text):

    result = {
        "topics": [],
        "difficulty": "",
        "count": 0
    }

    text_lower = text.lower()

    # -------------------------
    # Difficulty
    # -------------------------

    if "easy" in text_lower:
        result["difficulty"] = "easy"

    elif "medium" in text_lower:
        result["difficulty"] = "medium"

    elif "hard" in text_lower:
        result["difficulty"] = "hard"

    # -------------------------
    # Question Count
    # -------------------------

    numbers = re.findall(
        r"\d+",
        text
    )

    if numbers:

        result["count"] = int(
            numbers[0]
        )

    # -------------------------
    # Topics
    # -------------------------

    topic_text = text_lower

    topic_text = topic_text.replace(
        "quiz",
        ""
    )

    topic_text = re.sub(
        r"\b(easy|medium|hard)\b",
        "",
        topic_text
    )

    topic_text = re.sub(
        r"\d+",
        "",
        topic_text
    )

    topic_text = topic_text.replace(
        "questions",
        ""
    )

    topic_text = topic_text.replace(
        "question",
        ""
    )

    topic_text = topic_text.replace(
        "on",
        ""
    )

    topic_text = topic_text.strip()

    if topic_text:

        result["topics"] = [
            topic_text
        ]

    return result