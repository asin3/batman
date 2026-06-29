"""
===========================================================
Batman Student

Module:
paths.py

Purpose:
Single source of truth for all filesystem paths.

Owner:
Batman Student Core

Reads:
-

Writes:
-

Governed By:
ADR-001 Desktop First
ADR-004 Data Governance

Single Source of Truth:
Filesystem Architecture
===========================================================
"""

from pathlib import Path


# ---------------------------------------------------------
# PROJECT ROOT
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------
# ROOT DIRECTORIES
# ---------------------------------------------------------

DATA_DIR = PROJECT_ROOT / "data"

DOCS_DIR = PROJECT_ROOT / "docs"

VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"


# ---------------------------------------------------------
# TEXTBOOK
# ---------------------------------------------------------

TEXTBOOK_DIR = (
    DATA_DIR
    / "class10"
    / "physics"
    / "textbook"
)

SOURCE_DIR = TEXTBOOK_DIR / "source"

STAGING_DIR = TEXTBOOK_DIR / "staging"

GENERATED_DIR = TEXTBOOK_DIR / "generated"

ARCHIVE_DIR = TEXTBOOK_DIR / "archive"


# ---------------------------------------------------------
# STUDENT DATA
# ---------------------------------------------------------

STUDENTS_DIR = (
    DATA_DIR
    / "students"
)


# ---------------------------------------------------------
# GOVERNANCE
# ---------------------------------------------------------

GOVERNANCE_DIR = (
    DATA_DIR
    / "governance"
    / "ICSE"
    / "class10"
    / "physics"
)


# ---------------------------------------------------------
# REPORTS
# ---------------------------------------------------------

REPORTS_DIR = (
    DATA_DIR
    / "class10"
    / "physics"
    / "reports"
)


# ---------------------------------------------------------
# LEARNING RESOURCES
# ---------------------------------------------------------

NOTES_DIR = (
    DATA_DIR
    / "class10"
    / "physics"
    / "notes"
)

PYQ_DIR = (
    DATA_DIR
    / "class10"
    / "physics"
    / "pyq"
)

QUESTION_BANK_DIR = (
    DATA_DIR
    / "class10"
    / "physics"
    / "question_bank"
)

REFERENCES_DIR = (
    DATA_DIR
    / "class10"
    / "physics"
    / "references"
)