from pathlib import Path

import joblib
from loguru import logger
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import typer

from mlops_foundations.config import MODELS_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    raw_dataset: Path = RAW_DATA_DIR / "student_placement_data_v1.csv",
    models_dir: Path = MODELS_DIR,
):
    df = pd.read_csv(raw_dataset)

    X = df.drop("Placement", axis=1)
    y = df["Placement"]

    model = RandomForestClassifier()
    model.fit(X, y)

    models_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, models_dir / "model.pkl")

    logger.info("Model trained on student placement dataset")


if __name__ == "__main__":
    app()
