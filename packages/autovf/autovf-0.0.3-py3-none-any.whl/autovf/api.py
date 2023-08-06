import os

from fastapi import FastAPI

from .predict import AutoVFPredict


app = FastAPI()
axgp = AutoVFPredict(model_path=os.environ.get("AUTOVF_MODEL_PATH"))
schema = axgp.get_prediction_schema()


@app.post("/predict")
def predict(sample: schema):
    sample = sample.json()
    return axgp.predict_single(sample)
