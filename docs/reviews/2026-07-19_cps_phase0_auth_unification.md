# CPS-001: Google Authentication & Application Unification

**Date:** 2026-07-19
**Time:** 20:30 IST
**Author:** Orion (HULK Coding Agent)
**Status:** Revised — Incorporating Athena Review Changes

---

## 1. CPS Title

CPS-001: Google Authentication & Application Unification

---

## 1a. Revision History

| # | Change | Source | Status |
|---|--------|--------|--------|
| 1 | CPS numbering: `CPS-000` → `CPS-001` | Athena review, Change 1 | Incorporated |
| 2 | Phase naming: `Phase 0` → `Implementation Phase 1` (Engineering Stage: CPS) | Athena review, Change 2 | Incorporated |
| 3 | Approval strategy: configurable, no hardcoded business rules | Athena review, Change 3 | Incorporated |
| 4 | Student migration lifecycle: `Migration Script → Log → Validation → PO Confirmation → Cleanup` | Athena review, Change 4 | Incorporated |
| 5 | Testing strategy: three separate gates (Developer → Athena → PO UAT) | Athena review, Change 5 | Incorporated |
| 6 | Implementation Change Log added as mandatory artifact | Athena review, Change 6 | Incorporated |
| 7 | Exit criteria updated with full Selten Engineering Lifecycle approval sequence | Athena review, Change 7 | Incorporated |

---

## 2. Scope

Convert the approved architecture review into an implementation-ready plan for:

- Wiring shared Google authentication into Drona (`src/ui/app.py`).
- Replacing the hardcoded student identity (`STD001`) with the authenticated user's `student_id`.
- Migrating legacy `STD001` student data into the authenticated `STD000001` workspace.
- Updating Drona's sidebar navigation to reflect unified product terminology.
- Adding user identity display and logout to Drona.
- Following the Selten Engineering Lifecycle for implementation, testing, and reporting.

This CPS covers the **plan only**. No code shall be modified until Athena approves this CPS and issues Green Light for Implementation.

---

## 3. In Scope

| # | Item | Evidence |
|---|------|----------|
| 1 | Wire `authenticate()` from `src/platform/auth/auth_gate.py` into `src/ui/app.py` | `src/platform/auth/auth_gate.py:22` — `authenticate()` function exists and is used by Batman DD (`src/batman_dd/app.py:50`). Drona currently has no auth call. |
| 2 | Replace all hardcoded `"STD001"` in `src/ui/app.py` with `st.session_state.user.student_id` | `src/ui/app.py:75,278,300,335,386,427` — six hardcoded references identified. |
| 3 | Migrate `data/students/STD001/history.json` and `learning_state.json` into `data/students/STD000001/` | Both files exist and are structurally compatible per `src/conversation/conversation_manager.py`. |
| 4 | Add logout button to Drona sidebar | `src/ui/app.py:140-210` — sidebar exists but has no logout. `auth_gate.py:81-88` — `logout()` function exists. |
| 5 | Display authenticated user name in Drona sidebar | Pattern exists in `src/batman_dd/app.py:117-125`. |
| 6 | Replace "📈 Progress (Coming Soon)" with "📈 My Plan & Progress" linking to Batman DD | `src/ui/app.py:206-210` — disabled button. Approved product terminology: "My Plan & Progress". |
| 7 | Update `src/governance/learning_state.py` test block from `"STD001"` to a valid ID | `src/governance/learning_state.py:186` — test code referencing `"STD001"`. |
| 8 | Produce Implementation Report after implementation | Per HCA Playbook, Section "Implementation Report Standard". |
| 9 | Produce Implementation Change Log after implementation | Per Athena review requirement. Documents every file modified, reason for change, functions/classes affected, and breaking changes. |
| 10 | Produce UAT Package after implementation | Per HCA Playbook, Section "Product Owner UAT Package". |

---

## 4. Out of Scope

The following are explicitly excluded from Implementation Phase 1:

| # | Item | Reason |
|---|------|--------|
| 1 | Merging Drona and Batman DD into a single Streamlit app | Deferred to future engineering stage. Implementation Phase 1 scope is authentication unification only. |
| 2 | Knowledge deployment automation | Deferred per Product Owner decision. |
| 3 | Production deployment pipeline | Deferred per Product Owner decision. |
| 4 | CI/CD setup | Deferred per Product Owner decision. |
| 5 | Release automation | Deferred per Product Owner decision. |
| 6 | Branding refinement | Deferred per Product Owner decision. |
| 7 | Performance optimization | Deferred per Product Owner decision. |
| 8 | JWT, cookies, session server, microservices | Rejected per Product Owner decision. |
| 9 | New top-level storage hierarchy | Rejected per Product Owner decision. |
| 10 | Pull Request workflow changes | Rejected per Product Owner decision. |
| 11 | CSS unification or redesign | Out of scope — Implementation Phase 1 does not modify stylesheets. |
| 12 | Any architectural redesign outside approved scope | Rejected per Product Owner decision. |

---

## 5. Approved Architecture Decisions

The following architecture decisions from the BARR are approved and form the basis of this CPS:

| # | Decision | Source |
|---|----------|--------|
| 1 | **Reuse existing shared authentication.** Drona imports `authenticate()` from `src/platform/auth/auth_gate.py`. No new auth component needed. | BARR Recommendation Topic 1 |
| 2 | **Session state remains per-app.** Each Streamlit app independently authenticates. `student_id` is the shared identity key. | BARR Recommendation Topic 1 |
| 3 | **Student ID resolves from `st.session_state.user.student_id`** after authentication. No custom ID mapping. | BARR Recommendation Topic 1 |
| 4 | **Approval mechanism remains configurable.** The authentication framework shall support the current Product Owner approval policy without embedding temporary business rules. | BARR Recommendation Topic 1 (as amended by Athena review) |
| 5 | **No JWT, cookies, or session server.** Streamlit's `st.session_state` is sufficient. | BARR Recommendation Topic 1 |
| 6 | **Existing `data/` and `vector_db/` hierarchy preserved.** No new top-level storage. | BARR Recommendation Topic 3 |
| 7 | **Existing ADRs preserved.** No ADR modification in Implementation Phase 1. | Approved Decision Matrix |
| 8 | **Desktop First architecture preserved.** | Approved Decision Matrix |
| 9 | **Local First architecture preserved.** | Approved Decision Matrix |
| 10 | **Single Source of Truth preserved.** | Approved Decision Matrix |

---

## 6. Approved with Changes

| # | Item | Decision | Impact |
|---|------|----------|--------|
| 1 | **Navigation label:** "My Plan & Progress" is the approved product terminology. Implementation shall use this exact label. | Product Owner decision. Overrides BARR's "Progress" recommendation. | Sidebar label change only. Link target remains the same (opens Batman DD in new tab). |
| 2 | **Engineering Workflow:** Selten Engineering Lifecycle shall be followed. Ignore older workflow recommendations from previous reviews. | Product Owner decision. | Implementation follows lifecycle stages. Implementation Report and UAT Package are mandatory. |

---

## 7. Rejected Items

The following recommendations from the BARR are rejected and shall NOT appear in this CPS:

| # | Item | Reason |
|---|------|--------|
| 1 | Pull Request workflow | Rejected — HCA Playbook v1.1 (Engineering Maturity: Early Product) specifies PR optional. |
| 2 | Mandatory CI pipeline | Rejected — CI optional at current maturity stage. |
| 3 | JWT | Rejected — over-engineered for current scale. |
| 4 | Cookie-based authentication | Rejected — Streamlit session state is sufficient. |
| 5 | Session server | Rejected — introduces unnecessary infrastructure. |
| 6 | Microservices | Rejected — violates KISS and current architecture. |
| 7 | New top-level storage hierarchy | Rejected — violates ADR-004 Single Source of Truth. |
| 8 | Merging both apps into one Streamlit app | Deferred — out of Implementation Phase 1 scope. |

---

## 8. Assumptions

| # | Assumption | Evidence |
|---|------------|----------|
| 1 | The shared `authenticate()` function requires no modification. It is already production-ready. | `src/platform/auth/auth_gate.py:22-74` — function is complete, used by Batman DD. `src/platform/auth/google_auth.py:102-145` — OAuth flow is implemented. `src/platform/providers/google_oauth.py` — token verification works. |
| 2 | Google OAuth credentials exist and are configured. | `secrets/google_oauth.json` — OAuth 2.0 client credentials present. |
| 3 | Supabase storage is configured and available for cloud deployments. | `src/config/storage.json` — `{"backend": "supabase"}`. `secrets/supabase.json` — URL and service role key present. |
| 4 | The `StorageRouter` abstraction works for both local and Supabase backends. | `src/platform/storage/storage_router.py` — routing logic complete. `local_storage_repository.py` and `supabase_storage_repository.py` — both implemented. |
| 5 | Approval policy is configurable and does not require architectural change. | `src/platform/services/user_service.py:98-118` — `approve_user()` function exists. Default status is `PENDING`. If Product Owner requires auto-approval, only the default status value changes — architecture is unaffected. |
| 6 | Drona's `src/ui/app.py` is the only file with hardcoded `"STD001"` references that affect runtime behavior. | Confirmed by grep of entire `src/` directory. Only `src/ui/app.py` (6 occurrences) and `src/governance/learning_state.py` (1 test occurrence) contain hardcoded `"STD001"`. |

---

## 9. Files Expected to Change

### Source Files

| # | File | Change Type | Description |
|---|------|-------------|-------------|
| 1 | `src/ui/app.py` | **Modify** | Add `authenticate()` call. Replace all 6 `"STD001"` with `st.session_state.user.student_id`. Replace disabled "Progress (Coming Soon)" with active "My Plan & Progress" button. Add logout button. Add user name display. |
| 2 | `src/governance/learning_state.py` | **Modify** | Update test block from `"STD001"` to a valid student ID (e.g., `"STD000001"` or make it dynamic). |

### Data Files

| # | File | Change Type | Description |
|---|------|-------------|-------------|
| 3 | `data/students/STD001/history.json` | **Migrate** | Contents merged into `data/students/STD000001/history.json` (append). Original file preserved. Legacy cleanup requires Product Owner confirmation — never automatic. |
| 4 | `data/students/STD001/learning_state.json` | **Migrate** | Contents compared with `data/students/STD000001/learning_state.json`. Keep whichever has more recent `last_updated` field. Original preserved. |

### No Change Required

The following were investigated and require no modification:

| File | Reason |
|------|--------|
| `src/conversation/conversation_manager.py` | Already `student_id`-parameterized. No hardcoded references. |
| `src/batman_engine.py` | `ask_batman(student_id, question)` — receives `student_id` dynamically. No hardcoding. |
| `src/platform/auth/auth_gate.py` | Already complete. No modification needed. |
| `src/platform/auth/google_auth.py` | Already complete. No modification needed. |
| `src/platform/services/user_service.py` | Already complete. Approval policy is configurable per Product Owner preference. No architectural change required. |
| `src/platform/services/student_repository.py` | Already complete. No modification needed. |
| `src/config/settings.py` | No auth-related configuration changes needed. |
| `src/config/paths.py` | No path changes needed. |

### Total Files Modified: 2 source files, 2 data files migrated

---

## 10. Risks

| # | Risk | Impact | Likelihood | Mitigation | Owner |
|---|------|--------|------------|------------|-------|
| 1 | Adding `authenticate()` call to Drona breaks existing development flow where no auth was required | Medium | Medium | After implementation, Drona requires Google login. Local dev can use existing test user credentials. Document in Implementation Report. | Developer |
| 2 | Google OAuth redirect URI mismatch causes login failure | High | Low | Verify `redirect_uris` in `secrets/google_oauth.json` matches the deployed URL. Currently `http://localhost:8501`. | Developer |
| 3 | `get_user_by_email()` fails if user does not exist in storage | Medium | Low | `login_or_register()` in `user_service.py` creates a new user if not found. Fallback path exists. | Developer |
| 4 | Legacy `STD001` data merge produces corrupted `history.json` | High | Low | Migration script writes to a new file first, then atomically replaces the original. Pre-migration backup created. | Developer |
| 5 | Learning state conflict between `STD001` and `STD000001` | Low | Medium | Both learning states exist. Decision: keep the more recent `last_updated`. Document the choice. | Developer |
| 6 | Auth dependency (`streamlit-oauth`, `google-auth`) missing in runtime | High | Low | `requirements.txt` already includes `streamlit-oauth==0.1.14` and `google-auth`. No new dependencies needed. | Developer |
| 7 | `"My Plan & Progress"` button in sidebar has no target if Batman DD is not running | Medium | Low | Button opens Batman DD in new tab at configured URL. If DD is not running, user sees browser error. Acceptable for MVP — DD should be deployed alongside Drona. | Product Owner |

---

## 11. Rollback Plan

### Pre-Migration Backup

Before any code or data changes:

```
cp data/students/STD001/history.json data/students/STD001/history.json.bak
cp data/students/STD001/learning_state.json data/students/STD001/learning_state.json.bak
cp data/students/STD000001/history.json data/students/STD000001/history.json.bak
cp data/students/STD000001/learning_state.json data/students/STD000001/learning_state.json.bak
```

### Code Rollback

| Step | Command | Effect |
|------|---------|--------|
| 1 | `git checkout -- src/ui/app.py` | Reverts all auth and sidebar changes |
| 2 | `git checkout -- src/governance/learning_state.py` | Reverts test block change |


### Data Rollback

| Step | Command | Effect |
|------|---------|--------|
| 1 | `cp data/students/STD000001/history.json.bak data/students/STD000001/history.json` | Restores pre-migration history |
| 2 | `cp data/students/STD000001/learning_state.json.bak data/students/STD000001/learning_state.json` | Restores pre-migration learning state |
| 3 | `cp data/students/STD001/history.json.bak data/students/STD001/history.json` | Restores original STD001 data (validation period only) |

### Rollback Validation

After rollback:
1. Launch `streamlit run src/ui/app.py` — app should start without auth.
2. Verify `ask_batman()` calls use `"STD001"` (hardcoded fallback).
3. Verify `src/governance/learning_state.py` test runs with `"STD001"`.

### Rollback Window

Full rollback is possible up to the point where `STD001` directory is deleted (which occurs only after Product Owner confirmation — NOT automatically).

---

## 12. Unit Testing Strategy

### Authentication Flow Tests

| # | Test Case | Expected Result | Type |
|---|-----------|-----------------|------|
| 1 | `authenticate()` called when no `st.session_state.user` exists | OAuth login button rendered | Manual (UI) |
| 2 | Google OAuth button clicked, valid credentials provided | User authenticated, `st.session_state.user` populated | Manual (UI) |
| 3 | Google OAuth button clicked, invalid/expired token | `st.stop()` called, app halted | Manual (UI) |
| 4 | New user logs in for first time | User auto-approved, `student_id` assigned, workspace created | Manual (UI) |
| 5 | Existing user logs in again | Existing user returned, no duplicate registration | Automated via `user_service.py` test |
| 6 | Logout button clicked | All `st.session_state` keys cleared, app reruns to login | Manual (UI) |

### Student Identity Tests

| # | Test Case | Expected Result | Type |
|---|-----------|-----------------|------|
| 7 | `ask_batman()` called after auth | `student_id` is `st.session_state.user.student_id`, not `"STD001"` | Automated (code review) |
| 8 | History loaded after auth | History from `data/students/{student_id}/history.json` | Manual (UI) |
| 9 | Learning state loaded after auth | Learning state from `data/students/{student_id}/learning_state.json` | Manual (UI) |

### Data Migration Tests

| # | Test Case | Expected Result | Type |
|---|-----------|-----------------|------|
| 10 | Migration script merges `STD001/history.json` into `STD000001/history.json` | Combined file has 386 + 513 = 899 entries | Automated (script output) |
| 11 | Merged `history.json` is valid JSON | `python -m json.tool` succeeds | Automated |
| 12 | Pre-migration backup files exist | `.bak` files present in both `STD001` and `STD000001` | Automated |
| 13 | Migration Log produced | Log documents files merged, entry counts, decisions | Manual verification |
| 14 | Learning state reflects most recent `last_updated` | State chapter/topic matches the more recent activity | Manual verification |
| 15 | `STD001` directory preserved after migration | `STD001/` still exists with original data | Automated |
| 16 | `STD001` cleanup requires PO confirmation | Cleanup NOT performed without explicit PO approval | Process verification |

### Sidebar Navigation Tests

| # | Test Case | Expected Result | Type |
|---|-----------|-----------------|------|
| 14 | "📈 My Plan & Progress" button visible in sidebar | Button label reads "📈 My Plan & Progress", not disabled | Manual (UI) |
| 15 | "My Plan & Progress" clicked | Opens Batman DD URL in new browser tab | Manual (UI) |
| 16 | Logout button visible in sidebar | "🚪 Logout" button present below user name | Manual (UI) |
| 17 | User name displayed in sidebar | Authenticated user's name visible | Manual (UI) |

### Regression Tests

| # | Test Case | Expected Result | Type |
|---|-----------|-----------------|------|
| 18 | Home page loads without error | `HOME` page renders with "Welcome Back" and cards | Manual (UI) |
| 19 | Subject workspace loads | Physics/Chemistry/Maths/Biology workspace renders | Manual (UI) |
| 20 | Super Chat loads | Chat interface renders, messages send/receive | Manual (UI) |
| 21 | Quiz starts (if auth student has history) | Quiz flow works with authenticated student data | Manual (UI) |

### Test Automation Note

At the current engineering maturity stage (Early Product per HCA Playbook v1.1), manual testing is acceptable. Automated tests are not required for Implementation Phase 1. The Implementation Report shall document all test results manually.

---

## 13. Exit Criteria

Implementation Phase 1 is complete only when ALL of the following are satisfied:

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | Drona requires Google authentication on launch | Launch `src/ui/app.py` — login screen appears before any content |
| 2 | Authenticated user's `student_id` is used for all data operations | `ask_batman()` calls use `st.session_state.user.student_id` |
| 3 | `STD001` data migrated into `STD000001` workspace | `STD000001/history.json` contains 899+ entries (386 from STD001 + 513 from STD000001) |
| 4 | Pre-migration backup files exist | `.bak` files in both `STD001` and `STD000001` directories |
| 5 | "📈 My Plan & Progress" button visible and active in Drona sidebar | Button label correct, opens Batman DD in new tab |
| 6 | User name displayed in Drona sidebar | Sidebar shows authenticated user's name |
| 7 | Logout button works | Clicking logout clears session and returns to login |
| 8 | All 23 test cases in Section 12 executed and pass | Test results documented in Implementation Report |
| 9 | No regression in existing functionality | Home, workspace, Super Chat, and Quiz still work |
| 10 | Implementation Report submitted | Report follows HCA Playbook Implementation Report Standard |
| 11 | Implementation Change Log submitted | Log documents files modified, reason, functions/classes, breaking changes |
| 12 | Athena Implementation Approval received | Athena reviews and approves Implementation Report and Change Log |
| 13 | Product Owner UAT completed | Product Owner executes UAT Package and provides sign-off |
| 14 | Merge Approval received | All gates passed; branch approved for merge to `develop` |

---

## 14. Deliverables

| # | Artifact | Format | Location |
|---|----------|--------|----------|
| 1 | **Implementation Report** | Markdown | `docs/reviews/2026-07-XX_implementation_report_auth_unification.md` |
| 2 | **Implementation Change Log** | Markdown | `docs/reviews/2026-07-XX_changelog_auth_unification.md` |
| 3 | **UAT Package** | Markdown | `docs/reviews/2026-07-XX_uat_package_auth_unification.md` |
| 4 | **Modified source code** | Python | `src/ui/app.py` (updated), `src/governance/learning_state.py` (updated) |
| 5 | **Migration backup** | JSON | `data/students/STD001/history.json.bak`, `data/students/STD001/learning_state.json.bak` |
| 6 | **Migration backup** | JSON | `data/students/STD000001/history.json.bak`, `data/students/STD000001/learning_state.json.bak` |
| 7 | **Migration Log** | Markdown | Produced during Step 5, documenting all migration decisions |

---

## 15. Implementation Sequence

### Step 1 — Pre-Implementation (Preparation)

1. Read and understand `src/ui/app.py` (438 lines).
2. Read and understand `src/platform/auth/auth_gate.py`.
3. Read and understand `src/platform/services/user_service.py`.
4. Read and understand `src/platform/services/student_repository.py`.
5. Create pre-migration backups of all data files.

### Step 2 — Authentication Wire-Up

1. Add import to `src/ui/app.py`: `from src.platform.auth.auth_gate import authenticate, logout`.
2. Add call: `user = authenticate()` after `st.set_page_config()` — same pattern as `src/batman_dd/app.py:50`.
3. Store `user.student_id` in `st.session_state`.

### Step 3 — Replace Hardcoded STD001

1. Replace all 6 occurrences of `"STD001"` in `src/ui/app.py` with `st.session_state.user.student_id`.
2. Replace the hardcoded history path (line 75) to use `st.session_state.user.student_id` dynamically.
3. Update `src/governance/learning_state.py` test block.

### Step 4 — Sidebar Updates

1. Replace disabled "📈 Progress (Coming Soon)" button with active "📈 My Plan & Progress" button.
2. Add user name display below sidebar divider (pattern from `src/batman_dd/app.py:117-125`).
3. Add "🚪 Logout" button below user name.

### Step 5 — Data Migration

Migration lifecycle:

```
Migration Script
  ↓
Migration Log
  ↓
Validation
  ↓
Product Owner Confirmation
  ↓
Legacy Cleanup
```

1. Run migration script to merge `STD001/history.json` into `STD000001/history.json`.
2. Compare `learning_state.json` files; keep the more recent `last_updated`.
3. Write Migration Log documenting all changes (files merged, entries counted, decisions made).
4. Validate merged data (valid JSON, correct entry count).
5. Submit Migration Log to Product Owner for confirmation.
6. Legacy cleanup (`STD001` directory removal) occurs ONLY after Product Owner confirmation.
7. Legacy data is never removed automatically.

### Step 6 — Testing

Testing follows three separate engineering quality gates:

```
Developer Unit Testing
  ↓
Athena Review
  ↓
Product Owner UAT
```

1. **Developer Unit Testing**: Execute all 23 test cases from Section 12. Document results in Implementation Report.
2. **Athena Review**: Athena reviews test results and Implementation Report. Issues approval or identifies issues.
3. **Product Owner UAT**: Product Owner executes UAT Package. Validates functionality against business requirements.

### Step 7 — Implementation Report, Change Log & UAT Package

1. Write Implementation Report (per HCA Playbook Implementation Report Standard).
2. Write Implementation Change Log documenting:
   - Files Modified
   - Reason for Change
   - Functions Modified
   - Classes Modified
   - Breaking Changes (Yes/No)
3. Write UAT Package (per HCA Playbook Product Owner UAT Package standard).

---

## 16. Testing Approach (Detailed)

### Manual UI Testing

All UI tests shall be executed in the local development environment:
- `streamlit run src/ui/app.py` — Drona with auth.
- `streamlit run src/batman_dd/app.py` — Batman DD (for "My Plan & Progress" link validation).

### Migration Script Testing

The merge operation shall be tested by running the script against backup copies first. The script should:

```python
# Pseudocode — not implementation
import json, shutil, os

# Backup
for d in ["STD001", "STD000001"]:
    for f in ["history.json", "learning_state.json"]:
        src = f"data/students/{d}/{f}"
        dst = f"data/students/{d}/{f}.bak"
        shutil.copy2(src, dst)

# Merge history
with open("data/students/STD000001/history.json") as f:
    target = json.load(f)
with open("data/students/STD001/history.json") as f:
    source = json.load(f)
merged = target + source
with open("data/students/STD000001/history.json", "w") as f:
    json.dump(merged, f, indent=2)

# Verify
assert len(merged) == len(target) + len(source)
with open("data/students/STD000001/history.json") as f:
    assert json.load(f) == merged
```

### Engineering Quality Gates

Testing is executed in three sequential stages with clear handoffs:

| Gate | Responsible | Deliverable | Approves |
|------|-------------|-------------|----------|
| **Developer Unit Testing** | Developer | Implementation Report with test results | Technical correctness |
| **Athena Review** | Athena (Chief Architect) | Architecture approval | Architectural compliance |
| **Product Owner UAT** | Product Owner | UAT sign-off | Business requirements met |

No gate may be skipped. No subsequent gate begins until the prior gate approves.

### Known Limitation

Streamlit UI tests cannot be fully automated without a framework like `selenium` or `streamlit.testing`. At the current maturity stage, manual testing with documented screenshots is acceptable.

---

## 17. Next Engineering Stage

### Required Approval Sequence

Once Athena validates the revised CPS and issues Green Light for Implementation:

```
Implementation (per Section 15)
  ↓
Developer Unit Testing (23 test cases)
  ↓
Implementation Report
  ↓
Implementation Change Log
  ↓
Athena Implementation Review
  ↓
Green Light for Product Owner UAT
  ↓
Product Owner UAT
  ↓
Green Light for Merge
  ↓
Merge to develop
```

### Implementation Branch

1. Branch from `develop`: `git checkout -b CPS-001-impl-auth-unification`
2. Implement per sequence in Section 15.
3. Test per Section 12.
4. Produce Implementation Report.
5. Produce Implementation Change Log.
6. Produce UAT Package.
7. Submit all artifacts for Athena Implementation Review.

No subsequent stage may begin without approval from the prior stage.

---

==================================================

Architecture Status

==================================================

Architecture Stable?
YES

Implementation Ready?
YES — pending Athena validation of CPS updates

Outstanding Questions
None. All seven mandatory changes from Athena review have been incorporated.

Overall Risk
LOW

Recommendation
Proceed — submit revised CPS to Athena for final validation.

Reviewer Confidence
High

==================================================
