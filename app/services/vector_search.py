import math


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_similar_chunks(
    query_embedding: list[float],
    chunks: list[dict],
    top_k: int = 3,
) -> list[dict]:

    results = []

    for chunk in chunks:
        similarity = cosine_similarity(
            query_embedding,
            chunk["embedding"],
        )

        results.append({
            "chunk_id": chunk["chunk_id"],
            "page": chunk["page"],
            "text": chunk["text"],
            "similarity": similarity,
        })

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    return results[:top_k]