# MLOps Foundations

## Purpose
Educational Python 3.12 project for learning an end-to-end ML workflow: train a
student placement classifier, persist it, and serve predictions through FastAPI.
Based on Cookiecutter Data Science v2; this is a local learning project.

## Layout and entry points
- `mlops_foundations/`: importable application package.
- `modeling/train.py`: train a RandomForestClassifier from
  `data/raw/student_placement_data_v1.csv`; target: `Placement`.
- `modeling/predict.py`: prediction function `main`; cached model loader.
- `api.py`: FastAPI `app`; `GET /` and `POST /predict` with a `data` dictionary.
- Features: `CGPA`, `IQ`, `Profile Score`, in training-column order.
- `config.py`: project-relative paths and dotenv setup.
- `models/model.pkl`: trained artifact. `tests/`: unittest regression tests.
- `docs/`: MkDocs documentation and task specifications.

## Environment and commands
Run from the repository root. Project dependencies are declared in `pyproject.toml`
and locked in `uv.lock`. Do not add dependencies without the user's approval.

```bash
uv sync --locked
.venv/bin/python -m unittest discover -s tests -v
PATH="$PWD/.venv/bin:$PATH" make lint
.venv/bin/python -m ruff check --isolated --select E,F,I --line-length 99 tests
.venv/bin/python -m ruff format --isolated --line-length 99 --check tests
# Requires FastAPI, Uvicorn and ML dependencies in the same environment:
.venv/bin/python -m uvicorn mlops_foundations.api:app --reload
```

Use `uv add <package>` to add an approved dependency and update the lockfile.

## Working rules
- Inspect Git status and preserve the learner's uncommitted work.
- Keep changes small and explain how they support the current lesson.
- Keep package names, imports, metadata, commands and documentation consistent.
- Add regression tests before changing behavior; run tests and lint before reporting success.
- Avoid reading `.env` or credentials. Tests must disable dotenv loading.
- Use temporary fixtures for tests; do not overwrite datasets, models or logs.
- Training overwrites `models/model.pkl`; run it only when requested.
- Load only trusted joblib/pickle artifacts; do not deserialize the learner's model for tests.
- Restart the API after retraining: the model cache is local to each process.
- Do not commit, push or deploy unless explicitly requested. Report validation limits.
