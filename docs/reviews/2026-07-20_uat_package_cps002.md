# Product Owner UAT Package
## CPS-002: DRONA Application & Experience Unification

**Date:** 2026-07-20
**Branch:** `orion/CPS-002-drona-workspace-unification`

---

## 1. Scope under Test

CPS-002 unifies the previously independent DRONA and Batman DD applications into a single DRONA application. All Batman DD workspaces (Progress, Schedule, Daily Debrief, Quick Notes) are accessible from the DRONA sidebar as internal pages. Batman DD is deprecated as a standalone application.

| # | Item | Scope |
|---|------|-------|
| 1 | Single application entry point (`streamlit run src/ui/app.py`) | All workspaces accessible from one launch |
| 2 | DRONA sidebar navigation includes all workspaces | Home, Learn (4 subjects), Super Chat, Progress, Schedule, Daily Debrief, Quick Notes, Quiz placeholder |
| 3 | Progress workspace renders curriculum tracker | Subject tabs, chapters, topic rows, completion states |
| 4 | Schedule workspace renders monthly planner | Calendar grid, day cards, subject assignments |
| 5 | Daily Debrief workspace renders | Debrief page content |
| 6 | Quick Notes workspace renders | Notes list, editor, save, delete |
| 7 | Single authentication session across all workspaces | No re-authentication when navigating between workspaces |
| 8 | No external "My Plan & Progress" link remains | External `localhost:8501` link removed from sidebar |
| 9 | Batman DD no longer required as independent application | `streamlit run src/batman_dd/app.py` is never needed |

## 2. Features Implemented

| # | Feature | Source | Description |
|---|---------|--------|-------------|
| 1 | Workspace imports | `src/ui/app.py` | Four Batman DD page renderers imported: `render_progress_page`, `render_scheduling_page`, `render_debrief_page`, `render_notes_page` |
| 2 | Extended page routing | `src/ui/app.py` | Four new routing cases: `PROGRESS`, `SCHEDULE`, `DEBRIEF`, `NOTES` |
| 3 | Sidebar navigation update | `src/ui/app.py` | Replaced external "My Plan & Progress" HTML link with internal `st.button()` navigation; added Schedule, Daily Debrief, Quick Notes buttons |
| 4 | External link removal | `src/ui/app.py` | `href="http://localhost:8501" target="_blank"` inline HTML deleted |
| 5 | Batman DD deprecation | `src/batman_dd/app.py` | Deprecation comment added to header |
| 6 | DRONA shell consistency | `src/ui/app.py` | All workspaces render within DRONA's existing `st.set_page_config`, sidebar, header, and branding |
| 7 | Session state preservation | `src/ui/app.py` | All existing DRONA session keys (`learn_messages`, `superchat_messages`, `page`, `subject`, `student_id`) continue working unchanged |

## 3. Preconditions

| # | Check | Instruction |
|---|-------|-------------|
| 1 | Branch checkout | `git fetch origin && git checkout orion/CPS-002-drona-workspace-unification` |
| 2 | Python environment | Python 3.x with all dependencies installed (`pip install -r requirements.txt`) |
| 3 | Google OAuth credentials | `secrets/google_oauth.json` configured for local execution |
| 4 | Student data | `data/students/` contains the existing student profile mapped to the test Google account |
| 5 | No other Streamlit app running | Ensure no other process occupies port 8501 |
| 6 | Browser | Modern browser (Chrome, Firefox, Edge) with Google account session available |
| 7 | Environment Certification | Phase 0 Environment Certification must be completed and PASS before executing UAT tests |

## 4. Test Environment

| Component | Specification |
|-----------|---------------|
| Entry point | `streamlit run src/ui/app.py` (port 8501) |
| Authentication | Google OAuth via `auth_gate.authenticate()` |
| Storage | Local filesystem (`data/students/`) |
| Python version | 3.x |
| Dependencies | Per `requirements.txt` |
| Workspace import paths | `src/batman_dd/pages/` (unchanged) |
| Batman DD standalone | Deprecated — not required for any test |

## 5. Product Owner Test Cases

### T-1: Application Launches as Single Entry Point

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1.1 | Run `streamlit run src/ui/app.py` | Application starts on `http://localhost:8501` |
| 1.2 | Observe the browser tab | Single application loads — no new tab or second app launch |

### T-2: Authentication Required

| Step | Action | Expected Result |
|------|--------|-----------------|
| 2.1 | Navigate to `http://localhost:8501` | "Continue with Google" button appears |
| 2.2 | Click "Continue with Google" | Google OAuth consent screen appears |
| 2.3 | Select a Google account | DRONA home page loads with sidebar navigation |

### T-3: All Workspaces Accessible from Sidebar

| Step | Action | Expected Result |
|------|--------|-----------------|
| 3.1 | After login, observe sidebar | Sidebar lists: 🏠 Home, 📚 Learn (Physics, Chemistry, Maths, Biology), 💬 Super Chat, divider, 📈 Progress, 📅 Schedule, 📝 Daily Debrief, 📒 Quick Notes, divider, 📝 Quiz (Coming Soon), divider, [user name], 🚪 Logout |
| 3.2 | Click each workspace button | Each click navigates to the corresponding workspace without errors |

### T-4: Progress Workspace

| Step | Action | Expected Result |
|------|--------|-----------------|
| 4.1 | Click "📈 Progress" in sidebar | Progress workspace renders with subject tabs (Physics, Chemistry, Biology, Maths) |
| 4.2 | Click each subject tab | Curriculum tree displays chapters and topic rows with completion states for each subject |
| 4.3 | Verify topic completion status | Topics show correct completion state (completed / in progress / not started) |

### T-5: Schedule Workspace

| Step | Action | Expected Result |
|------|--------|-----------------|
| 5.1 | Click "📅 Schedule" in sidebar | Schedule workspace renders with monthly calendar grid |
| 5.2 | Observe day cards | Each day card displays subject assignments if scheduled |
| 5.3 | Navigate months | Calendar updates to show different months |

### T-6: Daily Debrief Workspace

| Step | Action | Expected Result |
|------|--------|-----------------|
| 6.1 | Click "📝 Daily Debrief" in sidebar | Daily Debrief workspace renders (stub or content) |
| 6.2 | Verify no application errors | Page loads without Streamlit errors |

### T-7: Quick Notes Workspace

| Step | Action | Expected Result |
|------|--------|-----------------|
| 7.1 | Click "📒 Quick Notes" in sidebar | Quick Notes workspace renders with notes list |
| 7.2 | Create a new note | Note is saved and appears in the list |
| 7.3 | Delete a note | Note is removed from the list |
| 7.4 | Verify persistence after page navigation | Navigate to another workspace and back — notes list persists |

### T-8: Single Authentication Session

| Step | Action | Expected Result |
|------|--------|-----------------|
| 8.1 | Authenticate once via Google OAuth | User is logged in to DRONA |
| 8.2 | Navigate to Progress workspace | Content renders — no re-authentication prompt |
| 8.3 | Navigate to Schedule workspace | Content renders — no re-authentication prompt |
| 8.4 | Navigate to Daily Debrief workspace | Content renders — no re-authentication prompt |
| 8.5 | Navigate to Quick Notes workspace | Content renders — no re-authentication prompt |
| 8.6 | Navigate back to Home | Home renders — session remains active |

### T-9: No External Link to Batman DD

| Step | Action | Expected Result |
|------|--------|-----------------|
| 9.1 | Inspect DRONA sidebar | No "My Plan & Progress" button exists |
| 9.2 | Inspect sidebar for external links | No `href` target `_blank` links to `localhost:8501` |
| 9.3 | Verify "Progress" is an internal button | Clicking "📈 Progress" navigates within DRONA — does not open a new tab |

### T-10: Logout

| Step | Action | Expected Result |
|------|--------|-----------------|
| 10.1 | While logged in, click "🚪 Logout" in sidebar | Session is cleared |
| 10.2 | Page refreshes | "Continue with Google" login screen appears |
| 10.3 | Verify no protected content visible | DRONA workspace content is not rendered before re-authentication |

### T-11: Existing DRONA Workspaces Unchanged (Regression)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 11.1 | After login, click "🏠 Home" | Home page renders with "Welcome Back" cards (Continue Learning, Announcements, Latest Discussion, Schedule) |
| 11.2 | Click "📚 Learn → Physics" | Physics workspace loads with chat interface, topic strip, and conversation history |
| 11.3 | Click "📚 Learn → Chemistry" | Chemistry workspace loads with chat interface |
| 11.4 | Click "📚 Learn → Maths" | Maths workspace loads with chat interface |
| 11.5 | Click "📚 Learn → Biology" | Biology workspace loads with chat interface and Pending Action |
| 11.6 | Click "💬 Super Chat" | Super Chat loads with open-domain chat |
| 11.7 | Click "📝 Quiz (Coming Soon)" | Quiz placeholder renders (non-functional) |

### T-12: Visual Shell Consistency

| Step | Action | Expected Result |
|------|--------|-----------------|
| 12.1 | Navigate to each workspace (Home, Learn, Super Chat, Progress, Schedule, Debrief, Notes) | DRONA header, sidebar, and branding ("🎓 DRONA") are consistent across all workspaces |
| 12.2 | Observe workspace-specific content | Each workspace renders its own content correctly within the shared DRONA shell |

## 6. Expected Behaviour

| # | Behaviour | Criteria |
|---|-----------|----------|
| 1 | Single application | `streamlit run src/ui/app.py` is the only command needed. All workspaces accessible within one browser tab. |
| 2 | Single authentication | One Google OAuth login grants access to all 10 workspaces. No re-authentication when switching workspaces. |
| 3 | Internal navigation | All sidebar buttons use `st.session_state.page` routing. No external links, no new tabs. |
| 4 | Progress workspace | Curriculum tree renders with 4 subject tabs, chapter/topic hierarchy, completion states. |
| 5 | Schedule workspace | Monthly calendar renders with day cards and subject assignments. |
| 6 | Daily Debrief workspace | Page renders without errors. |
| 7 | Quick Notes workspace | Notes list, create, save, delete all function. Persistence across navigation. |
| 8 | DRONA shell consistency | Header "🎓 DRONA", sidebar, footer uniform across all workspaces. |
| 9 | Zero regression | Home, Learn (all 4 subjects), Super Chat, Quiz placeholder function identically to CPS-001. |
| 10 | Logout | Session clears. All workspaces become inaccessible until re-authentication. |

## 7. Regression Checklist

| # | Area | Verification | Result |
|---|------|-------------|--------|
| R-1 | Home workspace | Welcome Back cards render (Continue Learning, Announcements, Latest Discussion, Schedule) | ⬜ |
| R-2 | Physics workspace | Chat loads with topic strip and conversation history | ⬜ |
| R-3 | Chemistry workspace | Chat loads with topic strip and conversation history | ⬜ |
| R-4 | Maths workspace | Chat loads with topic strip and conversation history | ⬜ |
| R-5 | Biology workspace | Chat loads with topic strip, conversation history, and Pending Action | ⬜ |
| R-6 | Super Chat workspace | Open-domain chat loads | ⬜ |
| R-7 | Quiz (Coming Soon) | Placeholder renders as non-functional | ⬜ |
| R-8 | Authentication | Google OAuth login works | ⬜ |
| R-9 | Logout | Session clears, returns to login screen | ⬜ |
| R-10 | Session state | Existing session keys (`learn_messages`, `superchat_messages`, `page`, `subject`, `student_id`) persist across navigation | ⬜ |
| R-11 | Student identity | Correct student name displayed in sidebar | ⬜ |
| R-12 | Batman DD standalone | `streamlit run src/batman_dd/app.py` is not required for any feature | ⬜ |

## 8. Out-of-Scope Items

| # | Item | Reason |
|---|------|--------|
| 1 | CSS consolidation | Deferred to future CPS. DRONA shell consistent; workspace-specific DD components retain existing styling. |
| 2 | File relocation of Batman DD modules | Pages remain at `src/batman_dd/pages/`. Zero refactoring risk. |
| 3 | Deletion of `src/batman_dd/` directory | Preserves history and import paths. Cleanup deferred. |
| 4 | Business logic changes | All existing services remain unchanged. |
| 5 | Data migration | Student data at `data/students/` unchanged. |
| 6 | Infrastructure changes | No Docker, CI/CD, or deployment changes. |
| 7 | Authentication changes | `auth_gate.py` reused as-is from CPS-001. |
| 8 | Configuration changes | `settings.py`, `secrets/`, `.env` unchanged. |
| 9 | New business features | Unification only — no new functionality beyond existing Batman DD workspaces. |
| 10 | Quiz implementation | "Quiz (Coming Soon)" remains a disabled placeholder. |
| 11 | Batman DD page feature enhancements | Progress, Schedule, Debrief, Notes pages render as-is from their existing implementations. |
| 12 | Performance optimisation | No performance-related changes in this CPS. |

## 9. Pass / Fail Recording Template

### UAT Test Results

| Test ID | Description | Expected | Actual | Status |
|---------|-------------|----------|--------|--------|
| T-1 | Application launches as single entry point | Application starts on port 8501, no second app | | ⬜ |
| T-2 | Authentication required | Google OAuth login renders and completes | | ⬜ |
| T-3 | All workspaces accessible from sidebar | All 10 workspaces listed and navigable | | ⬜ |
| T-4 | Progress workspace renders | Curriculum tree with 4 subject tabs, chapters, topic rows | | ⬜ |
| T-5 | Schedule workspace renders | Monthly calendar grid with day cards | | ⬜ |
| T-6 | Daily Debrief workspace renders | Debrief page renders without errors | | ⬜ |
| T-7 | Quick Notes workspace renders | Notes list, create, save, delete function | | ⬜ |
| T-8 | Single authentication session | No re-authentication when switching workspaces | | ⬜ |
| T-9 | No external link to Batman DD | No "My Plan & Progress" external link; "Progress" navigates internally | | ⬜ |
| T-10 | Logout | Session clears, returns to login | | ⬜ |
| T-11 | Existing DRONA workspaces unchanged | Home, Learn (4 subjects), Super Chat, Quiz placeholder function identically | | ⬜ |
| T-12 | Visual shell consistency | DRONA header, sidebar, branding uniform across all workspaces | | ⬜ |

### Regression Results

| Test ID | Description | Result |
|---------|-------------|--------|
| R-1 | Home workspace | ⬜ |
| R-2 | Physics workspace | ⬜ |
| R-3 | Chemistry workspace | ⬜ |
| R-4 | Maths workspace | ⬜ |
| R-5 | Biology workspace | ⬜ |
| R-6 | Super Chat workspace | ⬜ |
| R-7 | Quiz placeholder | ⬜ |
| R-8 | Authentication | ⬜ |
| R-9 | Logout | ⬜ |
| R-10 | Session state | ⬜ |
| R-11 | Student identity | ⬜ |
| R-12 | Batman DD standalone not required | ⬜ |

### Overall Result

**PASS / FAIL** (circle one)

Date Tested:

Tested By:

---

## 10. UAT Completion Criteria

All of the following must be satisfied for UAT to be considered COMPLETE:

| # | Criterion | Evidence |
|---|-----------|----------|
| 1 | All 12 test cases (T-1 through T-12) recorded as PASS | Completed UAT Test Results table |
| 2 | All 12 regression checks (R-1 through R-12) recorded as PASS | Completed Regression Results table |
| 3 | No unresolved defects | Zero open blocker or critical defects |
| 4 | DRONA single-application behaviour verified | Product Owner confirms single app, single auth, single experience |
| 5 | All existing DRONA features confirmed unchanged | Product Owner confirms Home, Learn, Super Chat, Quiz placeholder function identically to CPS-001 |
| 6 | UAT package signed off and submitted | Completed UAT Package archived in `docs/reviews/` |

### UAT Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | | | |
| Engineering (Athena) | Athena | | |
| Engineering (Orion) | Orion | | |

---

*End of UAT Package*
