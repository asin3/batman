# Architecture Review
## CPS-002: DRONA Application & Experience Unification

**Date:** 2026-07-20
**Time:** 17:15 IST
**Author:** Orion (HULK Coding Agent)
**Repository:** batman_student
**Branch:** develop

---

## 1. Current Architecture

### Two Independent Applications

The repository currently contains two independent Streamlit applications:

| Aspect | DRONA | Batman DD |
|--------|-------|-----------|
| **Entry point** | `src/ui/app.py` | `src/batman_dd/app.py` |
| **Port** | 8501 (default) | 8501 (default) — cannot run simultaneously without port conflict |
| **Auth** | `auth_gate.authenticate()` | `auth_gate.authenticate()` |
| **Session** | Independent `st.session_state` | Independent `st.session_state` |
| **Shell** | Own sidebar, header, CSS | Own sidebar, header, footer, CSS |
| **Brand** | "🎓 DRONA — Learn. Think. Understand." | "🦇 BATMAN-DD — Daily Discipline" |
| **Pages** | Home, Workspace (per-subject), Super Chat | Progress, Scheduling, Daily Debrief, Quick Notes |
| **Navigation** | Sidebar buttons + external link to DD | Sidebar buttons |

### DRONA Page Structure (`src/ui/app.py`)

- **HOME** — Welcome Back cards (Continue Learning, Announcements, Latest Discussion, Schedule)
- **WORKSPACE** — Per-subject chat with topic strip, Pending Action (Biology only)
- **SUPER_CHAT** — Open-domain chat
- Sidebar: Home, Learn (4 subjects), Super Chat, Quiz (Coming Soon), **My Plan & Progress** (external link to `localhost:8501`), user name, Logout

### Batman DD Page Structure (`src/batman_dd/app.py`)

- **Progress** — Curriculum tree with per-topic status tracking (subject tabs, chapters, topics with completion states)
- **Scheduling** — Monthly calendar planner with per-day subject scheduling
- **Daily Debrief** — Stub (title only)
- **Quick Notes** — Notes CRUD with save/delete
- Sidebar: 4 page buttons, student name, Logout

### Shared Platform Layer

- `src/platform/auth/auth_gate.py` — Shared `authenticate()` and `logout()`
- `src/platform/services/` — User service, authorization
- `src/conversation/` — Conversation management

### CPS-001 Legacy

"My Plan & Progress" in DRONA opens `http://localhost:8501` in a new tab, launching Batman DD as an independent app requiring separate authentication. This was the intentional CPS-001 design with deferred unification.

---

## 2. Business Objective

**Product Owner requirement:** DRONA shall operate as a single application.

The user shall never perceive historical application boundaries.

Key decisions from Product Owner:
- Multiple application launches create unnecessary complexity
- Separate Google authentication flows reduce usability
- User experience should present a single DRONA application

---

## 3. Proposed Workspace Architecture

### Principle

A single Streamlit application hosts multiple Workspaces. Each Workspace is an isolated feature area with its own content, and optionally its own secondary navigation. All Workspaces share a common application shell.

### Application Shell (Shared)

| Component | Description |
|-----------|-------------|
| `st.set_page_config` | Single page config: title "DRONA", icon "🎓" |
| Authentication | Single `authenticate()` call at module scope — one session |
| Sidebar | Primary navigation listing all Workspaces |
| Header | Shared branding ("🎓 DRONA") |
| Visual brand | DRONA shell (header, sidebar, navigation, typography, spacing, primary colors) visually consistent across all workspaces; workspace-specific components may retain their own styling |

### Workspaces

| Workspace | Source | Secondary Nav | Description |
|-----------|--------|---------------|-------------|
| **Home** | DRONA (existing) | No | Welcome dashboard with cards |
| **Learn** | DRONA (existing) | No | Per-subject chat with topic strip |
| **Super Chat** | DRONA (existing) | No | Open-domain chat |
| **Progress** | Batman DD → migrated | Yes (subject tabs) | Curriculum tree, topic tracking — replaces "My Plan & Progress" |
| **Schedule** | Batman DD → migrated | No | Monthly calendar planner |
| **Debrief** | Batman DD → migrated | No | Daily reflection (stub → implement) |
| **Notes** | Batman DD → migrated | No | Quick Notes CRUD |
| **Quiz** | DRONA (placeholder) | No | Currently "Coming Soon" — retained as placeholder |

### Navigation Model

```
Primary (Sidebar)
├── 🏠 Home
├── 📚 Learn
│   ├── Physics
│   ├── Chemistry
│   ├── Maths
│   └── Biology
├── 💬 Super Chat
├── 📈 Progress          ← migrated from Batman DD
├── 📅 Schedule           ← migrated from Batman DD
├── 📝 Daily Debrief      ← migrated from Batman DD
├── 📒 Quick Notes        ← migrated from Batman DD
├── 📝 Quiz (Coming Soon)
└── [user name]
    └── 🚪 Logout
```

Secondary navigation (within Workspace):
- **Progress**: Subject tabs (Physics, Chemistry, Biology, Maths) — already exists in Batman DD
- **Learn**: Subject buttons in sidebar — already exists

### Session Model

Single `st.session_state` shared by all Workspaces:
- `user` — Authenticated user object
- `student_id` — Student identity
- `page` — Current workspace/page
- Per-workspace state (e.g., `learn_messages`, `superchat_messages`) kept as session keys

---

## 4. Impact Analysis

### Files to Keep (No Change)

| File | Reason |
|------|--------|
| `src/platform/auth/auth_gate.py` | Shared authentication — works as-is |
| `src/ui/components.py` | DRONA UI components — reusable |
| `src/batman_dd/core/services/` | Batman DD business logic (progress, scheduling, notes services) — reusable |
| `src/batman_dd/components.py` | UI components — reusable (subject tabs, topic rows, calendar, etc.) |
| `src/batman_dd/pages/progress.py` | Progress page logic — reusable as workspace |
| `src/batman_dd/pages/scheduling.py` | Scheduling page logic — reusable as workspace |
| `src/batman_dd/pages/debrief.py` | Debrief stub — placeholder for implementation |
| `src/batman_dd/pages/notes.py` | Notes page logic — reusable as workspace |
| `src/config/settings.py` | Configuration — no change |
| `data/` | Student data — no change |

### Files to Modify

| File | Change |
|------|--------|
| `src/ui/app.py` | Import Batman DD page renderers, add new workspaces to navigation, remove external DD link |
| `.gitignore` | No change expected |

### Files to Remove / Supersede

| File | Reason |
|------|--------|
| `src/batman_dd/app.py` | No longer needed — Batman DD ceases as independent app |
| `src/batman_dd/styles.css` | No longer loaded by DRONA — shell uses DRONA's existing CSS; workspace-specific DD components retain their own styling |
| `src/ui/app.py` line 224 | External `href="http://localhost:8501"` link removed |

### Files to Create

| File | Purpose |
|------|---------|
| (None) | Complete CSS consolidation deferred to future CPS |

### Authentication Impact

**Critical improvement:** Single authentication call → single `st.session_state` → no re-authentication required. The CPS-001 engineering investigation identified independent sessions as the root cause of the UAT observation. CPS-002 eliminates this by design.

### Configuration Impact

`src/config/settings.py:54` — `GOOGLE_REDIRECT_URI = "http://localhost:8501"` remains valid as only one app runs on port 8501.

---

## 5. Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|------------|--------|------------|
| 1 | Workspace state collisions in shared `st.session_state` | Medium | Medium | Use prefixed keys per workspace (e.g., `learn_messages`, `progress_subject`, `schedule_month`) |
| 2 | Batman DD page imports break if moved | Low | High | Import pages as modules from their existing locations; do not relocate files in CPS-002 |
| 3 | CSS conflicts between DRONA and Batman DD styles | Medium | Low | DRONA shell CSS takes precedence; workspace-specific components retain existing DD styling — no merge required in CPS-002 |
| 4 | Learn workspace subject navigation duplicated | Low | Low | Sidebar already has subject buttons; Progress workspace has its own subject tabs — no conflict |
| 5 | Regression in existing DRONA features | Low | High | Manual UAT after merge; existing tests cover core paths |
| 6 | Progress page hardcoded to `/data/class10` | Low | Medium | Existing design — acceptable for current product stage |

---

## 6. Alternatives Considered

### Alternative A: Keep Two Apps, Improve Navigation (Rejected)

Keep DRONA and Batman DD as separate apps but improve the linking UX (e.g., auto-launch DD, shared OAuth token).

**Rejected because:**
- Does not address Product Owner's primary complaint: "multiple application launches create unnecessary complexity"
- Shared OAuth across Streamlit processes is technically complex
- User would still perceive application boundaries

### Alternative B: Micro-Frontend Architecture (Rejected)

Implement each workspace as an independently deployable Streamlit app with an app shell that composites them.

**Rejected because:**
- Violates Constitution Principle 9 (Simple before complex) and Principle 10 (simplest correct implementation)
- Streamlit does not natively support micro-frontends
- Adds infrastructure complexity with no product benefit at current stage

### Alternative C: Streamlit Pages (Recommended)

Streamlit natively supports multi-page apps via `st.navigation` and `st.Page` (introduced in Streamlit 1.36+). However, this requires restructuring into Streamlit's `pages/` convention.

**Not recommended because:**
- Would require relocating all page modules
- Loses flexibility in navigation layout
- Strongly coupled to Streamlit's page discovery mechanism
- Current architecture (manual page routing via `st.session_state.page`) is simpler and more maintainable

### Alternative D (Recommended): Unified DRONA with Workspace Architecture

One `app.py`, one `authenticate()` call, manual page routing (as currently used in both apps), with Batman DD pages imported as modules.

**Selected because:**
- Minimal code change — DRONA already routes by `st.session_state.page`
- Batman DD pages are already modular (standalone render functions)
- One authentication call solves the CPS-001 UAT finding
- Preserves existing directory structure
- No framework lock-in

---

## 7. Recommendation

**Adopt Alternative D: Unified DRONA with Workspace Architecture.**

### Summary of Changes

| # | Action | Detail |
|---|--------|--------|
| 1 | Import Batman DD page renderers in `src/ui/app.py` | Add imports for `render_progress_page`, `render_scheduling_page`, `render_debrief_page`, `render_notes_page` |
| 2 | Extend page routing | Add cases for `"PROGRESS"`, `"SCHEDULE"`, `"DEBRIEF"`, `"NOTES"` |
| 3 | Update sidebar navigation | Replace external "My Plan & Progress" link with internal `st.session_state.page = "PROGRESS"` button; add Schedule, Debrief, Notes buttons |
| 4 | Remove external DD launch URL | Delete `href="http://localhost:8501"` inline HTML |
| 5 | Keep Batman DD module directory intact | Pages remain at `src/batman_dd/pages/` — no file relocation |
| 6 | Retain existing session key conventions | All existing `st.session_state` keys preserved; new keys added for new workspaces |

### What Does NOT Change

- Authentication module (`auth_gate.py`)
- Business logic services (`student_progress_service.py`, etc.)
- Data directory structure
- Application entry point (`src/ui/app.py`)
- Streamlit configuration
- CPS-001 implementation (auth, student identity, migration)

### Benefits

- Single authentication session resolves CPS-001 UAT finding
- Perceived as one application by the user
- Minimal code changes — leverages existing modular Batman DD pages
- No file relocation — all existing imports continue working
- All existing DRONA features remain unchanged
- Batman DD directory can be removed in a future CPS when convenient

---

## 8. Architecture Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | **Single Streamlit app.** DRONA becomes the sole entry point. | Meets Product Owner requirement. Eliminates independent authentication. |
| 2 | **Manual page routing preserved.** `st.session_state.page` continues as the routing mechanism. | Already proven in both apps. No framework dependency. |
| 3 | **Batman DD pages imported as modules.** No file relocation. | Zero refactoring risk. All existing imports continue to work. |
| 4 | **Batman DD app entry point deprecated.** `src/batman_dd/app.py` is not deleted but becomes unused. | Preserves history. Cleanup deferred. |
| 5 | **"My Plan & Progress" renamed to "Progress".** Internal navigation replaces external link. | Aligns with Product Owner terminology. Eliminates multi-app UX. |
| 6 | **Pre-existing session keys unchanged.** New keys follow the same convention. | Preserves CPS-001 session logic. No migration needed. |
| 7 | **Visual Shell Consistency.** The DRONA application shell (header, sidebar, branding, navigation, typography, spacing and primary colors) shall remain visually consistent across all workspaces. Workspace-specific components may retain their existing styling where appropriate. A complete CSS consolidation is intentionally deferred to a future CPS. | Satisfies Product Owner requirement of a single-application perception. Workspace-specific component styling retains existing investment. Deferred full consolidation balances scope with architectural goals. |

---

## Architecture Status

Architecture Stable? YES
Implementation Ready? YES (CPS-002 — conditionally)
Overall Risk: LOW
Outstanding Questions: None — Architecture Decisions defined
Recommendation: **Proceed to CPS-002 preparation**
Reviewer Confidence: High
