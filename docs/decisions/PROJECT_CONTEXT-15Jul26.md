# BATMAN STUDENT — PROJECT HANDOFF CONTEXT FOR CODEX

## 1. WHAT WE ARE BUILDING

Batman Student is an educational intelligence platform being built by Selten.

It is NOT intended to be a generic chatbot or simple RAG tutor.

Long-term product purpose:

UNDERSTAND THE STUDENT
        ↓
UNDERSTAND WHAT THE STUDENT KNOWS
        ↓
UNDERSTAND WHAT THE STUDENT NEEDS
        ↓
DECIDE THE NEXT BEST LEARNING ACTION
        ↓
LEARN FROM THE RESULT

Batman should act as a Tutor + Coach + Mentor + Learning Companion.

Initial academic scope started with ICSE Class 10 and textbook knowledge.

The architecture is intended to expand later across:

- multiple subjects
- multiple boards
- multiple grades
- tutoring
- homework
- assessment
- adaptive learning
- study planning
- student progress
- parent intelligence
- teacher intelligence

Core product philosophy:

Python decides first.
LLMs assist and do not control Batman.
Batman never guesses.
Validate before acting.
One source of truth.
Learn permanently.
Knowledge and student intelligence remain local where practical.
AI providers remain replaceable.
Simple before complex.
Architecture before implementation.

---

## 2. CURRENT PROJECT STATUS

Batman has already moved beyond an early MVP.

Approximate capability status:

DOCUMENT INTELLIGENCE
~80%

Docling adopted.
Document registration and ingestion lifecycle exist.
Knowledge artifacts exist.
Text, figures and tables are represented in the knowledge architecture.

KNOWLEDGE ENGINE
~75%

Semantic chunks exist.
Embeddings exist.
Chroma vector storage exists.
Retrieval Engine exists.
Validated retrieve(question, top_k) API exists.
Basic Retrieval Validation passed 5/5 test cases.

UNDERSTANDING INTELLIGENCE
~55%

Existing modules include intent understanding, entity extraction, confidence, clarification and conversation state.

These are useful Batman assets but are not currently orchestrated cleanly.

WORKFLOW / CONVERSATION INTELLIGENCE
~20%

This is the major current architecture hole.

student_tutor.py currently contains or coordinates too much traffic logic.

Multi-turn flows and state transitions are fragile.

Example discovered bug:

Student:
"What is neuron?"

Then:
"quick quiz 2 easy"

Batman parsed the quiz topic as "Quick".

Retrieval therefore returned Reflex Arc content instead of Neuron content.

The root problem is broader than this parser bug.

Batman does not yet reliably resolve:

- current topic
- previous topic
- explicit new topic
- "same topic"
- missing topic
- follow-up references

The previous development path started patching student_tutor.py.

That approach is REJECTED.

STUDENT INTELLIGENCE
~30%

Student history exists.
Learning state exists.
Progress-related modules exist.

However, Batman does not yet have a mature Student Model or formal mastery model.

ASSESSMENT INTELLIGENCE
~10%

Existing implementation is mainly MCQ quiz-oriented.

This is NOT the intended final architecture.

Assessment must eventually support:

- MCQ
- True/False
- Match
- Fill Blank
- Short Answer
- Long Answer
- Explain Why
- Numerical
- Derivation
- Proof
- Diagram
- Graph
- Working Steps

Existing quiz modules should not be deleted yet.

Quiz should eventually become one part of Assessment Intelligence.

ADAPTIVE TEACHING INTELLIGENCE
~10%

Hints, Socratic flow, misconception handling and teaching strategy are immature.

BATMAN DECISION INTELLIGENCE
~5%

The future core Selten IP is:

"What is the next best learning action for this student?"

This Decision Intelligence does not yet exist as a mature engine.

---

## 3. CURRENT TECH STACK

Primary language:

Python 3.12

Development environment:

Windows 11
Local-first / Desktop-first
Current local repository approximately:

F:\batman_student

Knowledge / Retrieval:

Docling
ChromaDB
SentenceTransformers
all-MiniLM-L6-v2

OCR history:

Tesseract
pdf2image
Pillow

AI Providers:

OpenAI
Gemini

Existing Provider Router should remain.

OpenAI is mainly used for tutoring / explanations.

Gemini has been considered/used for vision and related capabilities.

AI providers must remain replaceable.

UI:

Streamlit

Known installed Streamlit version during development:

1.58.0

Other historical environment details:

Python 3.12.10
Tesseract 5.5.x

---

## 4. IMPORTANT REPOSITORY AREAS

The repository contains major areas including:

src/
    student_tutor.py

    understanding/
        engine.py
        conversation_state.py
        clarification_engine.py
        confidence_engine.py
        entity_extractor.py
        and related understanding modules

    retrieval/
        retrieval_engine.py
        retrieval_validator.py
        vector_retriever.py
        and related retrieval modules

    governance/
        topic_normalizer.py
        topic_map_builder.py
        structure and governance modules

    ingestion/
        document_scanner.py
        pdf_to_text.py
        and ingestion lifecycle modules

    llm/
        provider_router.py
        OpenAI provider
        Gemini provider

    quiz/
        existing quiz-related modules

    behavior/
        tutor / intent / educational behaviour modules

data/
    document_registry.json

    class10/
        subject knowledge sources and generated assets

    governance/
        ICSE/
            class10/
                subject_map.json
                physics/
                    chapter_map.json
                    topic_map.json
                    structure_rules.json
                    textbook_structure.json
                    layout_analysis.json
                    parsing_strategy.json

    students/
        student folders
        history.json
        learning_state.json
        progress.json
        schedule.json where applicable

    users/
        user folders and profile data

docs/
    architecture/
        ADR-001-Desktop-First.md
        ADR-004-Data-Governance.md
        ADR-005 / ADR-006 Understanding Engine architecture documents
        ADR-007-Knowledge-Ingestion-Lifecycle.md
        ADR-008-Knowledge-Artifact-Structure.md
        ADR-009-Semantic-Chunking-Strategy.md
        ADR-010-Embedding-Strategy.md
        ADR-011-Knowledge-Asset-Contract.md
        ADR-012-Batman-Hybrid-Educational-Intelligence-Architecture.md
        CPS-PROTOCOL.md

    governance/
        BATMAN-CONSTITUTION.md
        BACKLOG.md

    roadmap/
        ROADMAP.md
        BACKLOG.md
        KNOWN_LIMITATIONS.md
        MVP.md
        PlatformRepositoryRoadmap.md

    standards/
        coding_guidelines.md
        prompt_guidelines.md
        student_tutor_rules.md

IMPORTANT:

This folder list is contextual only.

CODEX MUST INSPECT THE ACTUAL CURRENT REPOSITORY.

Do not assume this handoff list is complete or more current than the live repo.

---

## 5. FROZEN / IMPORTANT ARCHITECTURAL DECISIONS

### ADR-001 — Desktop First

Batman is desktop/local-first during Product 1.0.

Core knowledge, student data and decision systems remain local.

Desktop First does NOT mean Desktop Only.

Future cloud/web/mobile capabilities may extend the architecture.

---

### Data Governance

One source of truth.

Knowledge must have clear ownership.

Student data, academic knowledge, governance data and understanding data are separate concerns.

---

### Knowledge Ingestion Lifecycle

Academic documents follow a lifecycle broadly based on:

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

Docling is the document parsing foundation.

Batman builds its educational knowledge contract around Docling.

Batman should NOT build its own PDF parsing engine.

---

### Understanding Engine

Batman requires a Python-first Understanding Engine.

Python owns:

- state
- workflow decisions
- validation
- governance
- routing
- memory
- business rules

LLMs assist with:

- semantic interpretation
- natural language understanding
- ambiguity assistance
- explanation generation
- educational reasoning

LLMs do not own workflow.

Conceptual pipeline:

Student
↓
Understanding
↓
Validation
↓
Memory / Context
↓
Execution
↓
Response

---

### Hybrid Educational Intelligence Architecture

ADR-012 defines Batman as a Hybrid Educational Intelligence Platform.

Architecture:

FREE / OPEN-SOURCE FOUNDATION
        ↓
BATMAN INTELLIGENCE
        ↓
SELTEN PRODUCT IP

Technology decisions:

Docling
→ ADOPT + EXTEND
→ Document Intelligence

Batman Knowledge Engine
→ KEEP + SELECTIVELY EXTEND
→ Haystack components/patterns may be evaluated only for proven retrieval gaps

Microsoft Agent Framework
→ SELECTED ARCHITECTURAL DIRECTION for workflow / conversation-state orchestration
→ adoption has NOT yet been implemented
→ existing repo must first be mapped

Batman Understanding Engine
→ KEEP / REPAIR / EXTEND
→ Batman-owned intelligence

Bayesian Knowledge Tracing / pyBKT concepts
→ ADOPT MODEL + BUILD AROUND
→ future mastery estimation

STACK or equivalent open-source symbolic assessment
→ future specialist maths/STEM assessment capability

Batman Assessment Intelligence
→ BUILD BATMAN

Batman Decision Engine
→ BUILD BATMAN
→ core future Selten IP

Batman Learned Knowledge
→ BUILD BATMAN
→ permanent structured learning

Provider Router
→ KEEP
→ AI providers remain replaceable

IMPORTANT:

Do NOT install or migrate to these frameworks simply because they are listed.

The repository must first be architecture-mapped.

---

## 6. IMPORTANT BUSINESS / PRODUCT DECISION

Batman must not waste engineering effort rebuilding solved commodity infrastructure.

The operating rule is:

ADOPT mature free/open-source foundations where appropriate.

EXTEND them.

BUILD Batman-specific educational intelligence around them.

Avoid mandatory paid platform dependencies.

Current strategic ownership boundary:

FOUNDATION MAY OWN:

- document parsing
- workflow mechanics
- checkpoint mechanics
- mastery mathematics
- symbolic mathematical evaluation
- selected retrieval utilities

BATMAN MUST OWN:

- student understanding
- curriculum governance
- topic validation
- student context fusion
- pedagogy
- assessment coordination
- adaptive learning
- next-best-learning-action
- permanent educational learning

Frameworks assist Batman.

Frameworks do not define Batman.

---

## 7. KNOWN CURRENT BUGS / OPEN ISSUES

### Workflow orchestration problem

student_tutor.py currently coordinates too much traffic.

Normal Tutor and Quiz routing have historically become mixed.

A previous CPS corrected one direct routing problem, but the broader workflow architecture remains weak.

Do NOT continue adding local if/else patches to student_tutor.py.

---

### Topic context resolution problem

Example:

Student:
"What is neuron?"

Student:
"quick quiz 2 easy"

Understanding result parsed:

topic = "Quick"

Quiz retrieval therefore queried the wrong topic and retrieved Reflex Arc content.

Batman should instead understand that the student did not provide a new academic topic.

Expected intelligent flow should be similar to:

Student asks about Neuron
↓
Current learning topic = Neuron
↓
Student asks "quick quiz 2 easy"
↓
No explicit new academic topic detected
↓
Batman identifies previous/current topic = Neuron
↓
Batman may ask:
"Continue with Neuron, or choose a new topic?"
OR resolve automatically if confidence and conversation rules permit

The exact policy should follow Batman Constitution and architecture.

A dedicated topic_validator.py does not currently appear to exist.

Do not create it blindly before architecture mapping.

---

### Conversation state

conversation_state.py exists.

It is not clear whether the current student_tutor.py uses it correctly or completely.

Inspect actual usage.

---

### Understanding assets may be disconnected

Existing modules include:

engine.py
conversation_state.py
clarification_engine.py
confidence_engine.py
entity_extractor.py
topic_normalizer.py

These were built to create general Batman intelligence.

The recent broken quiz flow suggests some of these assets may be bypassed, partially integrated or poorly orchestrated.

Inspect before changing.

---

### Legacy retrieval path

The validated retrieval API is:

retrieve(question, top_k)

from:

src/retrieval/retrieval_engine.py

Historically Batman also used:

retrieve_context(...)

from:

src/retrieval/vector_retriever.py

The architectural decision was:

Validated retrieve() should become the knowledge access point.

No parallel retrieval architecture should survive unnecessarily.

However, inspect the actual live repository before retiring vector_retriever.py because other modules may still depend on it.

---

### Python package naming collision

There is or was:

src/platform/

This collides with Python's standard library module:

platform

When src is inserted directly into sys.path, Python may import:

src/platform/__init__.py

instead of the standard Python platform module.

This caused:

AttributeError:
module 'platform' has no attribute 'python_implementation'

The safe execution command discovered was:

python -m src.student_tutor

rather than:

python src/student_tutor.py

Do NOT casually rename src/platform without a dependency and import impact analysis.

---

### Gemini provider errors

Intermittent Gemini errors have occurred:

[Gemini Error]
ClientError

Provider failure should not destroy deterministic workflow state.

Inspect provider fallback and error handling separately from workflow logic.

---

### HF Hub warning

SentenceTransformer currently produces an unauthenticated HF Hub warning.

This is not the current architecture blocker.

Do not prioritize it during architecture mapping.

---

## 8. NEXT TASK — CODEX ARCHITECTURE MAPPING

The immediate task is NOT implementation.

The immediate task is:

BATMAN ARCHITECTURE MAPPING AGAINST ADR-012

Inspect the COMPLETE LIVE REPOSITORY.

Read at minimum:

docs/governance/BATMAN-CONSTITUTION.md

docs/architecture/ADR-001-Desktop-First.md

docs/architecture/ADR-004-Data-Governance.md

docs/architecture/ADR-007-Knowledge-Ingestion-Lifecycle.md

docs/architecture/ADR-008-Knowledge-Artifact-Structure.md

docs/architecture/ADR-009-Semantic-Chunking-Strategy.md

docs/architecture/ADR-010-Embedding-Strategy.md

docs/architecture/ADR-011-Knowledge-Asset-Contract.md

docs/architecture/ADR-012-Batman-Hybrid-Educational-Intelligence-Architecture.md

docs/architecture/CPS-PROTOCOL.md

Also inspect the complete src/ tree and relevant data contracts.

Map every relevant module into exactly one primary category:

KEEP
Existing module is architecturally correct and should remain.

WRAP
Existing module is useful but should be placed behind a cleaner interface or service boundary.

MIGRATE
Existing responsibility should move gradually to the ADR-012 target architecture.

MERGE
Duplicate or overlapping responsibilities should be consolidated.

RETIRE
Module/path is obsolete or conflicts with the target architecture.

MISSING
ADR-012 requires a capability that does not currently exist.

For every module/capability report:

- file/module
- current responsibility
- actual callers/dependencies
- observed architecture issue, if any
- classification
- reason
- target owner/layer
- migration risk
- recommended migration order

Specifically trace these flows:

1. Normal tutor request

Student
→ Understanding
→ Topic/context resolution
→ Retrieval
→ Tutor behaviour
→ Provider
→ Response

2. Quiz / assessment request

Student
→ Understanding
→ Conversation context
→ Topic resolution
→ Clarification
→ Retrieval
→ Assessment
→ Answer handling
→ Next assessment item

3. Multi-turn continuation

Previous topic
→ student follow-up
→ conversation state
→ reference resolution
→ next action

4. Student intelligence

Student attempt / interaction
→ history
→ learning state
→ progress
→ weak/strong topic logic
→ adaptive revision

5. Knowledge access

Caller
→ retrieval API
→ embedding
→ vector database
→ chunk/knowledge asset

Identify all parallel, duplicate or bypass paths.

---

## 9. REQUIRED CODEX OUTPUT

Return:

A. EXECUTIVE ARCHITECTURE SUMMARY

One concise explanation of where Batman actually stands today.

B. KEEP / WRAP / MIGRATE / MERGE / RETIRE / MISSING MAP

Prefer a table.

C. CURRENT REAL EXECUTION FLOW

Based on actual code.

Do not repeat intended ADR architecture as if it already exists.

D. TOP ARCHITECTURE GAPS

Rank by impact.

E. FRAMEWORK READINESS

State whether the repo is currently ready to introduce Microsoft Agent Framework.

Answer:

READY NOW
READY AFTER PREPARATION
NOT READY

Explain why.

F. FIRST MIGRATION SLICE

Recommend the smallest safe first migration step.

The first slice must solve an architecture boundary problem.

Do not propose a broad rewrite.

G. FILES LIKELY AFFECTED BY FIRST SLICE

List them.

H. RISKS / CONTRADICTIONS

Identify conflicts between current code and frozen ADRs / Constitution.

---

## 10. THINGS CODEX MUST NOT CHANGE DURING THIS TASK

DO NOT MODIFY ANY FILE.

DO NOT WRITE CODE.

DO NOT INSTALL PACKAGES.

DO NOT ADD MICROSOFT AGENT FRAMEWORK YET.

DO NOT ADD HAYSTACK.

DO NOT ADD pyBKT.

DO NOT ADD STACK.

DO NOT REWRITE student_tutor.py.

DO NOT PATCH "Quick".

DO NOT BUILD MORE MCQ LOGIC.

DO NOT DELETE vector_retriever.py.

DO NOT RENAME src/platform.

DO NOT CHANGE DATA FILES.

DO NOT CHANGE CHROMA.

DO NOT RE-EMBED KNOWLEDGE.

DO NOT MODIFY STUDENT HISTORY.

DO NOT MODIFY LEARNING STATE.

DO NOT CREATE NEW ADRs.

DO NOT COMMIT OR PUSH.

THIS TASK IS READ-ONLY ARCHITECTURE DISCOVERY.

The live repository is the source of truth for implementation status.

The frozen Constitution and accepted ADRs are the source of truth for architectural intent.

Where code and architecture disagree, REPORT THE CONTRADICTION.

Do not silently fix it.

---

## 11. WORKING RULES

KISS protocol.

Architecture before implementation.

Inspect before recommending.

Never assume a module is unused only from its filename.

Trace imports and callers.

Never recommend deleting code without dependency evidence.

Do not confuse Quiz with Batman.

Quiz is a small subset of Assessment Intelligence.

Do not evaluate Batman only as an MCQ product.

Think Batman-wide:

Tutor
Understanding
Conversation
Knowledge
Student Intelligence
Assessment
Adaptive Teaching
Decision Intelligence

Use the actual repository as evidence.

Return the architecture map only.

No code changes.