# ADR-004: Data Governance & Folder Ownership

**Status:** Accepted

**Date:** 2026-06-25

---

# Context

As Batman Student grows across multiple subjects, boards, students, and AI providers, uncontrolled file placement creates architectural drift.

To ensure maintainability, every file within the project shall have a single owner and a single source of truth.

---

# Decision

Batman Student adopts a strict **Domain Ownership Model**.

Every file belongs to exactly one domain.

---

# Domain 1 — Academic Content

Location:

data/class10/

Contains:

* Textbooks
* Notes
* PYQs
* Question Banks
* References
* Sample Solved Papers
* Reports

Never stores:

* Student history
* Progress
* Learning state
* Preferences

---

# Domain 2 — Student Data

Location:

data/students/

Contains:

* History
* Learning State
* Progress
* Preferences
* Bookmarks
* Quiz Attempts

Never stores:

* Textbooks
* OCR Output
* Question Banks

---

# Domain 3 — System Data

Location:

vector_db/

Contains:

* Embeddings
* Indexes
* Search Collections
* Runtime Cache

Never stores:

* Student data
* Academic content

---

# Domain 4 — Governance

Location:

data/governance/

Contains:

* subject_map.json
* chapter_map.json
* topic_map.json
* curriculum metadata

Never stores:

* Conversations
* OCR text
* Student information

---

# Single Source of Truth

Every dataset shall exist in one location only.

Examples:

History

✓ data/students/STD001/history.json

✗ Any other location

Question Bank

✓ data/class10/physics/question_bank/

✗ Student folders

Vector Database

✓ vector_db/

✗ Subject folders

---

# Module Ownership

Conversation Manager

Reads:

Student

Writes:

Student

Question Bank

Reads:

Academic Content

Writes:

Academic Content

OCR Pipeline

Reads:

Academic Content

Writes:

Academic Content

Retriever

Reads:

Vector Database

Writes:

None

Governance

Reads:

Academic Content

Writes:

Governance

---

# Governance Header

Every Python module shall begin with a Governance Header documenting:

* Purpose
* Owner
* Reads
* Writes
* Dependencies
* Single Source of Truth

---

# Architecture Checklist

Before introducing any new file:

1. Which domain owns it?
2. Does a similar file already exist?
3. Is there already a Single Source of Truth?
4. Which module writes it?
5. Which modules read it?
6. Does it violate another domain?

If any answer is unclear, implementation shall stop until resolved.

---

# Future Compatibility

This ADR applies to:

* Multiple Subjects
* Multiple Boards
* Local LLM
* Cloud Synchronization
* Parent Portal
* Teacher Portal
* Multi-user deployments

---

# Status

Accepted.

Frozen for Product 1.0.
