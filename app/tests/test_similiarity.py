import math

from app.services.embeddings import generate_embedding


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

    return dot_product / (
        magnitude_a * magnitude_b
    )


text_a = """
Python backend developer with FastAPI experience.
"""

text_b = """
Backend engineer experienced in Python web APIs.
"""

text_c = """
I like watching cricket on weekends.
"""


embedding_a = generate_embedding(text_a)
embedding_b = generate_embedding(text_b)
embedding_c = generate_embedding(text_c)


similarity_ab = cosine_similarity(
    embedding_a,
    embedding_b,
)

similarity_ac = cosine_similarity(
    embedding_a,
    embedding_c,
)


print(f"A ↔ B similarity: {similarity_ab:.4f}")
print(f"A ↔ C similarity: {similarity_ac:.4f}")