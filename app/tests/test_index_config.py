from google.cloud import aiplatform

PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "asia-south1"

INDEX_ID = (
    "projects/991086939141/"
    "locations/asia-south1/"
    "indexes/8415600426346348544"
)

aiplatform.init(
    project=PROJECT_ID,
    location=LOCATION,
)

index = aiplatform.MatchingEngineIndex(
    index_name=INDEX_ID
)

print("Index:", index.resource_name)
print("Display name:", index.display_name)

index_resource = index._gca_resource

print("Index config:")
print(index_resource)