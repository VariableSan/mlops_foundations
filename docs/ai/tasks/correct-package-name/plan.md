# Plan

1. Map references and environment read-only (analyst); record baseline.
2. Add focused unittest tests before production edits (test writer owns tests/).
   Confirm missing corrected package and current API call fail for expected reasons.
3. Rename source and references, correct API callable import, update local lock metadata
   (implementer owns source/, manifests, Makefile and existing project docs).
4. Write English AGENTS.md and Russian lesson guide (main agent, after implementation).
5. Run unittest suite, quality gate, explicit test lint, docs validation. Delegate read-only
   review and independent verification. Fix only actionable findings; report limits.

All writes are sequential in the user's checkout. Do not overwrite existing lesson work.
