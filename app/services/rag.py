from google import genai
from google.genai.types import HttpOptions

from app.services.embeddings import generate_embedding
from app.services.vector_search import retrieve_relevant_chunks

PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "global"

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    http_options=HttpOptions(api_version="v1"),
)


def generate_rag_answer(
    document_id: str,
    question: str,
    top_k: int = 5,
):
    # 1. Convert question into an embedding
    query_embedding = generate_embedding(question)

    # 2. Retrieve relevant chunks
    chunks = retrieve_relevant_chunks(
        document_id=document_id,
        query_embedding=query_embedding,
        top_k=top_k,
    )

    if not chunks:
        return {
            "answer": "I could not find relevant information in the document.",
            "sources": [],
        }

    # 3. Build context from retrieved chunks
    context_parts = []

    for chunk in chunks:
        context_parts.append(f"""
Page: {chunk["page"]}
Chunk ID: {chunk["chunk_id"]}

{chunk["text"]}
""")

    context = "\n\n---\n\n".join(context_parts)

    # 4. Ask Gemini using only the retrieved context
    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information provided
in the document context below.

Rules:

1. Do not invent facts that are not present in the context.
2. You may perform simple reasoning or calculations using facts
   explicitly present in the context.
3. For example, if the document provides employment start/end dates,
   you may calculate the duration of employment.
4. If a role says "Present", treat it as an ongoing role.
5. Do not assume missing dates.
6. If an exact answer cannot be determined from the context,
   clearly explain what information is available instead.
7. Keep the answer concise and factual.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    # 5. Return answer + source information
    sources = [
        {
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "distance": chunk.get("distance"),
            "text": chunk["text"],
        }
        for chunk in chunks
    ]

    return {
        "answer": response.text,
        "sources": sources,
    }
