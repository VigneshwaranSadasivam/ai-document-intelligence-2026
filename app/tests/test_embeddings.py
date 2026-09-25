from app.services.embeddings import generate_embedding


text = """
Python backend developer with experience in
FastAPI, Google Cloud, BigQuery and Vertex AI.
"""


embedding = generate_embedding(text)


print("Embedding generated successfully.")
print("Vector dimensions:", len(embedding))
print("First 10 values:")
print(embedding[:10])