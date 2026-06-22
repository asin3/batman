import json
import re
from pathlib import Path


TEXTBOOK_FOLDER = Path(
    "data/class10/physics/textbook"
)

MCQ_OUTPUT_FOLDER = Path(
    "data/class10/physics/question_bank/mcq"
)

MCQ_OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


def extract_mcqs(text):

    questions = []

    pattern = re.compile(
        r"""
        (\d+)\.\s*
        (.*?)
        \(a\)\s*(.*?)
        \(b\)\s*(.*?)
        \(c\)\s*(.*?)
        \(d\)\s*(.*?)
        Ans\.\s*\((.)\)\s*(.*?)
        (?=
            \n\d+\.
            |
            \Z
        )
        """,
        re.DOTALL | re.VERBOSE
    )

    matches = pattern.findall(
        text
    )

    for match in matches:

        (
            number,
            question,
            option_a,
            option_b,
            option_c,
            option_d,
            answer,
            explanation
        ) = match

        questions.append(
            {
                "question_number": number,
                "question": question.strip(),

                "options": {
                    "A": option_a.strip(),
                    "B": option_b.strip(),
                    "C": option_c.strip(),
                    "D": option_d.strip()
                },

                "correct_answer":
                    answer.upper(),

                "explanation":
                    explanation.strip(),

                "source":
                    "textbook"
            }
        )

    return questions


def process_file(txt_file):

    print(
        f"\nProcessing: {txt_file.name}"
    )

    text = txt_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    if "MULTIPLE CHOICE TYPE" not in text:

        print(
            "No MCQ section found."
        )

        return

    mcq_section = text.split(
        "MULTIPLE CHOICE TYPE"
    )[-1]

    mcqs = extract_mcqs(
        mcq_section
    )

    chapter_name = (
        txt_file.stem
        .replace("chapter-", "")
        .replace(".txt", "")
    )

    output_file = (
        MCQ_OUTPUT_FOLDER /
        f"{chapter_name}.json"
    )

    output_file.write_text(
        json.dumps(
            mcqs,
            indent=4
        ),
        encoding="utf-8"
    )

    print(
        f"Questions Found: {len(mcqs)}"
    )

    print(
        f"Saved: {output_file.name}"
    )


def main():

    txt_files = sorted(
        TEXTBOOK_FOLDER.glob(
            "*.txt"
        )
    )

    for txt_file in txt_files:

        process_file(
            txt_file
        )

    print(
        "\nMCQ EXTRACTION COMPLETE"
    )


if __name__ == "__main__":

    main()