from google.cloud import aiplatform


PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "asia-south1"

INDEX_DISPLAY_NAME = "ai-document-intelligence-index"


def create_vector_index():
    aiplatform.init(
        project=PROJECT_ID,
        location=LOCATION,
    )

    index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name=INDEX_DISPLAY_NAME,
        dimensions=3072,
        approximate_neighbors_count=10,
        leaf_node_embedding_count=500,
        leaf_nodes_to_search_percent=10,
        index_update_method="STREAM_UPDATE",
        distance_measure_type="COSINE_DISTANCE",
        description="Vector index for AI Document Intelligence",
    )

    print("Vector index created.")
    print("Index name:", index.resource_name)

    return index


if __name__ == "__main__":
    print(create_vector_index())
