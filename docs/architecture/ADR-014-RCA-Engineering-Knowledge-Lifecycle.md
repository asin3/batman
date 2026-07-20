# ADR-014: RCA Engineering Knowledge Lifecycle

**Status:** Proposed (Pending Approval)

**Version:** 1.0

**Date:** 2026-07-20

**Owner:** Athena (Chief Architect)

---

# Purpose

This ADR defines how RCA captures, reviews, preserves, and reuses engineering knowledge throughout the software development lifecycle.

The objective is to ensure that engineering knowledge becomes a permanent organizational asset rather than remaining inside chat conversations or individual team members.

Engineering knowledge shall be treated as a first-class product artifact.

---

# Problem Statement

Traditional AI coding assistants complete a task and immediately forget the engineering decisions that led to the implementation.

As projects grow, this results in:

- Repeated mistakes
- Inconsistent engineering decisions
- Loss of architectural reasoning
- Duplicate discussions
- Poor traceability
- Weak governance

RCA shall instead continuously build an Engineering Knowledge Base from every engineering activity.

---

# Architectural Principle

Engineering work does not end with code.

Every engineering activity produces knowledge.

Every knowledge artifact shall become searchable, reviewable, and reusable.

---

# Engineering Knowledge Lifecycle

Business Requirement

↓

Architecture Review

↓

Approved Architecture

↓

CPS

↓

Athena CPS Review

↓

Implementation

↓

Implementation Report

↓

Athena Implementation Review

↓

Product Owner UAT

↓

Merge Readiness Review

↓

Merge

↓

Knowledge Extraction

↓

Engineering Knowledge Base

↓

Future RCA Learning

---

# Engineering Artifacts

Every engineering stage shall produce one primary engineering artifact.

Examples include:

- Architecture Review
- CPS
- Implementation Report
- Athena Implementation Review
- Product Owner UAT Report
- Merge Readiness Review
- Bug Fix Report
- Refactoring Report

Engineering artifacts become permanent engineering records.

---

# Engineering Memory

Engineering memory shall be constructed from engineering artifacts.

Examples:

- Architecture decisions
- Common implementation mistakes
- Approved implementation patterns
- Rejected approaches
- Review observations
- Lessons learned

Engineering memory shall never depend upon chat history.

---

# Review Inputs

Athena shall perform engineering reviews using repository evidence.

Examples include:

- Git Diff
- Changed Files
- CPS
- ADRs
- Engineering Artifacts
- Repository Structure
- Static Analysis Reports
- Unit Testing Results

Additional review inputs may be introduced as RCA evolves.

The review process shall remain technology independent.

---

# Review Outputs

Every Athena review shall produce:

- Decision
- Findings
- Mandatory Actions
- Recommendations
- Governance Improvements
- Architecture Status
- Overall Risk

These become part of the permanent engineering record.

---

# Knowledge Extraction

After every completed engineering cycle RCA shall identify reusable knowledge.

Examples:

- Frequently approved solutions
- Frequently rejected implementations
- Common migration patterns
- Architecture anti-patterns
- Coding standards
- Governance improvements

Extracted knowledge becomes available for future engineering work.

---

# Artifact Repository

Engineering artifacts shall be stored separately from application source code and application data.

Repository structure:

docs/

├── architecture/

├── hca/

├── reviews/

├── uat/

└── knowledge/

Application data shall never contain engineering artifacts.

---

# Future Automation

Future versions of RCA may automatically:

- Generate Git Diffs
- Generate Architecture Summaries
- Run Static Analysis
- Detect ADR violations
- Search previous engineering reviews
- Recommend similar CPS implementations
- Surface previous implementation risks

Automation shall assist engineering judgment.

Automation shall never replace engineering judgment.

---

# Guiding Principles

Engineering knowledge belongs to Selten.

Engineering knowledge shall outlive individual chats.

Engineering knowledge shall be reviewable.

Engineering knowledge shall be traceable.

Engineering knowledge shall continuously improve RCA.

---

# Consequences

Positive

- Better engineering governance
- Reduced repeated mistakes
- Better architectural consistency
- Faster onboarding
- Improved engineering confidence
- Foundation for intelligent RCA evolution

Trade-offs

- More engineering documentation
- Larger knowledge repository
- Additional review discipline

These trade-offs are accepted.

---

# Future Evolution

This ADR intentionally remains technology agnostic.

Future versions may introduce:

- Git Diff automation
- AST analysis
- Semgrep
- CodeQL
- Architecture Graphs
- Knowledge Graphs
- AI-assisted architectural reasoning

These technologies enhance the Engineering Knowledge Lifecycle but do not change its principles.

---

# Decision

Selten adopts the Engineering Knowledge Lifecycle as the permanent mechanism for capturing, preserving, reviewing, and reusing engineering knowledge across all future products and repositories.

Engineering knowledge is recognized as a strategic organizational asset.