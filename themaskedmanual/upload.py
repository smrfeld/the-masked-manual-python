from google.cloud import storage
import os

def upload_to_google_cloud_storage():
    
    # Client
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fname = os.path.join(dir_path, 'the-masked-manual-4a1f9306ddf1.json')
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


