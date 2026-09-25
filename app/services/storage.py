import tempfile
from pathlib import Path
from google.cloud import storage

BUCKET_NAME = "ai-document-intelligence-2026-documents"

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

def upload_file_to_gcs(
    file_bytes: bytes,
    document_id: str,
    filename: str,
) -> str:

    blob_path = f"documents/{document_id}_{filename}"

    blob = bucket.blob(blob_path)

    blob.upload_from_string(
        file_bytes,
        content_type="application/pdf",
    )

    return f"gs://{BUCKET_NAME}/{blob_path}"


def download_file_from_gcs(
    gcs_uri: str,
) -> str:

    # Remove gs://
    path = gcs_uri[5:]

    bucket_name, blob_path = path.split("/", 1)

    source_bucket = client.bucket(bucket_name)
    blob = source_bucket.blob(blob_path)

    temp_dir = tempfile.mkdtemp()

    filename = Path(blob_path).name

    local_path = Path(temp_dir) / filename

    blob.download_to_filename(str(local_path))

    return str(local_path)