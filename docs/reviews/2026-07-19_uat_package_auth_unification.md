# Product Owner UAT Package
## CPS-001: Google Authentication & Application Unification

**Date:** 2026-07-19
**Time:** 21:15 IST
**Branch:** CPS-001-impl-auth-unification

---

## Branch Name

```
CPS-001-impl-auth-unification
```

## Environment Certification

Before executing UAT, complete Phase 0 – Environment Certification per the PRODUCT_OWNER_UAT_STANDARD.

Certification checks:
- Repository Validation
- Python Environment Validation
- Python Runtime Validation
- Application Dependency Validation
- Secrets Validation
- Data Validation
- Network Validation
- Browser Validation

Record the Environment Certification result in `docs/uat/` and confirm PASS before proceeding.

## How to Checkout

```
git fetch origin
git checkout CPS-001-impl-auth-unification
```

## How to Run

### Drona (with authentication)
```bash
streamlit run src/ui/app.py
```

### Batman DD (for "My Plan & Progress" link validation)
```bash
streamlit run src/batman_dd/app.py
```

## Required Test Data

- Google account for authentication (use the Product Owner's approved test account email that maps to the existing student profile)
- Google OAuth credentials configured in `secrets/google_oauth.json` (local) or `st.secrets` (Streamlit Cloud)
- Supabase credentials configured in `secrets/supabase.json` (optional — local storage works too)

## Test Steps

### Test 1: Authentication Required

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1.1 | Run `streamlit run src/ui/app.py` | "Continue with Google" button appears |
| 1.2 | Do NOT click login | Drona content is NOT rendered |
| 1.3 | Click "Continue with Google" | Google OAuth consent screen appears |
| 1.4 | Select a Google account | Drona home page loads |

### Test 2: Student Identity

| Step | Action | Expected Result |
|------|--------|-----------------|
| 2.1 | After login, observe the sidebar | User name displayed (e.g., "Amit") |
| 2.2 | Navigate to a subject workspace (e.g., Physics) | Chat interface loads with history from `STD000001` |
| 2.3 | Send a message | `ask_batman()` uses `STD000001` (not `STD001`) |

### Test 3: "My Plan & Progress"

| Step | Action | Expected Result |
|------|--------|-----------------|
| 3.1 | In Drona sidebar, locate "📈 My Plan & Progress" | Button is active (not disabled) |
| 3.2 | Click "📈 My Plan & Progress" | Batman DD opens in a new browser tab |
| 3.3 | If not authenticated in Batman DD | Batman DD shows its own Google login (independent session) |

### Test 4: Logout

| Step | Action | Expected Result |
|------|--------|-----------------|
| 4.1 | After login, click "🚪 Logout" in the sidebar | Session cleared |
| 4.2 | Page refreshes | "Continue with Google" login screen appears again |

### Test 5: Data Migration Verification

| Step | Action | Expected Result |
|------|--------|-----------------|
| 5.1 | Check `data/students/STD000001/history.json` | File contains 475 entries |
| 5.2 | Check `data/students/MIGRATION_LOG_CPS001.md` | Migration Log exists with all details |
| 5.3 | Check `data/students/STD001/` | Directory still exists (not deleted) |
| 5.4 | Check `data/students/STD000001/learning_state.json` | `last_updated` is `2026-07-15T04:44:49` |

### Test 6: Regression — Existing Features

| Step | Action | Expected Result |
|------|--------|-----------------|
| 6.1 | Click "🏠 Home" | Home page renders with "Welcome Back" and cards |
| 6.2 | Click "📚 Learn → Physics" | Physics workspace loads with chat |
| 6.3 | Click "💬 Super Chat" | Super Chat loads |
| 6.4 | Type a quiz command (e.g., "Quiz me on Force easy 1") | Quiz starts (if student has history) |

## Expected Results Summary

| # | Feature | Expected |
|---|---------|----------|
| 1 | Google login required | ✅ |
| 2 | Authenticated student_id used | ✅ |
| 3 | User name in sidebar | ✅ |
| 4 | "My Plan & Progress" opens DD | ✅ |
| 5 | Logout works | ✅ |
| 6 | Migrated data accessible | ✅ |
| 7 | No regression | ✅ |

## Rollback Instructions

```bash
# Code rollback
git checkout develop -- src/ui/app.py
git checkout develop -- src/governance/learning_state.py

# Data rollback
cp data/students/STD000001/history.json.bak data/students/STD000001/history.json
cp data/students/STD000001/learning_state.json.bak data/students/STD000001/learning_state.json
cp data/students/STD001/history.json.bak data/students/STD001/history.json
cp data/students/STD001/learning_state.json.bak data/students/STD001/learning_state.json
```

All rollback steps are reversible. No data loss occurs.
