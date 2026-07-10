# ADR-007: Knowledge Ingestion Lifecycle

Status: Accepted

Date: 2026-07-10

---

# Context

Batman ingests multiple academic resources including textbooks, notes, PYQs, question banks, references and solved papers.

Every document must follow one standardized ingestion pipeline.

---

# Decision

Every academic document shall follow the same lifecycle.

```
RAW
    ↓
REGISTERED
    ↓
PARSED
    ↓
METADATA_ENRICHED
    ↓
CHUNKED
    ↓
EMBEDDED
    ↓
INDEXED
    ↓
ACTIVE
    ↓
ARCHIVED
```

---

# Registration

When a document is copied into a source folder, Batman automatically:

- assigns Document ID
- records filename
- records board
- records class
- records subject
- records source type
- sets status = RAW

---

# Parsing

Batman parses documents using Docling.

Output includes:

- text
- headings
- tables
- figures
- page numbers
- reading order

---

# Metadata

Every chunk stores:

- Document ID
- Board
- Class
- Subject
- Source Type
- Chapter
- Topic
- Page
- Chunk Number

---

# Chunking

Chunking is structure-aware.

Priority:

1. Heading
2. Topic
3. Paragraph
4. Table
5. Exercise
6. Figure Caption

Character-count chunking is used only as a fallback.

---

# Embedding

Only ACTIVE chunks are embedded.

Archived documents are excluded.

---

# Lifecycle Rules

A document may exist in only one lifecycle state at a time.

Transitions are automatic.

---

# Future Compatibility

Supports:

- ICSE
- CBSE
- State Boards
- Class 1–12
- Multiple Languages
- Images
- Diagrams
- Tables
- Future Vision Models

---

# Status

Accepted.

Frozen for Product 1.0.