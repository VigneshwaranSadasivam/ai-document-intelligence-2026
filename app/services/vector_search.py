# import math


# def cosine_similarity(
#     vector_a: list[float],
#     vector_b: list[float],
# ) -> float:
#     dot_product = sum(
#         a * b
#         for a, b in zip(vector_a, vector_b)
#     )

#     magnitude_a = math.sqrt(
#         sum(a * a for a in vector_a)
#     )

#     magnitude_b = math.sqrt(
#         sum(b * b for b in vector_b)
#     )

#     if magnitude_a == 0 or magnitude_b == 0:
#         return 0.0

#     return dot_product / (magnitude_a * magnitude_b)


# def search_similar_chunks(
#     query_embedding: list[float],
#     chunks: list[dict],
#     top_k: int = 3,
# ) -> list[dict]:

#     results = []

#     for chunk in chunks:
#         similarity = cosine_similarity(
#             query_embedding,
#             chunk["embedding"],
#         )

#         results.append({
#             "chunk_id": chunk["chunk_id"],
#             "page": chunk["page"],
#             "text": chunk["text"],
#             "similarity": similarity,
#         })

#     results.sort(
#         key=lambda item: item["similarity"],
#         reverse=True,
#     )

#     return results[:top_k]

from google.cloud import aiplatform
from google.cloud.aiplatform_v1.types import IndexDatapoint
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
from app.services.firestore import get_chunks_by_ids


PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "asia-south1"

INDEX_ID = "projects/991086939141/locations/asia-south1/indexes/8415600426346348544"
ENDPOINT_ID = "projects/991086939141/locations/asia-south1/indexEndpoints/3125401384371879936"

DEPLOYED_INDEX_ID = "document_index_v1"


def get_vector_endpoint():
    aiplatform.init(
        project=PROJECT_ID,
        location=LOCATION,
    )

    return aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=ENDPOINT_ID
    )


def upsert_chunks(chunks: list[dict]):
    if not chunks:
        raise ValueError(
            "No chunks with embeddings were provided to Vector Search."
        )

    aiplatform.init(
        project=PROJECT_ID,
        location=LOCATION,
    )

    index = aiplatform.MatchingEngineIndex(
        index_name=INDEX_ID
    )

    datapoints = []

    for chunk in chunks:
        print(
            "Upserting:",
            chunk["chunk_id"],
            "document_id:",
            chunk["document_id"],
        )

        datapoints.append(
            IndexDatapoint(
                datapoint_id=chunk["chunk_id"],
                feature_vector=chunk["embedding"],
                restricts=[
                    IndexDatapoint.Restriction(
                        namespace="document_id",
                        allow_list=[chunk["document_id"]],
                    )
                ],
            )
        )

    print("Datapoints to upsert:", len(datapoints))

    index.upsert_datapoints(
        datapoints=datapoints,
    )


    return {
        "count": len(datapoints),
        "status": "upserted",
    }

def search_vector_index(
    query_embedding: list[float],
    document_id: str,
    top_k: int = 3,
):
    endpoint = get_vector_endpoint()

    document_filter = [
        Namespace(
            name="document_id",
            allow_tokens=[document_id],
            deny_tokens=[],
        )
    ]

    print("Filter namespace:", document_filter[0].name)
    print("Filter token:", document_filter[0].allow_tokens)

    results = endpoint.find_neighbors(
        deployed_index_id=DEPLOYED_INDEX_ID,
        queries=[query_embedding],
        num_neighbors=top_k,
        filter=document_filter,
    )

    print("Filtered Vector Search results:", results)

    if not results:
        return []

    return results[0]

def retrieve_relevant_chunks(
    document_id: str,
    query_embedding: list[float],
    top_k: int = 3,
) -> list[dict]:

    results = search_vector_index(
        query_embedding=query_embedding,
        document_id=document_id,
        top_k=top_k,
    )

    chunk_ids = [
        result.id
        for result in results
    ]

    chunks = get_chunks_by_ids(
        document_id=document_id,
        chunk_ids=chunk_ids,
    )

    distance_map = {
        result.id: result.distance
        for result in results
    }

    for chunk in chunks:
        chunk["distance"] = distance_map.get(
            chunk["chunk_id"]
        )

    chunks.sort(
        key=lambda chunk: chunk["distance"]
    )

    return chunks