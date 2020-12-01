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

    # Upload
    blob = upload_file(
        bucket=bucket,
        fname_local='data_latest.txt',
        fname_google='data_latest.txt'
        )

    # Make public
    blob.make_public()

    # Also upload and store with date
    today = date.today()
    d1 = today.strftime("%Y_%m_%d")
    blob = upload_file(
        bucket=bucket,
        fname_local='data_latest.txt',
        fname_google='data_%s.txt' % d1
        )
    
    # Upload cache
    fname_local = "cache.tar.gz"
    os.system('tar -czf %s cache' % fname_local)
    blob = upload_file(
        bucket=bucket,
        fname_local=fname_local,
        fname_google='cache_%s.tar.gz' % d1
        )

def upload_file(bucket : storage.bucket, fname_local : str, fname_google : str) -> storage.blob:
    print("Uploading: %s to google cloud storage: %s ...." % (fname_local, fname_google))

    # Blob
    blob = bucket.blob(fname_google)

    # Upload
    blob.upload_from_filename(filename=fname_local)
    print("Uploaded successfully: %s to %s." % (fname_local, fname_google))

    return blob
