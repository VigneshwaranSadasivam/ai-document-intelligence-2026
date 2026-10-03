from app.services.embeddings import generate_embedding


embedding = generate_embedding(
    "What Python technologies are mentioned?"
)

print("Embedding dimension:", len(embedding))