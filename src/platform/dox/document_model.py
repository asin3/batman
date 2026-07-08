"""
============================================================
Batman DOX Import Engine (BDIE)

Document Model

Purpose:
Defines the universal document structure produced by all
document readers (DOCX, PDF, Excel, HTML, etc.).

This model is intentionally product-agnostic.
Batman, Spiderman, Superman and other products will build
their own JSON from this model.

============================================================
"""

from dataclasses import dataclass, field


# ============================================================
# Topic
# ============================================================

@dataclass
class Topic:
    title: str


# ============================================================
# Chapter
# ============================================================

@dataclass
class Chapter:
    number: str
    title: str
    full_title: str
    topics: list[Topic] = field(default_factory=list)


# ============================================================
# Group
# (Unit / Section / Semester / Module ...)
# ============================================================

@dataclass
class Group:
    title: str
    chapters: list[Chapter] = field(default_factory=list)


# ============================================================
# Subject
# ============================================================

@dataclass
class Subject:
    title: str
    groups: list[Group] = field(default_factory=list)
    chapters: list[Chapter] = field(default_factory=list)


# ============================================================
# Document
# ============================================================

@dataclass
class Document:
    document_type: str
    subjects: list[Subject] = field(default_factory=list)


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    document = Document(document_type="curriculum")

    print(document)