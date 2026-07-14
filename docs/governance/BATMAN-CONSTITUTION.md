# Batman Constitution

Version 2.0

---
Mission

Build an educational intelligence platform that becomes more capable over time while minimizing unnecessary complexity and dependence on external AI.

---
Batman is an educational intelligence system.

Every future feature shall follow these principles.

---

## Principle 1 

 Buy Before Build

Before designing or implementing any new capability, Batman engineering shall first evaluate mature, well-supported, production-ready solutions.

Evaluation order:

1. Use an existing solution if it satisfies Batman's requirements.
2. Extend an existing solution if minor customization is sufficient.
3. Build a custom solution only when:
   - no suitable solution exists,
   - licensing prevents adoption,
   - performance requirements cannot be met,
   - or Batman requires unique capabilities that create long-term product value.

Batman shall never reinvent commodity infrastructure that is already solved by mature, production-ready software.

Engineering effort shall focus on Batman's unique intelligence, governance, learning, and user experience—not commodity infrastructure.

Custom code is Batman's most expensive asset.

Every new line of code must justify why an existing production-ready solution is insufficient.

Every recommendation presented during Batman design discussions shall explicitly state whether it is:
- Adopt
- Extend
- Build

----

## Principle 2

Python decides first.

---

## Principle 3

LLMs assist.

They do not control Batman.

---

## Principle 4

Batman never guesses.

If confidence is low,

Batman asks.

---

## Principle 5

Every response is validated before execution.

Understanding alone is never sufficient.

---

## Principle 6

One source of truth.

Every piece of knowledge has exactly one owner.

---

## Principle 7

Batman learns permanently.

Successful interpretations become reusable local knowledge.

Repeated requests should require fewer LLM calls over time.

---

## Principle 8

Knowledge is local.

Student data is local.

Decision making is local.

Cloud AI is optional.

---

## Principle 9

Simple before complex.

Prefer the smallest architecture that satisfies the requirement.

Avoid unnecessary frameworks and abstractions.

---

## Principle 10

Every new feature must answer:

What is the simplest correct implementation?

---

## Principle 11

Every architectural decision must reduce future complexity.

Not increase it.

---

## Principle 12

Batman is deterministic wherever possible.

Randomness belongs only inside educational explanations and creativity.

Never inside workflow.

---

## Principle 14

Architecture before implementation.

If the architecture is unclear,

coding stops until it becomes clear.

---

## Principle 15

Python grows.

LLM dependence shrinks.

Batman should become more intelligent through accumulated knowledge, not through increasing API usage.

---

## Principle 16

Student trust is more important than appearing intelligent.

Batman admits uncertainty.

Batman asks.

Batman verifies.

Batman never invents facts.

---

## Principle 17

Every successful interaction should make Batman better prepared for the next interaction.

Learning is permanent.

Repeated work is failure.

---
## Principle 18

Inspect Before Modify.

Before generating any CPS for an existing file, inspect the current version of that file.

If the file is unavailable, request it first.

Never modify an existing implementation based on memory or assumptions.

---
## Principle 19 

CPS Completion & Backlog Governance

No new CPS shall begin while there are unresolved items from the previous CPS.

If an item is intentionally deferred, it must first be recorded in the Engineering Backlog (BACKLOG.md) with:

- A unique Backlog ID (BKL-xxx)
- Status
- Planned Stage (or Target CPS)
- Reason for Deferral

Only after every unresolved item has either been completed or formally moved to the Engineering Backlog may the next CPS begin.

This rule ensures that technical debt is consciously managed, architectural decisions remain traceable, and no approved work is forgotten.

---
## Principle 20

Every knowledge artifact required during tutoring must be produced during ingestion. Live tutoring must never depend on reprocessing the original source document.

---

## Principle 21

CPS Business Flow Rule

Every CPS must define the business impact of the change in simple language.

Before implementation, each CPS must state:

### Business Flow

Explain where the CPS sits in the product flow and what business process changes.

### Advantage

State the direct product, operational, scale, quality, or customer advantage created by the CPS.

### Disadvantage / Risk

State the limitation, technical debt, dependency, cost, or risk introduced by the CPS.

### Rule

Technical implementation alone is not sufficient.

Every CPS must answer:

1. What changes in the business flow?
2. What advantage does Batman gain?
3. What disadvantage or risk is introduced?

Keep the explanation short and understandable without reading the source code.


---

## Principle 22


---


---
## Batman Engineering Protocol

Protocol Keyword:

BCP

When "BCP" is referenced during any Batman discussion, it means:

- Apply the Batman Constitution.
- Apply Governance.
- Apply KISS.
- Apply Buy Before Build.
- Prefer existing production-ready solutions.
- Follow frozen ADRs.
- Preserve architectural consistency.
- Produce CPS when implementation is requested.
- Explain implementation using Baby Steps unless the user requests otherwise.
- Inspect existing code before generating CPS.

----
## BCP-005 — Extraction Contract (Frozen)

Batman never depends on a specific document extraction engine.

Batman depends only on the Extraction Contract.

Every supported extractor must produce the following artifacts:

- document.md
- document.json
- metadata.json

All downstream components (Chunk Builder, Embedding Engine, Vector Database, Retrieval Engine, Batman Core) consume these artifacts only.

The original PDF is treated as the immutable source document and is never processed again after successful extraction.

This design allows Batman to replace the extraction engine in the future without changing any downstream architecture.
----