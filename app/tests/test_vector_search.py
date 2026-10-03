from app.services.embeddings import generate_embedding
from app.services.vector_search import search_vector_index


query = "What Python technologies are mentioned?"

query_embedding = generate_embedding(query)

results = search_vector_index(
    query_embedding,
    top_k=3,
)

for result in results:
    print(
        "ID:",
        result.id,
        "Distance:",
        result.distance,
    )