# CPS Classification Protocol

## CPS Types

Every CPS must be classified as one of two types.

### FOUNDATION CPS

A Foundation CPS creates or fundamentally changes a Batman capability, architectural layer, or product flow.

At the beginning of a Foundation CPS, define:

- Business Flow
- Advantage
- Disadvantage / Risk

These business details are stated once at CPS initiation and must not be repeated in every implementation response.

### CHANGE CPS

A Change CPS performs a fix, validation, cleanup, normalization, refactor, or limited extension within an existing capability.

Change CPS responses must move directly to implementation.

Business Flow, Advantage, and Disadvantage / Risk are not required unless the change materially alters the product or architecture.

## Rule

Do not classify CPS work using Major, Minor, Mid-Major, or similar subjective levels.

Use only:

FOUNDATION CPS
CHANGE CPS

When a Change CPS grows into a new capability or materially changes the business flow, it must be reclassified as a Foundation CPS before implementation continues.