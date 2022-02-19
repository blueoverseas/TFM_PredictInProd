import os
import joblib
from google.cloud import storage
from termcolor import colored
from TaxiFareModel.params import BUCKET_NAME, MODEL_NAME, MODEL_VERSION, PATH_TO_LOCAL_MODEL


def storage_upload(rm=False):
    client = storage.Client().bucket(BUCKET_NAME)

    local_model_name = 'model.joblib'
    storage_location = f"models/{MODEL_NAME}/{MODEL_VERSION}/{local_model_name}"
    blob = client.blob(storage_location)
    blob.upload_from_filename('model.joblib')
    print(colored(f"=> model.joblib uploaded to bucket {BUCKET_NAME} inside {storage_location}",
                  "green"))
    if rm:
        os.remove('model.joblib')

def download_model(bucket=BUCKET_NAME, rm=True):
    client = storage.Client().bucket(bucket)
    storage_location = f'models/{MODEL_NAME}/{MODEL_VERSION}/{PATH_TO_LOCAL_MODEL}'
    blob = client.blob(storage_location)
    blob.download_to_filename(PATH_TO_LOCAL_MODEL)
    print("=> pipeline downloaded from storage")
    model = joblib.load(PATH_TO_LOCAL_MODEL)
    if rm:
        os.remove(PATH_TO_LOCAL_MODEL)
    return model
