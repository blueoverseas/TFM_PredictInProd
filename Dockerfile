FROM python:3.8.12-buster

COPY TFM_PredictInProd/model.joblib /model.joblib
COPY TFM_PredictInProd/TaxiFareModel /TaxiFareModel
COPY TFM_PredictInProd/api/fast.py /fast.py
COPY TFM_PredictInProd/requirements.txt /requirements.txt
COPY gcp/neural-gantry-340415-1d47b099bdcd.json /credentials.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn fast:app --reload --host 0.0.0.0 --port $PORT
