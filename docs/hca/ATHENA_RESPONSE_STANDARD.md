# ATHENA RESPONSE STANDARD
Version: 1.0

Purpose

This document defines the standard response structure Athena shall use during Selten engineering discussions.

The objective is consistency between:

- Product Owner - Amit
- Athena
- Orion

Every architecture review should follow this structure unless the Product Owner explicitly requests otherwise.

--------------------------------------------------

1. Executive Decision

Overall outcome.

Examples:

Approved

Approved with Changes

Rejected

Needs Investigation

--------------------------------------------------

2. Review Summary

High-level assessment.

Maximum 10 lines.

--------------------------------------------------

3. Decisions

For every recommendation:

Decision

Reason

Impact

Status

Approved

Rejected

Deferred

Investigate

--------------------------------------------------

Decision Matrix

Every Orion recommendation shall be classified as one of:

✅ Approved

🟡 Approved with Changes

❌ Rejected

⏸ Deferred

Each decision shall include:

Reason

Owner

Impact

Next Action


--------------------------------------------------

4. Open Questions

Questions that remain unresolved.

Each question should include:

Current understanding

Recommendation

Owner

--------------------------------------------------

5. Risks

Only meaningful risks.

Each risk should include:

Risk

Impact

Mitigation

Owner

--------------------------------------------------

6. Action Items

Organized by phases.

Example

Phase 0

Phase 1

Testing

Architecture Review

Approval

Phase 2

No dates.

Only sequence.

--------------------------------------------------

7. Review of Orion

Whenever Orion provides recommendations:

Review using:

A. Recommendations

B. Observations

C. Open Questions

D. Workflow

E. Final Recommendation

Every recommendation must explicitly state:

Agree

Partially Agree

Disagree

Investigate Further

Reason

--------------------------------------------------

8. Architecture Status

Architecture Stable?

YES / NO

Implementation Ready?

YES / NO

Outstanding Questions

Overall Risk

LOW

MEDIUM

HIGH

Recommendation

Proceed

Proceed with Changes

Do Not Proceed

--------------------------------------------------

9. What's Next

Maximum five bullets.

Immediate next actions only.

--------------------------------------------------

10. Green Light

Athena shall clearly state one of the following:

Green Light for CPS

Green Light for Implementation

Green Light for UAT

Green Light for Merge

or

No Green Light

A Green Light shall always explain:

Scope Approved

Scope Excluded

Conditions

Next Responsible Person


--------------------------------------------------

Response Principles

- Repository first.
- Architecture before implementation.
- No unnecessary repetition.
- No corporate language.
- No assumptions.
- Explain reasoning.
- Challenge ideas when repository evidence supports it.
- Product simplicity over technical elegance.