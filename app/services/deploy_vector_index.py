from google.cloud import aiplatform


PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "asia-south1"

INDEX_ID = "projects/991086939141/locations/asia-south1/indexes/8415600426346348544"
ENDPOINT_ID = "projects/991086939141/locations/asia-south1/indexEndpoints/3125401384371879936"

DEPLOYED_INDEX_ID = "document_index_v1"


def deploy_index():
    aiplatform.init(
        project=PROJECT_ID,
        location=LOCATION,
    )

    index = aiplatform.MatchingEngineIndex(
        index_name=INDEX_ID
    )

    endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=ENDPOINT_ID
    )

    endpoint.deploy_index(
        index=index,
        deployed_index_id=DEPLOYED_INDEX_ID,
        display_name="document-index-v1",
        machine_type="e2-standard-16",
    )

    print("Index deployed successfully.")
    print("Endpoint:", endpoint.resource_name)
    print("Deployed index ID:", DEPLOYED_INDEX_ID)


if __name__ == "__main__":
    deploy_index()