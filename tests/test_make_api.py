"""Verify the documented API launch commands without starting a server."""

import shlex
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MakeApiTests(unittest.TestCase):
    def test_api_targets_launch_uvicorn_with_expected_reload_mode(self):
        for target, reload_enabled in (("api-dev", True), ("api-prod", False)):
            with self.subTest(target=target):
                result = subprocess.run(
                    ["make", "--dry-run", target],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                command = shlex.split(result.stdout)
                self.assertEqual(
                    command[:6],
                    ["uv", "run", "--locked", "python", "-m", "uvicorn"],
                )
                self.assertIn("mlops_foundations.api:app", command)
                self.assertEqual("--reload" in command, reload_enabled)
