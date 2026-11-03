"""Exercise the public package and API without user data, models, or dotenv files."""

import importlib
import importlib.util
import json
import logging
import os
import sys
import unittest
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

PACKAGE = "mlops_foundations"
ROOT = Path(__file__).resolve().parents[1]


class PackageNameTests(unittest.TestCase):
    def test_corrected_package_is_available(self):
        self.assertIsNotNone(
            importlib.util.find_spec(PACKAGE),
            "The project must expose the corrected mlops_foundations package name",
        )


class PredictionApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if importlib.util.find_spec(PACKAGE) is None:
            raise unittest.SkipTest(
                "API tests require the corrected package; see package-name test"
            )
        cls.resources = ExitStack()
        cls.addClassCleanup(cls.resources.close)
        folder = Path(cls.resources.enter_context(TemporaryDirectory()))
        previous_cwd = Path.cwd()
        previous_handlers = set(logging.getLogger().handlers)
        cls.resources.callback(os.chdir, previous_cwd)
        cls.resources.callback(cls.close_new_log_handlers, previous_handlers)
        os.chdir(folder)
        cls.resources.enter_context(patch.object(sys, "path", [str(ROOT), *sys.path]))
        cls.resources.enter_context(patch("dotenv.load_dotenv"))
        cls.predict = importlib.import_module(f"{PACKAGE}.modeling.predict")
        cls.api = importlib.import_module(f"{PACKAGE}.api")
        cls.resources.callback(cls.predict.load_model.cache_clear)

        # A tiny deterministic classifier, never the user's model.pkl or training data.
        model = RandomForestClassifier(n_estimators=1, random_state=0)
        model.fit(pd.DataFrame({"score": [0, 0, 1, 1]}), [0, 0, 1, 1])
        model_path = folder / "fixture.pkl"
        joblib.dump(model, model_path)
        cls.model = cls.predict.load_model(model_path)

    @staticmethod
    def close_new_log_handlers(previous_handlers):
        root_logger = logging.getLogger()
        for handler in set(root_logger.handlers) - previous_handlers:
            root_logger.removeHandler(handler)
            handler.close()

    def request(self, method, path, payload=None):
        # Direct handlers avoid optional HTTP clients and server/threadpool dependencies.
        from fastapi import HTTPException

        try:
            if (method, path) == ("GET", "/"):
                response = self.api.home()
            else:
                response = self.api.get_prediction(self.api.InputData(**payload))
            return 200, json.loads(json.dumps(response))
        except HTTPException as exc:
            return exc.status_code, {"detail": exc.detail}
        except TypeError as exc:
            self.fail(f"The API must call the prediction function successfully: {exc}")

    def test_prediction_function_returns_python_scalar(self):
        with patch.object(self.predict, "load_model", return_value=self.model):
            result = self.predict.main({"score": 1})
        self.assertEqual(result, 1)
        self.assertIs(type(result), int)

    def test_predict_returns_scalar_from_real_prediction_function(self):
        with patch.object(self.predict, "load_model", return_value=self.model):
            status, body = self.request("POST", "/predict", {"data": {"score": 1}})
        self.assertEqual(status, 200)
        self.assertEqual(body, {"prediction": 1})

    def test_empty_features_return_400(self):
        with patch.object(self.predict, "load_model", return_value=self.model):
            status, body = self.request("POST", "/predict", {"data": {}})
        self.assertEqual(status, 400)
        self.assertIn("cannot be empty", body["detail"])

    def test_invalid_features_return_400(self):
        with patch.object(self.predict, "load_model", return_value=self.model):
            status, body = self.request("POST", "/predict", {"data": {"score": "invalid"}})
        self.assertEqual(status, 400)
        self.assertTrue(body["detail"])

    def test_missing_model_returns_503(self):
        with patch.object(self.predict, "load_model", side_effect=FileNotFoundError("No model")):
            status, body = self.request("POST", "/predict", {"data": {"score": 1}})
        self.assertEqual(status, 503)
        self.assertEqual(body, {"detail": "No model"})

    def test_health_is_available_without_model(self):
        with patch.object(self.predict, "load_model", side_effect=FileNotFoundError("No model")):
            self.assertEqual(self.request("GET", "/"), (200, {"message": "ML API running"}))
