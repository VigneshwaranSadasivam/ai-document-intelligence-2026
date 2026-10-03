from google.cloud import aiplatform
from google.cloud.aiplatform_v1.types import IndexDatapoint


PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "asia-south1"

INDEX_ID = (
    "projects/991086939141/locations/asia-south1/"
    "indexes/8415600426346348544"
)

DATAPOINT_ID = "test_stream_001"


aiplatform.init(
    project=PROJECT_ID,
    location=LOCATION,
)

index = aiplatform.MatchingEngineIndex(
    index_name=INDEX_ID
)

datapoint = IndexDatapoint(
    datapoint_id=DATAPOINT_ID,
    feature_vector=[0.0] * 3072,
)

print("Upserting test datapoint...")

index.upsert_datapoints(
    datapoints=[datapoint],
)

print("Upsert request completed.")