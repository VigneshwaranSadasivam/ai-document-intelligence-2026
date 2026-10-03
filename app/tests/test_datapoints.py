from google.cloud import aiplatform


PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "asia-south1"

ENDPOINT_ID = (
    "projects/991086939141/locations/asia-south1/"
    "indexEndpoints/3125401384371879936"
)

DEPLOYED_INDEX_ID = "document_index_v1"

DATAPOINT_ID = "doc_205f49c9_chunk_0001"


aiplatform.init(
    project=PROJECT_ID,
    location=LOCATION,
)

endpoint = aiplatform.MatchingEngineIndexEndpoint(
    index_endpoint_name=ENDPOINT_ID
)

datapoints = endpoint.read_index_datapoints(
    deployed_index_id=DEPLOYED_INDEX_ID,
    ids=[DATAPOINT_ID],
)

for datapoint in datapoints:
    print(datapoint)