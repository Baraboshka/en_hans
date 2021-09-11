import os
from google.cloud import storage

def init_bucket():
    gcs_credentials = os.path.abspath('gcs.json')
    gcs_bucket = 'en-hans'
    client: storage.Client = storage.Client.from_service_account_json(gcs_credentials)
    return client.bucket(gcs_bucket)