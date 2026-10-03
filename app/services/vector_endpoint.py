from google.cloud import aiplatform


PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "asia-south1"

ENDPOINT_DISPLAY_NAME = "ai-document-intelligence-endpoint"


def create_index_endpoint():
    aiplatform.init(
        project=PROJECT_ID,
        location=LOCATION,
    )

    endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
        display_name=ENDPOINT_DISPLAY_NAME,
        description="Vector Search endpoint for AI Document Intelligence",
        public_endpoint_enabled=True,
    )

    print("Index endpoint created.")
    print("Endpoint name:", endpoint.resource_name)

    return endpoint


if __name__ == "__main__":
    create_index_endpoint()