# Batman Student — Project Analysis

---

## 1. Project Purpose

**Batman Student** (branded **"DRONA"** in the UI) is an AI-powered educational intelligence platform for **ICSE Class 10 students**, initially targeting **Physics**. It explains concepts, answers textbook questions, conducts quizzes, maintains student history, and tracks learning progress via two modes: **Learn** and **Super Chat**.

**Sources:** `src/ui/app.py:30-31`, `src/config/settings.py:42-46`, `docs/roadmap/MVP.md:1-36`, `docs/architecture/ADR-001-Desktop-First.md:11`

---

## 2. Tech Stack

| Layer | Technology | Evidence |
|---|---|---|
| **Language** | Python 3 | `requirements.txt`, `src/*.py` |
| **UI** | Streamlit 1.58.0 | `src/ui/app.py:1`, `requirements.txt` |
| **LLM Providers** | OpenAI, Gemini, DeepSeek (currently DeepSeek) | `src/llm/provider_router.py:1-42`, `src/config/settings.py:21` |
| **Vector DB** | ChromaDB 1.5.9 | `requirements.txt`, `src/retrieval/chroma_search.py` |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) | `requirements.txt`, `src/config/settings.py:35` |
| **Auth** | Google OAuth via `streamlit-oauth` | `requirements.txt`, `src/config/settings.py:52-58` |
| **OCR** | pytesseract, pdf2image, pypdf, pillow | `requirements.txt`, `src/ingestion/` |
| **Cloud** | Supabase (not yet used) | `supabase/` (empty), `requirements.txt` |

---

## 3. Folder Structure

```
batman_student/
├── .devcontainer/          # Dev container config
├── data/                   # Runtime data (document registry, student history)
├── docs/
│   ├── architecture/       # ADRs (Desktop First, Embedding Strategy, etc.)
│   ├── decisions/          # Project context documents
│   ├── governance/         # BATMAN-CONSTITUTION.md
│   ├── roadmap/            # MVP, BACKLOG, KNOWN_LIMITATIONS
│   └── standards/          # Coding/prompt guidelines
├── secrets/                # Credential files
├── src/
│   ├── __init__.py
│   ├── batman_engine.py    # Core engine
│   ├── student_tutor.py    # CLI/console tutor entry point
│   ├── learn_manager.py    # Subject/workspace definitions
│   ├── knowledge_validation.py
│   ├── question_bank.py
│   ├── question_extractor.py
│   ├── runtime_error_boundary.py
│   ├── behavior/           # Intent classifier, concept teacher, homework guide, study coach, quiz master, router
│   ├── config/             # paths.py, settings.py, pilot_documents.py
│   ├── conversation/       # conversation_manager.py, pending_action_manager.py
│   ├── embedding/          # embedding_builder.py, vector_db_builder.py
│   ├── governance/         # learning_state, topic_normalizer, progress_tracker, etc.
│   ├── ingestion/          # OCR, PDF extraction, chunking, pipeline
│   ├── knowledge/          # knowledge_repository.py, knowledge_asset_builder.py, document_adapter.py
│   ├── llm/                # Provider implementations: openai, gemini, deepseek, claude, local; router
│   ├── orchestration/      # quiz_router.py, tutor_router.py
│   ├── platform/           # __init__.py
│   ├── quiz/               # quiz_parser.py, quiz_generator.py, quiz_manager.py
│   ├── retrieval/          # chroma_search.py, embeddings.py, retrieval_engine.py, router, validator, vector_retriever, knowledge_provider
│   ├── tests/              # ~30 test files
│   ├── understanding/      # intent_engine, learning_engine, confidence_engine, etc.
│   └── ui/                 # app.py (Streamlit), components.py, styles.css, assets/
├── supabase/               # Empty (future cloud sync)
├── vector_db/              # Local vector store
├── vector_db_bad/          # Disused vector store
└── requirements.txt
```

---

## 4. Entry Point

**Primary (UI):** `src/ui/app.py` — a Streamlit application that imports and calls `src.batman_engine.ask_batman`.

**Secondary (CLI):** `src/student_tutor.py` — a standalone Python script with its own REPL loop. `src/batman_engine.py` is a module library, not directly runnable.

**Evidence:** `src/ui/app.py:12`, `src/student_tutor.py:1-50`, `src/batman_engine.py:1`

---

## 5. Current Implementation Status

**Active development — pre-1.0.** The project has:

- A **working MVP** targeting ICSE Class 10 Physics
- Multiple **completed subsystems**: LLM provider router (OpenAI/Gemini/DeepSeek), ChromaDB vector retrieval, intent classification, quiz generation/management, conversation history, OCR ingestion pipeline, embedding builder, and a Streamlit UI with Google OAuth
- **30+ test files** covering core components (`src/tests/`)
- **Known limitations**: single-user local deployment, no centralized database, Streamlit UI quirks
- The project is **Desktop-First** with cloud features (Supabase) deferred
- Currently configured to use **DeepSeek** as the LLM provider (`src/config/settings.py:21`)

---

## 6. Architecture (from implementation code)

### Main Modules

| Module | Path | Role |
|---|---|---|
| **Engine** | `src/batman_engine.py:1-661` | Core `ask_batman()` — orchestrates intent, skill, retrieval, prompt-building, LLM call, history, pending actions |
| **CLI Tutor** | `src/student_tutor.py:1-1075` | Standalone REPL — uses `src/understanding/engine.py`, `src/orchestration/*`, `src/llm/provider_router.py` instead of direct OpenAI calls |
| **UI** | `src/ui/app.py:1-438` | Streamlit app — imports `batman_engine.ask_batman`, hardcodes student "STD001" |
| **Behavior** | `src/behavior/` | Intent classifier (`intent_classifier.py:1-55` uses LLM to classify), skill router (`batman_router.py:1-34`), role prompts (`concept_teacher.py:1-9`, `homework_guide.py:1-10`, `study_coach.py:1-8`, `solved_example.py:1-21`) |
| **Understanding** | `src/understanding/` | `engine.py:1-163` orchestrates 5 steps: intent (`intent_engine.py:1-172`, Python regex, no LLM), entities (`entity_extractor.py:1-240`, regex), confidence (`confidence_engine.py:1-167`), clarification (`clarification_engine.py:1-108`), learning (`learning_engine.py:1-90`, stub) |
| **LLM** | `src/llm/` | `provider_router.py:1-42` dispatches based on `LLM_PROVIDER` setting to `openai_provider.py:1-29` (gpt-5.5), `deepseek_provider.py:1-74` (deepseek-v4-flash), `gemini_provider.py:1-29` (gemini-2.5-flash) |
| **Retrieval** | `src/retrieval/` | `knowledge_provider.py:1-52` (ChromaDB `./vector_db`, collection `icse_class10`), `retrieval_engine.py:1-256` (sentence-transformers all-MiniLM-L6-v2 + ChromaDB), `retrieval_router.py:1-6` (skips retrieval only for `STUDY_PLAN`), `vector_retriever.py:1-243` (alternative retrieval service) |
| **Quiz** | `src/quiz/` | `quiz_manager.py:1-190` in-memory state machine, `quiz_generator.py:1-120` (LLM prompt for MCQ generation), `quiz_parser.py:1-88` (regex parse of "quiz" commands) |
| **Conversation** | `src/conversation/` | `conversation_manager.py:1-119` (JSON file persistence per student), `pending_action_manager.py:1-489` (regex + keyword resolution of follow-up offers) |
| **Governance** | `src/governance/` | `learning_state.py:1-204` (JSON persistence per student), `topic_normalizer.py:1-266` (regex cleanup), 16 other files |
| **Ingestion** | `src/ingestion/` | OCR pipeline (`pdf_to_text.py`, `clean_text.py`, `chunk_builder.py`, `chunk_text.py`, `docling_extractor.py`, `create_vector_db.py`) |
| **Knowledge** | `src/knowledge/` | `knowledge_repository.py:1-149` (loads document.json, chunks.json, figure_manifest.json, manifest.json) |
| **Embedding** | `src/embedding/` | `embedding_builder.py:1-105`, `vector_db_builder.py:1-138` (SentenceTransformer → ChromaDB) |
| **Orchestration** | `src/orchestration/` | `tutor_router.py:1-89` (routes QUIZ vs TUTOR), `quiz_router.py:1-127` (MCQ display/parse) |
| **Runtime Safety** | `src/runtime_error_boundary.py:1-130` | `sys.excepthook` replacement — logs to file, shows student-safe message |

### Data Flow

```
INPUT (question string)
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. Pending Action Check          (pending_action_manager.py)    │
│    └─ structured dict? → resolve pending action (ACCEPT/REJECT) │
│    └─ quiz active? → check_answer(), build next question        │
│    └─ starts with "quiz"? → parse_quiz_request(), start_quiz()  │
│    └─ normal question → continues                               │
├─────────────────────────────────────────────────────────────────┤
│ 2. Intent Classification                                         │
│    └─ student_tutor.py:   understanding.engine.understand()      │
│       (intent regex, entity regex, confidence, clarification)    │
│    └─ batman_engine.py:   classify_intent() via LLM              │
├─────────────────────────────────────────────────────────────────┤
│ 3. Skill Selection        (batman_router.py / intent→skill map)  │
├─────────────────────────────────────────────────────────────────┤
│ 4. Retrieval Decision     (retrieval_router.should_retrieve())   │
│    └─ if yes: query ChromaDB collection with question text       │
├─────────────────────────────────────────────────────────────────┤
│ 5. Prompt Assembly                                              │
│    behavior_prompt + rules + history + context + question        │
├─────────────────────────────────────────────────────────────────┤
│ 6. LLM Call                                                     │
│    └─ batman_engine.py:   OpenAI client directly (gpt-5.5)       │
│    └─ student_tutor.py:   ask_llm() → provider_router            │
│                           → deepseek/openai/gemini               │
├─────────────────────────────────────────────────────────────────┤
│ 7. Post-processing                                               │
│    └─ append to history (JSON file per student)                  │
│    └─ remember_pending_action() → scan for "would you like..."   │
│    └─ return answer string                                       │
└─────────────────────────────────────────────────────────────────┘
```

### LLM Integration

**Provider Router** (`src/llm/provider_router.py:1-42`):

```
ask_llm(prompt) → dispatches to:
  ├─ deepseek_provider:  OpenAI-compatible client → api.deepseek.com, model "deepseek-v4-flash"
  ├─ openai_provider:    OpenAI client, model "gpt-5.5"
  └─ gemini_provider:    google.genai client, model "gemini-2.5-flash"
```

**Direct OpenAI call** in `batman_engine.py:56-58, 634-637` — uses `client.responses.create(model="gpt-5.5")` bypassing the provider router.

**LLM used for:** intent classification (`intent_classifier.py:1-55`), MCQ generation (`quiz_generator.py:1-120`), and all tutor/teaching responses.

### Control Flow — Two Separate Execution Paths

1. **`batman_engine.ask_batman()`** (`src/batman_engine.py:217-661`) — used by Streamlit UI (`src/ui/app.py:12`). Single function: takes `(student_id, question)`, returns answer string. Contains its own intent classification, direct OpenAI API call, quiz logic, history management. Does NOT use `provider_router`.

2. **`student_tutor.py`** (`src/student_tutor.py:204-1075`) — CLI REPL. Uses the full Understanding Engine pipeline, `provider_router.ask_llm()`, orchestration routers, governance learning state, question bank persistence. More feature-complete than `batman_engine.py`.

---

## 7. Execution Path: Streamlit UI → First LLM API Call

### Step 1: Streamlit UI — `src/ui/app.py`

**WORKSPACE page** (user types a question in the Physics chat):

```python
full_question = f"{st.session_state.subject}: {question}"   # e.g. "Physics: What is force?"
answer = ask_batman("STD001", full_question)                   # app.py:385-388
```

**SUPER_CHAT page** (generic chat without subject prefix):

```python
answer = ask_batman("STD001", question)  # app.py:426-428
```

`ask_batman` is imported from `src.batman_engine` (`app.py:12`).

---

### Step 2: `ask_batman(student_id, question)` — `src/batman_engine.py:217-661`

**2a. Load conversation history** (`batman_engine.py:222-224`)

```python
history = load_history(student_id)
```

This calls `conversation_manager.load_history()` (`conversation_manager.py:25-67`):

- Resolves path `data/students/{student_id}/history.json` (`conversation_manager.py:9-22`)
- If file doesn't exist, writes `[]` to it and returns `[]`
- Otherwise reads and returns JSON, backfilling `mode`/`subject` fields for backward compat

**2b. Gate checks** (all return early without LLM call):

| Check | Lines | Condition |
|---|---|---|
| Pending action dict | 226-350 | `isinstance(question, dict)` → resolve via `pending_action_manager.resolve_pending_action_response()` |
| Quiz active | 356-419 | `is_quiz_active()` → check answer, build next question |
| Quiz start | 425-469 | `question.lower().startswith("quiz")` → `parse_quiz_request()`, `start_quiz()` |

**2c. Workspace mode**: subject prefix `"Physics:"` is stripped to determine `mode="LEARN"` and `subject="Physics"` (`batman_engine.py:478-498`).

**Super Chat mode**: no colon → `mode="SUPER_CHAT"`, `subject=""`.

**2d. Append user message to in-memory history** (`batman_engine.py:500-507`).

---

### Step 3: Intent Classification — `src/behavior/intent_classifier.py`

```python
intent = classify_intent(question)  # batman_engine.py:513-515
```

This calls `intent_classifier.classify_intent(question)` (`intent_classifier.py:4-55`):

- Builds a prompt instructing the LLM to return one of `LEARN / SUPER_CHAT / QUIZ / HOMEWORK / SOLVED_EXAMPLE / STUDY_PLAN`
- Calls `ask_llm(prompt)` — **this is the first LLM API call**
- Strips and uppercases the response

---

### Step 4: `ask_llm(prompt)` — `src/llm/provider_router.py:17-38`

```python
def ask_llm(prompt):
    if LLM_PROVIDER == "gemini":
        response = gemini_response(prompt)
    elif LLM_PROVIDER == "deepseek":
        response = deepseek_response(prompt)
    else:
        response = openai_response(prompt)
```

`LLM_PROVIDER` is imported from `src.config.settings` (`settings.py:21`):

```python
LLM_PROVIDER = "deepseek"  # settings.py:21
```

Since `LLM_PROVIDER == "deepseek"`, the router calls `deepseek_provider.generate_response(prompt)`.

---

### Step 5: `deepseek_provider.generate_response(prompt)` — `src/llm/deepseek_provider.py:37-57`

```python
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def generate_response(prompt):
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

This sends an HTTP POST to `https://api.deepseek.com/v1/chat/completions` with the intent-classification prompt. This is the **actual first LLM API call** over the network.

---

### Alternative paths (if `LLM_PROVIDER` were different):

- **OpenAI**: `openai_provider.generate_response()` → `client.responses.create(model="gpt-5.5", input=prompt)` at `openai_provider.py:17-20`
- **Gemini**: `gemini_provider.generate_response()` → `client.models.generate_content(model="gemini-2.5-flash", contents=prompt)` at `gemini_provider.py:17-20`

---

### Complete Call Chain

```
src/ui/app.py:385-388 (or 426-428)
  └─ ask_batman("STD001", question)
       └─ src/batman_engine.py:217
            ├─ conversation_manager.load_history()     → src/conversation/conversation_manager.py:25
            │    └─ reads data/students/STD001/history.json
            ├─ [gate checks: pending action, quiz, etc.]
            ├─ intent = classify_intent(question)       → src/behavior/intent_classifier.py:4
            │    └─ ask_llm(prompt)                    → src/llm/provider_router.py:17
            │         └─ LLM_PROVIDER check             → src/config/settings.py:21
            │              └─ deepseek_provider.generate_response()  → src/llm/deepseek_provider.py:37
            │                   └─ client.chat.completions.create(model="deepseek-v4-flash")
            │                        ▲ FIRST LLM API CALL (HTTP POST to api.deepseek.com)
            └─ ...
```

**Files read:** `src/ui/app.py`, `src/batman_engine.py`, `src/conversation/conversation_manager.py`, `src/config/paths.py`, `src/behavior/intent_classifier.py`, `src/llm/provider_router.py`, `src/config/settings.py`, `src/llm/deepseek_provider.py`, `src/llm/openai_provider.py`, `src/llm/gemini_provider.py`, `src/behavior/batman_router.py`, `src/retrieval/retrieval_router.py`, `src/behavior/concept_teacher.py`, `src/behavior/homework_guide.py`, `src/behavior/study_coach.py`, `src/behavior/solved_example.py`, `src/retrieval/knowledge_provider.py`, `src/quiz/quiz_parser.py`, `src/quiz/quiz_manager.py`, `src/conversation/pending_action_manager.py`
