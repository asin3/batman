# Implementation Change Log
## CPS-001: Google Authentication & Application Unification

**Date:** 2026-07-19
**Time:** 21:15 IST
**Branch:** CPS-001-impl-auth-unification

---

## File: `src/ui/app.py`

| Attribute | Detail |
|-----------|--------|
| **Reason for Change** | Add shared Google authentication, replace hardcoded student ID, update sidebar for unified product experience |
| **Functions Modified** | `load_history()` — added optional `student_id` parameter with fallback to `st.session_state.student_id` |
| **Functions Added** | None (new import: `authenticate`, `logout` from `auth_gate`) |
| **Classes Modified** | None |
| **Breaking Changes** | **Yes** — Drona now requires Google authentication on launch. No anonymous access. |

### Specific Changes

| Location (approx) | Before | After |
|-------------------|--------|-------|
| Imports | No auth imports | `from src.platform.auth.auth_gate import authenticate, logout` |
| After `set_page_config` | No auth call | `user = authenticate()` |
| Session state | No student_id | `if "student_id" not in st.session_state: st.session_state.student_id = user.student_id` |
| `load_history()` path | Hardcoded `"STD001"` | Dynamic `student_id` parameter |
| All `ask_batman()` calls | `"STD001"` | `st.session_state.student_id` |
| `load_pending_action()` | `"STD001"` | `st.session_state.student_id` |
| Sidebar "Progress" | Disabled button | Active "📈 My Plan & Progress" link (new tab) |
| Sidebar user name | Not present | `user.name` displayed |
| Sidebar logout | Not present | "🚪 Logout" button calling `logout()` |

---

## File: `src/governance/learning_state.py`

| Attribute | Detail |
|-----------|--------|
| **Reason for Change** | Test block referenced deprecated `STD001` |
| **Functions Modified** | None (test `__main__` block only) |
| **Classes Modified** | None |
| **Breaking Changes** | **No** |

### Specific Changes

| Line | Before | After |
|------|--------|-------|
| 186 | `student = "STD001"` | `student = "STD000001"` |

---

## Data Migration: `data/students/`

| Item | Detail |
|------|--------|
| **Reason for Change** | Migrate legacy `STD001` data into authenticated `STD000001` workspace |
| **Files Affected** | `STD001/history.json`, `STD001/learning_state.json`, `STD000001/history.json`, `STD000001/learning_state.json` |
| **Migration Type** | Append merge (history), timestamp comparison (learning state) |
| **Backups Created** | `.bak` copies of all 4 files |
| **Cleaning** | `STD001` directory preserved. Requires Product Owner confirmation. |
| **Breaking Changes** | **No** — all existing data preserved and accessible |
