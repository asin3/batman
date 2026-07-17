# ADR-011
# Knowledge Asset Contract v1.0

Status
FROZEN

---

## Purpose

Defines the immutable knowledge artifacts produced by Batman's ingestion pipeline.

All downstream systems (Retrieval, Tutor, DD, APIs, UI, Embeddings) consume these contracts.

Only the producing stage may modify its artifact.

---

# Artifact Ownership

Docling Extractor
    document.json
    figure_manifest.json

Chunk Builder
    chunks.json

Knowledge Asset Builder
    manifest.json
    enriches:
        figure_manifest.json
        chunks.json

Pipeline Runner
    validates artifacts
    orchestrates execution

---

# Frozen Artifacts

## document.json

Owner
Docling Extractor

Purpose

Canonical Docling document.

Never edited downstream.

---

## figure_manifest.json

Owner
Docling Extractor

Enriched by
Knowledge Asset Builder

Frozen Fields

- figure_id
- document_id
- docling_picture
- page
- caption
- file
- status

Status Lifecycle

PENDING
PROCESSING
COMPLETED
RETRY_QUEUED
SKIPPED
FAILED
RESOLVED

---

## chunks.json

Owner
Chunk Builder

Enriched by
Knowledge Asset Builder

Frozen Fields

- id
- heading
- content
- page
- label
- parent
- children
- source_objects
- figure_refs
- table_refs

---

## manifest.json

Owner
Knowledge Asset Builder

Purpose

Knowledge asset summary.

Frozen Sections

- knowledge_assets
- pipeline

Pipeline Fields

docling_extracted
chunks_built
figures_extracted
tables_extracted
knowledge_linked
validated
embeddings_created

---

# Design Rules

Document IDs are immutable.

Figure IDs are immutable.

Chunk IDs are immutable.

Table IDs are immutable.

Artifacts are append-only.

Downstream components consume artifacts.

They never regenerate them.

---

# Producer / Consumer Contract

Producer
↓

Consumer

Docling
↓

Chunk Builder

Chunk Builder
↓

Knowledge Asset Builder

Knowledge Asset Builder
↓

Embedding Engine

Embedding Engine
↓

Retrieval Engine

Retrieval Engine
↓

Batman Tutor

---

Status

Knowledge Asset Contract v1.0

FROZEN