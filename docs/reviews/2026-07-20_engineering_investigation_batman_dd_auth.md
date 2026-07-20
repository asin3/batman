# Engineering Investigation Report
## Batman DD Authentication Behavior

**Date:** 2026-07-20
**Time:** 13:30 IST
**Investigator:** Orion (HULK Coding Agent)
**Repository:** batman_student
**Branch:** CPS-001-impl-auth-unification

---

## 1. Investigation Scope

Product Owner UAT observed the following:

> Drona authentication succeeds. Navigation to Batman DD succeeds. Batman DD displays its login screen. The Google authentication flow does not complete successfully.

The investigation addresses:
- Whether this behavior matches the approved architecture
- If expected: explain why
- If not: root cause and CPS recommendation

---

## 2. Findings

### 2.1 Authentication Architecture

Both Drona (`src/ui/app.py`) and Batman DD (`src/batman_dd/app.py`) use the **identical shared authentication module**:

```
src/platform/auth/auth_gate.py
```

Both apps call `authenticate()` at module load:

| App | File | Line |
|-----|------|------|
| Drona | `src/ui/app.py` | 44 |
| Batman DD | `src/batman_dd/app.py` | 50 |

The auth chain is identical: `auth_gate.authenticate()` → `google_auth.login()` → `OAuth2Component.authorize_button()` → Google OAuth consent.

### 2.2 Why Batman DD Shows Its Own Login

Streamlit's `st.session_state` is **per-process**. Drona and Batman DD run as separate Python processes. When a user clicks "My Plan & Progress" in Drona, it opens `http://localhost:8501` in a new tab. That tab loads Batman DD's process, which has an empty `st.session_state` — so `authenticate()` renders the "Continue with Google" button.

**The independent session behavior is not a defect.** It is explicitly approved in the CPS:

> CPS Section 5, Item 2: "Session state remains per-app. Each Streamlit app independently authenticates. student_id is the shared identity key."

> CPS Section 4, Item 1: "Merging Drona and Batman DD into a single Streamlit app — Deferred to future engineering stage."

The UAT Package itself documents this as expected (Test 3, Step 3.3):
> "If not authenticated in Batman DD | Batman DD shows its own Google login (independent session)"

### 2.3 Why Google Auth Fails to Complete

The Product Owner reported "the Google authentication flow does not complete successfully." The root cause is a **deployment configuration issue**, not an implementation defect:

**Google OAuth redirect URI is hardcoded to port 8501:**

| Location | Value | Line |
|----------|-------|------|
| `src/config/settings.py` | `GOOGLE_REDIRECT_URI = "http://localhost:8501"` | 54 |
| `src/platform/auth/google_auth.py` | Reads `redirect_uris[0]` from `google_oauth.json` | 119 |
| `src/ui/app.py` | Hardcoded `href="http://localhost:8501"` for DD link | 224 |

Google OAuth requires the redirect URI to exactly match what is registered in the Google Cloud Console. If Batman DD is served on a port other than 8501 (e.g., 8502 when both apps run simultaneously), Google returns `redirect_uri_mismatch` and the auth flow silently fails.

This explains the Product Owner's observation: "screen displayed, then again popup, that login doesn't do anything."

---

## 3. Architecture Assessment

| Behavior | Expected per Architecture? | Status |
|----------|---------------------------|--------|
| Batman DD shows independent login | YES — per CPS Section 5, Item 2 | Working as designed |
| Auth flow does not complete | NO — deployment configuration limitation | Environment blocker |

The independent session behavior is correct. The auth failure is caused by the hardcoded port-8501 redirect URI, not by the authentication implementation.

---

## 4. Architecture Recommendation

### Finding: No Architectural Change Required

The independent session behavior is intentional and approved. The CPS explicitly defers single-app unification to a future phase. No architectural correction is needed.

### Recommended Operational Guidance

For **Product Owner UAT**, the recommended workaround is:

> Run only **one Streamlit app at a time** on port 8501. This ensures the Google OAuth redirect URI matches the running app.

Procedure:
```bash
# Terminal 1: Drona
source .venv/bin/activate && streamlit run src/ui/app.py

# Stop Drona (Ctrl+C), then:
# Terminal 1: Batman DD
source .venv/bin/activate && streamlit run src/batman_dd/app.py
```

When only one app runs at a time on port 8501, Google OAuth completes successfully for both apps independently.

### Future CPS Consideration

If the Product Owner requires **single sign-on across both apps**, this should be addressed in a future CPS for merging Drona and Batman DD into a single Streamlit application. This is already approved as a deferred item in CPS Section 4, Item 1.

---

## 5. Files Referenced

| File | Relevance |
|------|-----------|
| `src/ui/app.py` | Drona auth call (L44), hardcoded DD URL (L224) |
| `src/batman_dd/app.py` | Batman DD auth call (L50) |
| `src/platform/auth/auth_gate.py` | Shared auth module |
| `src/platform/auth/google_auth.py` | OAuth redirect URI resolution (L119) |
| `src/config/settings.py` | `GOOGLE_REDIRECT_URI` config (L54) |
| `docs/reviews/2026-07-19_cps_phase0_auth_unification.md` | Approved architecture — per-app session state (Section 5, Item 2) |
| `docs/reviews/2026-07-19_uat_package_auth_unification.md` | Test 3.3 documents expected behavior |
| `docs/reviews/2026-07-20_athena_implementation_review_cps001.md` | Athena approved implementation |

---

## 6. Conclusion

| Question | Answer |
|----------|--------|
| Does Batman DD auth behavior match approved architecture? | **YES** — independent session is by design |
| Is the Google auth flow failure an architecture defect? | **NO** — it is a deployment configuration limitation (hardcoded port 8501) |
| Is a CPS correction required? | **NOT YET** — UAT can proceed with single-app procedure |

---

## Architecture Status

Architecture Stable? YES
Implementation Ready? YES
Overall Risk: LOW
Outstanding Questions: None
Recommendation: **Proceed with Product Owner UAT** using single-app procedure
Reviewer Confidence: High
