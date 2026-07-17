# ============================================================
# BATMAN STUDENT
#
# ENGINEERING BACKLOG
#
# Version : 1.0
#
# ============================================================

## Purpose

This document records approved engineering improvements that
are intentionally deferred.

Nothing may be postponed without creating a Backlog Item
(BKL-xxx).

This backlog prevents architectural debt from becoming
forgotten technical debt.

---

# Rules

1. Every deferred engineering improvement must receive a unique
   Backlog ID.

2. Every Backlog Item must have:
   - Priority
   - Status
   - Planned Stage
   - Reason for Deferral

3. No Backlog Item may be deleted.
   It must be marked Completed or Cancelled.

4. When a Backlog Item becomes active, it must be promoted into
   a CPS and recorded in the Promotion Log.

5. No new CPS may begin while unresolved work from the previous
   CPS exists unless that work has been formally moved into
   this backlog.

---

# Status Legend

| Status | Meaning |
|---------|---------|
| Proposed | Identified but not yet approved |
| Approved | Accepted and waiting |
| Current CPS | Currently under implementation |
| Deferred | Approved for later implementation |
| In Progress | Being implemented |
| Completed | Finished |
| Cancelled | No longer required |

---

# Active Backlog

---

## BKL-001

**Title**

Standard Bootstrap

**Priority**

High

**Status**

Deferred

**Planned Stage**

After CPS-006

**Reason for Deferral**

Avoid modifying every executable file while the Knowledge Layer
is still evolving.

**Description**

Replace repeated:

- PROJECT_ROOT
- sys.path
- bootstrap logic

with one reusable bootstrap utility.

---

## BKL-002

**Title**

Document Adapter Object

**Priority**

Medium

**Status**

Deferred

**Planned Stage**

After CPS-006

**Reason for Deferral**

Current function-based API is sufficient.

Object-based API can be introduced once the Knowledge Layer is
stable.

**Future Direction**

Instead of

- get_content_texts()
- get_normalized_pictures()
- get_normalized_tables()

Batman should expose

knowledge = load_document(...)

knowledge.texts

knowledge.pictures

knowledge.tables

knowledge.groups

---

## BKL-003

**Title**

Stable Chunk IDs

**Priority**

High

**Status**

Deferred

**Planned Stage**

Before Production Beta

**Reason for Deferral**

Temporary IDs are sufficient during development.

**Current**

CHUNK000001

**Future**

DOC000013-SEC010-0001

(or equivalent permanent format)

---

## BKL-004

**Title**

Knowledge Linking

**Priority**

Critical

**Status**

Current CPS

**Planned Stage**

CPS-006.3

**Description**

Populate:

- parent
- children
- figure_refs
- table_refs

using Docling relationships.

---

## BKL-005

**Title**

Figure Rendering

**Priority**

Medium

**Status**

Deferred

**Planned Stage**

Batman-DD Phase 1

**Description**

CLI

Display:

Figure 10.1 (Page X)

Batman-DD

Render the actual figure.

---

## BKL-006

**Title**

Table Rendering

**Priority**

Medium

**Status**

Deferred

**Planned Stage**

Batman-DD Phase 1

**Description**

Render textbook tables inside Batman-DD.

---

## BKL-007

**Title**

Chunk Quality Metrics

**Priority**

High

**Status**

Deferred

**Planned Stage**

Before Alpha Testing

**Description**

Generate build statistics:

- Total Chunks
- Average Chunk Length
- Sections
- Pictures Linked
- Tables Linked
- Coverage
- Empty Chunks
- Quality Warnings

---

## BKL-008

**Title**

Retrieval Diagnostics

**Priority**

High

**Status**

Deferred

**Planned Stage**

Before Alpha Testing

**Description**

Expose retrieval diagnostics:

- Matched Chunk
- Matched Section
- Matched Figure
- Matched Table
- Confidence
- Retrieval Time

---

## BKL-009

**Title**

Knowledge Build Report

**Priority**

Medium

**Status**

Deferred

**Planned Stage**

Before Multi-document Ingestion

**Description**

Generate a build report after ingestion:

PDF

↓

Sections

↓

Chunks

↓

Embeddings

↓

Coverage

↓

Warnings

---

## BKL-010

**Title**

Knowledge Graph

**Priority**

Low

**Status**

Deferred

**Planned Stage**

Batman v3

**Description**

Connect related concepts into a knowledge graph.

Example

Neuron

↓

Brain

↓

Spinal Cord

↓

Reflex Arc

---

## BL-011 — Batman Master Build Flow Documentation

### Status
BACKLOG

### Priority
HIGH

### Added During
CPS-006.3A

### Description

Create the single authoritative build-flow document for Batman.

Unlike ADRs or CPS documents, this document records the final approved architecture after experimentation and freezes.

It should answer:

- How Batman is built end-to-end.
- Component responsibilities.
- Processing pipeline.
- Objects produced at each stage.
- Inputs and outputs.
- Frozen architecture decisions.
- Dependencies between modules.
- Knowledge lifecycle.
- Retrieval lifecycle.
- Conversation lifecycle.

This document becomes the engineering source of truth.

### Scope (Future)

Examples of sections:

- Complete Batman Pipeline
- Knowledge Ingestion Flow
- Knowledge Asset Flow
- Knowledge Linking Flow
- Embedding Flow
- Retrieval Flow
- Conversation Flow
- Memory Flow
- UI Flow
- Batman-DD Integration
- Frozen Architecture Diagram
- Object Relationship Diagram
- Sequence Diagrams

### Deliverables

Future derivative documents can be generated from this master document:

- Developer Documentation
- Architecture Documentation
- Client Technical Documentation
- Business Process Documentation
- Operations Manual
- API Documentation
- Training Material
- Product Whitepaper

### Planned Stage

After Knowledge Layer reaches v1.0 and before Conversation Intelligence.

---
## BL-12 — Intelligent Processing Queue & Admin Alert Dashboard

### Status
BACKLOG

### Priority
HIGH

### Added During
CPS-006.3A.8 — Figure Asset Export

### Description

Batman must never terminate an ingestion pipeline because a single asset fails.

Instead, every processing failure should be recorded in a centralized Processing Queue and surfaced through an Admin Alert Dashboard.

### Scope

Applicable to all ingestion stages:

- Figure Export
- Table Export
- OCR
- Embeddings
- Vector Indexing
- Knowledge Linking
- LLM Processing
- Metadata Generation

### Processing Flow

Asset
    ↓
Processing
    ↓
Success
    └── Continue Pipeline

Failure
    ↓
Retry Queue
    ↓
Alert Dashboard
    ↓
Admin Review
    ↓
Retry / Ignore / Resolve
    ↓
Pipeline Updated

### Each Queue Item Stores

- Queue ID
- Document ID
- Asset Type
- Asset ID
- Processing Stage
- Error Type
- Error Message
- Retry Count
- First Failure
- Last Attempt
- Status
- Resolution Notes

### Alert Dashboard

Display:

- Total Pending
- Critical Failures
- Retry Required
- Recently Resolved
- Failed Documents
- Processing Statistics

### Admin Actions

- Retry Single Asset
- Retry Document
- Retry by Error Type
- Skip Permanently
- Mark Resolved
- Export Error Report

### Future Enhancements

- Automatic Retry Policies
- Priority Queue
- Scheduled Background Retry
- Notification System
- Health Dashboard
- Processing Analytics

### Planned Stage

After Knowledge Layer v1.0 and before Production Deployment.

---
## BL-14 —PAL-002 — Pipeline Artifact Validation
**Stage:** Before Knowledge Layer v1.0 Freeze (during Pipeline Runner implementation)

### Objective
The Pipeline Runner must validate all required artifacts before deciding to skip a document.

### Validation Rules
For every document, verify:

- document.json exists and is valid
- figure_manifest.json exists and is valid
- chunks.json exists and is valid
- manifest.json exists
- required folders (figures/, etc.) exist

### Behavior

If all artifacts are valid:
→ Skip processing.

If any artifact is missing or invalid:
→ Automatically rerun the required upstream stage(s).

Example:

Missing chunks.json
→ Run Chunk Builder only.

Missing figure_manifest.json
→ Run Docling Extractor, then downstream dependent stages.

Corrupted artifact
→ Rebuild only the affected dependency chain.

### Purpose

The operator should never manually delete folders or decide which scripts to rerun.

The Pipeline Runner is responsible for dependency validation, recovery, and resumable execution.
---

## BL-15 PAL-003 — Knowledge Link Coverage Improvement

**Stage:** After Retrieval Validation v1.0

### Objective

Improve deterministic Knowledge Linking coverage so all relevant figures and tables are linked to their semantic chunks.

### Current Observation

Example:

Question:
"What is neuron?"

Returned Chunk:
CHUNK000005
Heading:
10.2.1 Structure of the neuron (Fig. 10.1)

Expected:
figure_refs should contain FIG000001

Actual:
figure_refs = []

### Investigation Areas

- Parent-child relationship traversal
- Heading → Figure association
- Caption → Figure association
- Multi-object provenance
- Cross-page figure references
- Figure-before-text / Figure-after-text scenarios

### Success Criteria

Every figure or table referenced by a chunk is linked deterministically without using heuristics or LLM reasoning.

### Priority

P2 (Quality Improvement)

### Status

BACKLOG

---
## BL-16 PAL-004 — Python Standard Library Namespace Collision

**Issue**

Batman contains:

src/platform/

This can shadow Python's standard library `platform` module when scripts are executed directly from inside `src`.

**Current Workaround**

Run Python entry modules from project root using module execution:

python -m src.student_tutor

Streamlit continues through its controlled application entry point.

**Future Action**

Perform repository-wide import dependency scan and safely rename `src/platform` to a non-standard-library namespace.

Possible target:

src/batman_platform/

**Do Not**

Rename the package without dependency and import analysis.

**Priority**

P2 — Technical Debt / Production Hardening

**Status**

BACKLOG

---

BKL-012

Title

Universal Follow-up Conversation Engine

Priority

High

Status

Proposed

Planned Stage

After Current Production Stabilization

Reason for Deferral

Current implementation was introduced experimentally for Biology through an automated Codex change. The behaviour, scope, and implementation need to be understood before generalising it across Batman.

Business Problem

Batman sometimes asks a follow-up question and sometimes does not.

Currently:

Follow-up behaviour is inconsistent.
It appears to be limited to Biology.
Other subjects and Super Chat do not provide the same conversational experience.

This creates an inconsistent student experience.

Business Goal

Batman should behave like a continuous tutor.

Every meaningful learning interaction should end with an appropriate follow-up opportunity when applicable, regardless of subject.

The experience should be consistent across:

Physics
Chemistry
Biology
Maths
Super Chat

Investigation Required

Before implementation:

Understand how the current Biology follow-up engine works.
Identify all files modified by the original implementation.
Determine why follow-up questions are generated only sometimes.
Separate generic conversation logic from Biology-specific rules.
Design a reusable follow-up engine for all learning modes.
Business Meaning

Today Batman behaves differently depending on where the student is.

After this backlog item:

Batman will have one consistent tutoring style across the entire product instead of each subject behaving differently.

---


----
Proposed addition to reconstructed backlog
#	Item	State
29	Batman HQ ↔ Codex Engineering Workflow Governance — Freeze responsibility boundary: Batman HQ handles WHY/WHAT/business flow/product decisions/architecture and produces ADR/CPS decisions; Codex operates on the actual Batman repository to inspect code, map modules, implement approved CPS, run tests, show diffs and commit through Git workflow.	WORKING MODEL AGREED; NOT YET FORMALLY GOVERNED/FROZEN

---


---
# Promotion Log

| Date | Backlog ID | Promoted To |
|------|------------|-------------|
| 2026-07-12 | BKL-004 | CPS-006.3 – Knowledge Linking |

---

# Completed Backlog

(Completed items are moved here and never deleted.)

---

# Cancelled Backlog

(Cancelled items remain documented for historical traceability.)
