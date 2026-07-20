# AGENT BRANCHING STANDARD

Version: 1.0

Status: Active

Owner: Athena

---

# Purpose

This standard defines the branch naming convention for engineering work performed by AI agents and human engineers.

The objective is to provide clear ownership, improve engineering traceability, and simplify repository management.

---

# Principles

Every engineering branch shall identify:

- Responsible engineering agent
- Engineering work item
- CPS association where applicable

Branch ownership shall remain visible throughout the engineering lifecycle.

---

# Branch Namespace

The following namespace prefixes are approved.

| Namespace | Owner |
|-----------|-------|
| orion/ | Orion |
| athena/ | Athena |
| codex/ | Codex |
| human/ | Product Owner or Human Developer |

Additional namespaces may be introduced as new engineering agents are adopted.

---

# Branch Naming Convention

Engineering branches shall follow:

<agent>/<work-item>

Examples:

orion/CPS-002-drona-workspace-unification

codex/CPS-010-performance-optimization

athena/architecture-prototype

human/hotfix-login

---

# Merge Policy

Feature branches shall merge into:

develop

Only after:

- Athena Merge Readiness Review
- Green Light for Merge

---

# Historical Branches

Branches created before adoption of this standard remain unchanged.

Historical branches shall not be renamed solely to comply with this standard.

---

# Relationship to Other Standards

This standard complements:

- HCA_PLAYBOOK.md
- ATHENA_CPS_CLOSURE_STANDARD.md

---

# Decision

Agent namespace branch naming is adopted as the official engineering branching strategy for Selten repositories.