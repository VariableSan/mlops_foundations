---
name: writing-tdd-tests
description: Use when the user explicitly invokes this skill or requests writing tests or applying TDD in this project.
disable-model-invocation: true
---

# Writing Tests with TDD

Use this workflow only when the user explicitly invokes this skill or asks
for tests or TDD. A request to run existing tests alone does not require
creating or changing tests.

## Workflow

1. Inspect the relevant behavior and existing tests. Define observable
   acceptance criteria and identify the smallest useful regression test.
2. Write the test before changing production behavior. Run it and verify that
   it fails for the expected behavioral reason, not because of a broken
   fixture, syntax error, or missing dependency.
3. Implement the smallest production change that makes the test pass. Run the
   same test again and verify it passes.
4. Refactor if needed without weakening the test. Re-run the targeted test,
   the existing test suite, and the relevant lint checks.
5. Report the commands and results, including the observed red and green
   states. If either state cannot be demonstrated, say so explicitly.

Use `unittest` and the project commands in `AGENTS.md`. Disable dotenv
loading in tests, use temporary fixtures, and never load the learner's
model artifact or overwrite datasets, models, or logs. Preserve uncommitted
work; do not revert it to manufacture a red state.

When asked to add tests for behavior that already exists, verify a meaningful
red state only if a safe, representative pre-change state is available;
otherwise report that red was not observed rather than claiming TDD.
