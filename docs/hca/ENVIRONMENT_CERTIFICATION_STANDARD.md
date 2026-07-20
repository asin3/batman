# ENVIRONMENT CERTIFICATION STANDARD

Version: 1.0

Status: Active

Owner: Athena

---

# Purpose

This document defines the mandatory Environment Certification process for all engineering activities within Selten repositories.

The objective is to ensure that every engineering task executes in a verified, reproducible, and supported environment before implementation, testing, review, or deployment begins.

Environment Certification validates the execution environment.

It does not validate business functionality.

---

# Applicability

This standard shall be followed before:

- Product Owner UAT
- Developer Testing
- Orion Implementation
- Athena Review (when execution is required)
- CI/CD execution
- Automated Engineering Tasks

No engineering activity requiring code execution shall begin until Environment Certification passes.

---

# Certification Principle

Environment failures shall never be classified as application defects.

Environment failures shall be resolved before engineering work continues.

---

# Phase 0 – Environment Certification

Every engineering activity begins with Environment Certification.

Only after a PASS result may the next engineering phase begin.

---

# Repository Validation

Verify:

□ Correct repository

□ Correct branch

□ Working tree clean

Commands:

```bash
git branch
git status
```

Expected:

- Correct branch checked out
- Working tree clean

---

# Python Environment Validation

Verify:

□ Virtual environment exists

□ Virtual environment activated

□ python resolves from the virtual environment

□ pip resolves from the virtual environment

Commands:

```bash
which python
which pip
echo $VIRTUAL_ENV
```

Expected:

python

↓

.venv/bin/python

pip

↓

.venv/bin/pip

---

# Python Runtime Validation

Commands:

```bash
python --version
pip --version
```

Expected:

Commands execute successfully.

No system Python shall be used.

---

# Dependency Validation

Verify required runtime tools.

Examples:

```bash
streamlit --version
python -m streamlit --version
```

Additional tools may include:

- uvicorn
- pytest
- chroma
- ollama
- aider

Expected:

Required runtime dependencies execute successfully.

---

# Secrets Validation

Verify required secrets exist.

Examples:

- Google OAuth
- OpenAI
- Supabase
- Local Configuration

Sensitive values shall never be recorded in certification reports.

---

# Data Validation

Verify required engineering data exists.

Examples:

- Student Data
- Migration Files
- Configuration Files
- Vector Database
- Knowledge Base

---

# External Service Validation

Verify required external services are reachable.

Examples:

- Google OAuth
- Supabase
- OpenAI
- Local Model Server
- Ollama

Only services required by the current engineering activity need validation.

---

# Browser Validation

Record:

- Browser
- Version

Example:

Firefox 152

Chrome 140

---

# Platform Validation

Record:

- Operating System
- Architecture

Examples:

Ubuntu 24.04

Windows 11

macOS

Future automation may collect this automatically.

---

# Certification Result

One result shall be recorded.

PASS

FAIL

BLOCKED

Only PASS authorizes engineering work.

---

# Failure Classification

Environment failures shall be classified as one of:

- Repository
- Virtual Environment
- Dependency
- Configuration
- Secret
- Network
- External Service
- Platform
- Infrastructure
- Unknown

---

# Required Evidence

Every certification shall include:

- Commands Executed
- Actual Results
- Observations
- Root Cause (if failure)
- Resolution (if applicable)
- Verification Evidence

---

# Ownership

Developer

Responsible for creating a reproducible environment.

---

Orion

Responsible for validating the environment before implementation.

Responsible for restoring the environment if implementation introduces environment issues.

---

Product Owner

Responsible for confirming Environment Certification before beginning Business UAT.

---

Athena

Responsible for reviewing Environment Certification evidence when required.

---

# Engineering Principle

Engineering work shall never begin on an uncertified environment.

A reproducible engineering environment is part of the engineering deliverable.

---

# Relationship to Other Standards

This document defines the Environment Certification process.

Other standards may reference this document without duplicating its contents.

Examples:

- PRODUCT_OWNER_UAT_STANDARD.md
- HCA_PLAYBOOK.md
- ATHENA_CPS_CLOSURE_STANDARD.md
- Future CI/CD Standards
- Future HULK Engineering Standards

---

# Future Evolution

Future versions may automate certification using:

- HULK
- Orion
- Git Hooks
- CI/CD Pipelines
- Repository Health Checks
- Local Model Validation
- Infrastructure Validation

Automation shall verify compliance but shall not replace engineering judgment.

---

# Decision

Environment Certification is adopted as a mandatory engineering standard for all Selten repositories.

Engineering execution may begin only after Environment Certification has passed.