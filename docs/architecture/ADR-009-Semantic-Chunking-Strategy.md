# ADR-009 — Semantic Chunking Strategy

## Status

Accepted

---

## Decision

Batman will not use generic text splitters.

Batman will build semantic educational chunks based on document structure.

Chunk boundaries are determined by educational meaning rather than character count.

Examples include:

- Chapter
- Section
- Definition
- Explanation
- Formula
- Example
- Diagram
- Table
- Exercise
- Question
- Summary

These relationships must be preserved whenever possible.

---

## Rationale

Generic splitters optimize for LLM context windows.

Batman optimizes for learning.

Educational content must retain semantic relationships so that explanations, examples, diagrams, formulas and exercises remain connected.

---

## Future Improvements

Chunking rules will continuously evolve as Batman learns from real student interactions.

This ADR defines the architectural principle rather than a fixed implementation.