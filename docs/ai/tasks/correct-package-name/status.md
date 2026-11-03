# Status

Phase: specification / tests next.

- Read root/parent instructions, manifests, source and current Git changes.
- Baseline make lint exit 0; no existing tests found.
- Read-only isolated handler probe reproduced module-not-callable; function alias passed.
- Dataset header verified: CGPA, IQ, Profile Score, Placement; 100 rows. No records printed.
- User explicitly added package rename to scope. Preserve uncommitted source and model.
- No dependency installs or server startup performed.

## Red and green
- New test suite before implementation: `.venv/bin/python -m unittest discover -s tests -v`
  exit 1: corrected package unavailable (assertion, not a test import error).
- Diagnostic suite against old package: exit 1; four handler failures with
  `'module' object is not callable`; real predictor and health passed.
- Initial direct ASGI diagnostics hung and were interrupted (130). Final regression
  suite calls handlers directly; live HTTP/route behavior remains a manual check.
- Source renamed and references corrected, including local uv.lock entry. API now
  imports the callable. Existing training/prediction bodies and model preserved.
- `UV_CACHE_DIR=/tmp/mlops-foundations-uv-cache uv lock --offline`: exit 0.
- `.venv/bin/python -m unittest discover -s tests -v`: exit 0, 7 tests passed.
- `PATH="$PWD/.venv/bin:$PATH" make lint`: exit 0, 9 files formatted and Ruff passed.
- Tests need isolated Ruff settings because project include excludes tests. The
  agreed format line length is 99. An exploratory check using default 88 failed;
  no tests were weakened or changed for this check.
- English AGENTS.md added; Russian lesson note written in the learning vault.
- Phase: independent review and final verification. No installs or server startup.

## Final verification
- Independent verifier: unittest exit 0, 7 passed, 0 skipped; make lint exit 0;
  isolated Ruff check tests exit 0; isolated Ruff format check tests exit 0.
- Independent reviewer repeated the same commands: all exit 0. No actionable findings.
- Complete tracked diff and untracked package/tests/instructions inspected. Package,
  Makefile, pyproject, MkDocs and README references agree. Local lock entry matches.
- `git diff --check`: exit 0. Lesson + AGENTS syntax/links/frontmatter/whitespace
  Python validation: exit 0 (10 Bash blocks, 3 Python blocks, 1 JSON example).
- Russian lesson frontmatter and existing Navigation link preserved.
- No dependencies installed; Uvicorn remains absent. Manual: install the lesson's
  dependencies, refresh editable installation after rename, start Uvicorn, check
  GET /, /docs, POST /predict success/400/422 and the log file using the trusted model.
- Fresh-install reproducibility remains limited: runtime dependencies are not yet
  declared in requirements.txt and there are no pinned runtime versions. The guide
  provides explicit install commands and the missing requirements lines.
- Complete. No model/data changes, commits, pushes or deployment.
