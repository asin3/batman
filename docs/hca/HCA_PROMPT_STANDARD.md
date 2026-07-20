# HCA Prompt Standard
## Prompt Template for Orion
## To be followed by Athena
Version: 1.0

---

# Purpose

This document defines the standard structure Athena shall use when creating prompts for Orion.

Future prompts should follow this template instead of creating ad-hoc instructions.

Orion shall first read:

docs/hca/HCA_PLAYBOOK.md

before processing any request.

---

# Standard Prompt Structure

==================================================

HCA TASK REQUEST

==================================================

Date

Time

Title

---

## Objective

Describe the required outcome.

---

## Background

Business context.

Architecture context.

Previous decisions.

---

## Repository Context

Relevant folders.

Relevant modules.

Relevant ADRs.

Relevant CPS.

Relevant reports.

---

## Files To Read

Explicit list of files.

The first file shall always be:

docs/hca/HCA_PLAYBOOK.md

unless explicitly waived by the Product Owner.

---

## Constraints

Examples:

- Repository evidence only.
- No speculation.
- Do not write code.
- Do not modify files.
- Preserve ADRs.
- KISS.

---

## Deliverables

Examples:

Architecture Review

Implementation Plan

Migration Strategy

Risk Assessment

Testing Strategy

Documentation

Code

(as requested)

---

Success Criteria

Clearly define what constitutes successful completion of the task.

If implementation is requested,

explicitly state:

- Architecture Review
- CPS
- Implementation
- Unit Testing
- Implementation Report

Never combine multiple engineering stages into one request unless explicitly approved.

---

## Output Format

Executive Summary

Findings

Recommendations

Risks

Open Questions

Architecture Status

---

## Additional Notes

Any task-specific instructions.

==================================================

END OF REQUEST

==================================================

---

# Prompt Writing Rules

Athena should:

- Keep prompts focused.
- Avoid mixing unrelated objectives.
- Reference existing reports instead of repeating them.
- Reference HCA_PLAYBOOK instead of rewriting engineering rules.
- Define success criteria.
- Clearly identify implementation vs review tasks.
- Keep terminology consistent.

---

# Goal

Create prompts that are:

- predictable
- reviewable
- reusable
- repository-driven
- architecture-first