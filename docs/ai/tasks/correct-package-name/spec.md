# Correct package name and document the ML workflow

## Goal and acceptance criteria
- [x] The Python package is importable as `mlops_foundations` from the project root.
- [x] Package metadata, imports, Makefile, MkDocs and README reference the corrected name.
- [x] The existing local-package lock entry agrees with the renamed project.
- [x] POST /predict invokes the prediction function and preserves the response and 400/503 mapping.
- [x] Existing training/prediction logic, data and model artifacts are preserved.
- [x] An English root AGENTS.md explains purpose, layout, dependency workflow and validation.
- [x] The Russian lesson note explains training, prediction, caching, API, installation, requests and logs for this repository.

## Current evidence
The user has uncommitted training/prediction implementations, api.py and models/model.pkl.
The source directory is misspelled mlops_foundtations. api.py imports the prediction module
then calls it, causing TypeError: module object is not callable. Dependencies currently live
in requirements.txt, not project.dependencies. Uvicorn, pytest and httpx are absent locally.
Baseline `PATH="$PWD/.venv/bin:$PATH" make lint`: exit 0 (9 files formatted; Ruff passed).

## Scope
Rename the source directory and references, correct the API callable import, add focused
stdlib unittest tests, project instructions and lesson documentation. Updating only the
local project name in uv.lock is part of the rename; no dependency versions change.
Do not install/upgrade dependencies, migrate dependency management, train a model, load
existing model.pkl, change data, read secrets, commit, push, or deploy. Keep the current
checkout because the task explicitly concerns the user's uncommitted lesson work.

## Behavior and edge cases
Preserve / health response and /predict JSON shape. Keep ValueError -> 400 and missing
model -> 503. The health endpoint does not guarantee model availability. Model cache
requires restart/explicit invalidation after retraining. Package rename is intentionally
breaking for the old import name; document editable reinstall. Do not rename artifacts.

## Validation
Use `.venv/bin/python -m unittest discover -s tests -v` for package import and ASGI contract
checks with a temporary fixture model, never the user's model. Disable dotenv loading in
tests, isolate logs in a temporary cwd, restore patches. Use no new test dependencies.
Run `PATH="$PWD/.venv/bin:$PATH" make lint` as the existing quality gate and explicit Ruff
checks for new tests. Validate lesson code-block syntax, links and preserved frontmatter.
Manually installing Uvicorn and testing a live server remains necessary if unavailable.

## Assumptions
No compatibility alias for the typo is needed. The task does not request a dependency
installation; provide precise commands and persistent requirements.txt additions instead.
