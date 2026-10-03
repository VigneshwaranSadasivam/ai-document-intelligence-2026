from app.services.embeddings import generate_embedding
from app.services.vector_search import retrieve_relevant_chunks


document_id = "doc_29bc0d1b"

query = "What Python technologies are mentioned?"

query_embedding = generate_embedding(query)

chunks = retrieve_relevant_chunks(
    document_id=document_id,
    query_embedding=query_embedding,
    top_k=3,
)

for chunk in chunks:
    print("\n-----------------------------")
    print("Chunk ID:", chunk["chunk_id"])
    print("Page:", chunk["page"])
    print("Distance:", chunk["distance"])
    print("Text:")
    print(chunk["text"])