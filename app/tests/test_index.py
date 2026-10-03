from google.cloud import aiplatform

PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "asia-south1"

INDEX_ID = (
    "projects/991086939141/locations/asia-south1/"
    "indexes/8415600426346348544"
)

aiplatform.init(
    project=PROJECT_ID,
    location=LOCATION,
)

index = aiplatform.MatchingEngineIndex(
    index_name=INDEX_ID
)

resource = index.gca_resource

print("Vector count:", resource.index_stats.vectors_count)
print("Shard count:", resource.index_stats.shards_count)