# ADR-001: Desktop First Architecture

**Status:** Accepted

**Date:** 2026-06-25

---

# Context

Batman Student is an AI-powered learning platform being developed incrementally, starting with ICSE Class 10 Physics.

During the early stages of development, rapid experimentation, frequent architecture changes, OCR improvements, retrieval tuning, and LLM evaluations are expected. Cloud deployment at this stage would unnecessarily increase complexity, operational cost, and debugging effort.

Therefore, the project requires a local-first architecture that allows fast iteration while keeping the entire knowledge base under the developer's control.

---

# Decision

Batman Student shall follow a **Desktop-First Architecture** throughout Product 1.0.

All core services shall execute locally:

* User Interface
* Knowledge Storage
* Vector Database
* Student Data
* Governance
* OCR Pipeline
* Retrieval Engine

External AI models (OpenAI and Gemini) may be accessed through APIs, but all project knowledge shall remain local.

---

# Scope

This decision applies to:

* Product 1.0
* ICSE Class 10
* Single-user development
* Local Windows environment

---

# Architecture

Student

↓

Batman Student

↓

Local Knowledge Engine

├── OCR

├── Text Processing

├── Vector Database

├── Governance

├── Student Memory

├── Question Bank

└── Progress Engine

↓

Provider Router

├── OpenAI

└── Gemini

---

# Benefits

* Fast development cycle
* Complete ownership of data
* Offline knowledge storage
* Easy debugging
* Low infrastructure cost
* Simple backups
* Easy migration to cloud

---

# Consequences

The application is initially limited to a desktop environment.

Cloud synchronization, multi-device access, and collaborative features are intentionally deferred until later phases.

---

# Future Expansion

Desktop First does **not** mean Desktop Only.

Future versions may introduce:

* Cloud Synchronization
* Web Application
* Mobile Application
* Parent Portal
* Teacher Portal

These additions must extend—not replace—the Desktop architecture.

---

# Principles

* Knowledge remains local.
* Student data remains local.
* AI providers are replaceable.
* Cloud services are optional.
* Desktop remains the primary development platform.

---

# Status

Accepted.

Frozen for Product 1.0.
