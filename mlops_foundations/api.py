import logging
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from mlops_foundations.modeling.predict import main as predict

app = FastAPI()

os.makedirs("logs", exist_ok=True)

logging.basicConfig(filename="logs/predictions.log", level=logging.INFO)
logger = logging.getLogger(__name__)


class InputData(BaseModel):
    data: dict


@app.get("/")
def home():
    return {"message": "ML API running"}


@app.post("/predict")
def get_prediction(input: InputData):
    try:
        result = predict(input.data)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    logger.info("prediction_request=%s prediction=%s", input.data, result)

    return {"prediction": result}
