from google.cloud import storage
import os
from datetime import date

def upload_to_google_cloud_storage():
    
    # Write JSON credentials
    GCP_CRED = os.getenv('GCP_CRED')
    if GCP_CRED == None:
        print("Error! Could not get environment variable GCP_CRED to write to GCP. Set your service account JSON contents to this variable.")
        return

    fname = "service_account.json"
    f = open(fname,'w')
    f.write(GCP_CRED)
    f.close()

    # Client
    client = storage.Client.from_service_account_json(fname)

    # Bucket
    bucket = client.get_bucket('the-masked-manual-data')

    # Blob
    blob = bucket.blob('data_latest.txt')

    # Upload
    print("Uploading to google cloud storage....")
    blob.upload_from_filename(filename='data_latest.txt')
    print("Uploaded successfully.")

    # Make public
    blob.make_public()

    # Also upload and store with date
    today = date.today()
    d1 = today.strftime("%Y_%m_%d")
    blob_date = bucket.blob('data_%s.txt' % d1)

    # Upload
    print("Uploading backup to google cloud storage....")
    blob_date.upload_from_filename(filename='data_latest.txt')
    print("Uploaded backup successfully.")


