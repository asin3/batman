# PRODUCT OWNER UAT STANDARD

Version: 1.0

Status: Active

Owner: Athena

---

# Purpose

This document defines the standard process for Product Owner User Acceptance Testing (UAT).

The objective of Product Owner UAT is to validate that the implemented functionality satisfies the approved business requirements before merge approval.

Product Owner UAT validates business behaviour.

It does not replace engineering testing.

---

# Mandatory UAT Package

Every CPS entering Product Owner UAT shall include a UAT Package prepared by Orion.

The Product Owner shall not begin UAT until the UAT Package has been delivered.

Purpose

The UAT Package provides the Product Owner with a consistent testing guide and ensures that UAT validates the approved business scope rather than implementation assumptions.

Mandatory Contents

Every UAT Package shall contain:

1. CPS Information
   - CPS ID
   - Title
   - Repository
   - Branch
   - Version

2. Scope Under Test

3. Out of Scope

4. Preconditions

5. Test Environment

6. Product Owner Test Cases

For every test case:

- Test ID
- Business Scenario
- Steps
- Expected Result
- Actual Result (Product Owner)
- Pass / Fail

7. Regression Checklist

8. Known Limitations

9. UAT Completion Criteria

10. UAT Result Summary

Standard Location

docs/reviews/

Naming Convention

<date>_uat_package_<cps-id>.md

Example

2026-07-20_uat_package_cps002.md

Responsibility

Orion
- Prepare the UAT Package.

Product Owner
- Execute the UAT.
- Record actual results.
- Record Pass / Fail.
- Report business observations.

Athena
- Review UAT outcome.
- Determine CPS Closure readiness.

---

# Responsibilities

## Orion

Responsible for preparing the UAT Package.

Shall provide:

- Branch
- Setup Instructions
- Test Data
- Test Steps
- Expected Results
- Rollback Procedure

---

## Product Owner

Responsible for:

- Executing UAT
- Recording observations
- Reporting defects
- Approving business functionality

The Product Owner shall not modify source code during UAT.

---

## Athena

Responsible for:

- Reviewing Product Owner findings
- Determining merge readiness
- Issuing the Green Light for Merge

---

# Preconditions

Before Product Owner UAT begins, the following must exist:

✓ Green Light for Product Owner UAT

✓ Approved Implementation Branch

✓ Implementation Report

✓ Athena Implementation Review

✓ UAT Package

If any prerequisite is missing:

STOP.

Do not begin UAT.

---

# Phase 0 – Environment Certification

Before Product Owner UAT begins, execute Environment Certification according to:

docs/hca/ENVIRONMENT_CERTIFICATION_STANDARD.md

Product Owner UAT shall begin only after Environment Certification returns:

PASS

---

## Certification Checks

Execute all validation checks defined in ENVIRONMENT_CERTIFICATION_STANDARD.md:

- Repository Validation
- Python Environment Validation
- Python Runtime Validation
- Dependency Validation
- Secrets Validation
- Data Validation
- External Service Validation
- Browser Validation
- Platform Validation

Record the result and supporting evidence according to the Environment Certification Standard.

PASS

or

CONDITIONALLY CERTIFIED
(as approved by Athena)

---

# Environment Failure Rules

If an Environment Certification check fails:

Do not execute business test cases.

Do not classify the issue as an application defect.

Record the issue as an Environment Blocker.

Environment blockers shall be resolved before Product Owner UAT resumes.

---

# UAT Workspace

Every UAT execution shall create one UAT Report.

Storage Location:

docs/uat/

Naming Convention:

YYYY-MM-DD_product_owner_uat_<short_description>.md

Example:

2026-07-20_product_owner_uat_google_auth.md

---

# UAT Report Structure

Every Product Owner UAT shall produce one UAT Report.

The report shall contain the following sections.

1. UAT Information

- Date
- Time
- Tester
- Repository
- Branch
- CPS
- Sprint Workspace

2. Environment Certification Summary

PASS / FAIL / BLOCKED

Reference the Environment Certification record.

3. Test Execution Log

For every test record:

- Test Number
- Test Name
- Expected Result
- Actual Result
- Status
- Observation

4. Defects

List every defect discovered during UAT.

5. General Observations

Record usability, documentation, workflow or engineering observations that are not application defects.

6. Screenshots

Attach evidence for:

- FAIL
- BLOCKED
- Unexpected Behaviour

7. UAT Summary

Total Tests

Passed

Failed

Blocked

Not Executed

8. Product Owner Recommendation

PASS

PASS WITH OBSERVATIONS

FAIL

9. Next Action

Examples:

- Proceed to Athena Merge Readiness Review
- Return to Orion for correction
- Execute Partial Retest

---

# Test Execution Rules

Execute every test case in the supplied UAT Package.

Do not skip test cases.

Execute tests in sequence.

If a critical failure occurs:

Continue only if remaining tests are independent.

Otherwise stop and notify Athena.

---

# UAT Scope Freeze

Once Product Owner UAT has started, the implementation under test is frozen.

During Product Owner UAT:

- No source code modifications are permitted.
- No dependency changes are permitted.
- No repository changes are permitted.
- No architectural changes are permitted.

Only Product Owner observations, UAT evidence, and defect reports may be added.

If any implementation change becomes necessary:

1. Suspend Product Owner UAT.
2. Return the CPS to Orion.
3. Implement the required changes.
4. Repeat Athena Implementation Review.
5. Produce a new Environment Certification.
6. Restart Product Owner UAT.

Product Owner UAT shall always validate one fixed implementation baseline.

---

# Recording Test Results

Every executed test shall record:

- Test Number
- Test Name
- Expected Result
- Actual Result
- Status
- Execution Time
- Tester
- Remarks

Status values:

PASS

FAIL

BLOCKED

NOT EXECUTED

Screenshots shall be attached for:

- Every FAIL
- Every BLOCKED
- Any unexpected behaviour

Screenshots shall follow the naming convention:

TEST-<Number>_<Status>.png

Examples:

TEST-01_FAIL.png

TEST-04_BLOCKED.png

---

# Defect Recording

Every defect shall include:

- Defect ID
- Test Number
- Severity
- Description
- Steps to Reproduce
- Expected Behaviour
- Actual Behaviour
- Screenshot (if applicable)

Severity Levels

Critical

High

Medium

Low

---

# Issue Classification

Every observation recorded during UAT shall be classified.

Categories include:

- Environment
- Configuration
- Authentication
- Authorization
- Business Logic
- User Interface
- Navigation
- Performance
- Security
- Data Migration
- Regression
- Documentation
- Deployment
- Infrastructure
- Unknown

This classification assists future RCA Knowledge Extraction and Engineering Memory.

---

# UAT Summary

Every UAT Report shall conclude with:

Total Tests

Passed

Failed

Blocked

Not Executed

Overall Recommendation

PASS

or

FAIL

---

# UAT Decision

If all business-critical functionality passes:

Recommendation:

PASS

Athena may begin Merge Readiness Review.

If critical business issues remain:

Recommendation:

FAIL

Athena shall not issue Merge Approval.

---

# Engineering Lifecycle

Implementation

↓

Implementation Report

↓

Implementation Review Evidence

↓

Athena Implementation Review

↓

Environment Certification

↓

Green Light for Product Owner UAT

↓

Product Owner UAT

↓

Athena UAT Review

↓

Athena CPS Closure

↓

Merge Readiness Review

↓

Green Light for Merge

↓

Merge

---

# Guiding Principles

Product Owner UAT validates business value.

Engineering testing validates technical correctness.

Both approvals are mandatory before merge.

----