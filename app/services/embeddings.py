from google import genai
from google.genai.types import HttpOptions


PROJECT_ID = "ai-document-intelligence-2026"
LOCATION = "global"

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    http_options=HttpOptions(api_version="v1"),
)


EMBEDDING_MODEL = "gemini-embedding-001"


def generate_embedding(
    text: str,
) -> list[float]:

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    return response.embeddings[0].values

def generate_embeddings(
    chunks: list[dict],
) -> list[dict]:

    results = []

    for chunk in chunks:

        embedding = generate_embedding(
            chunk["text"]
        )

        results.append(
            {
                **chunk,
                "embedding": embedding,
            }
        )

    return results