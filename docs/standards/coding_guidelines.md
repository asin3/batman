# CPS Implementation Rules

## Rule CG-001 — File-First Development (FROZEN)

Before proposing any CPS implementation:

1. Review the latest version of the target source file.
2. Base all changes on the actual implementation, never on assumed code structures.
3. Reference existing variables, functions, and control flow exactly as they exist.
4. Every code insertion must specify an exact location using one of:
   - AFTER:
   - BEFORE:
   - REPLACE:
5. Never reference variables that have not yet been created.
6. Never instruct moving code unless the CPS explicitly includes a refactoring step.
7. Every CPS must compile without requiring architectural fixes from external tools.

If the current source file is unavailable or outdated, request the latest file before generating implementation steps.

## Rule CG-002 — AI Responsibility Boundary (FROZEN)

ChatGPT is responsible for:

- Architecture
- CPS design
- Data models
- Knowledge structures
- Pipeline design
- Business rules
- Integration strategy

GitHub Copilot may be used only for:

- Syntax corrections
- Missing imports
- Indentation
- Variable scope fixes
- IDE/runtime compilation issues

Copilot must not introduce or modify:

- Architecture
- Schemas
- Pipeline stages
- CPS sequence
- Business logic
- Knowledge relationships
- Frozen design decisions

Any architectural suggestion from Copilot must be reviewed and explicitly approved before implementation.