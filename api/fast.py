from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime
import pytz
import joblib
from TaxiFareModel.params import PATH_TO_LOCAL_MODEL
from TaxiFareModel.gcp import download_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/predict")
def predict(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count):
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)  # localize the user datetime with NYC timezone
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)    # localize the datetime to UTC
    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")

    X_pred = pd.DataFrame({
                            "key": ['2013-07-06 17:18:00.000000119'],
                            "pickup_datetime": [formatted_pickup_datetime],
                            "pickup_longitude": [float(pickup_longitude)],
                            "pickup_latitude": [float(pickup_latitude)],
                            "dropoff_longitude": [float(dropoff_longitude)],
                            "dropoff_latitude": [float(dropoff_latitude)],
                            "passenger_count": [int(passenger_count)]
    })
    #pipeline = joblib.load(PATH_TO_LOCAL_MODEL)
    pipeline = download_model()

    y_pred = float(pipeline.predict(X_pred))
    return {"fare": y_pred}

if __name__ == '__main__':
    print(predict('2013-07-06 17:18:00','-73.950655', '40.783282', '-73.984365', '40.769802', '1'))
