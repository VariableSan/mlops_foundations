"""Verify that installing the project declares the dependencies it needs."""

import re
import unittest
from importlib.metadata import requires


class ProjectDependencyTests(unittest.TestCase):
    def test_project_declares_runtime_and_tool_dependencies(self):
        requirements = requires("mlops-foundations")
        self.assertIsNotNone(requirements)
        names = {
            re.split(r"[\[<>=!~;\s]", requirement, maxsplit=1)[0].lower()
            for requirement in requirements
        }
        expected = {
            "fastapi",
            "joblib",
            "loguru",
            "mkdocs",
            "pandas",
            "pip",
            "python-dotenv",
            "ruff",
            "scikit-learn",
            "tqdm",
            "typer",
            "uvicorn",
        }
        self.assertEqual(expected - names, set(), "Project dependencies are missing")
        self.assertTrue(
            any(
                requirement.lower().startswith("uvicorn[standard]") for requirement in requirements
            ),
            "Uvicorn must include the standard extra",
        )
