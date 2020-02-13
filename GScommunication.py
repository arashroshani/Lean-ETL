from google.cloud import storage
import datetime


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    return blob.public_url

if __name__ == "__main__":
    upload_blob(
        bucket_name='arashdataproject',
        source_file_name='map.png',
        destination_blob_name='map' + ' _ ' + str(datetime.datetime.utcnow()),
    )
