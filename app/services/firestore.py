from google.cloud import firestore

PROJECT_ID = "ai-document-intelligence-2026"
client = firestore.Client(
    project=PROJECT_ID
)


def create_document_metadata(
    document_id: str,
    filename: str,
    gcs_uri: str,
):

    document_data = {
        "document_id": document_id,
        "filename": filename,
        "gcs_uri": gcs_uri,
        "status": "uploaded",
        "created_at": firestore.SERVER_TIMESTAMP,
    }

    client.collection("documents").document(
        document_id
    ).set(document_data)

    return document_data

def get_document_metadata(document_id: str):

    document_ref = (
        client
        .collection("documents")
        .document(document_id)
    )

    document = document_ref.get()

    if not document.exists:
        return None

    return document.to_dict()

def update_document_analysis(
    document_id: str,
    analysis: dict,
):

    document_ref = (
        client
        .collection("documents")
        .document(document_id)
    )

    document_ref.update({
        "status": "completed",
        "analysis": analysis,
        "analyzed_at": firestore.SERVER_TIMESTAMP,
    })

def save_document_chunks(
    document_id: str,
    chunks: list[dict],
):
    document_ref = client.collection("documents").document(document_id)

    chunks_ref = document_ref.collection("chunks")

    for chunk in chunks:
        chunk_data = {
            "chunk_id": chunk["chunk_id"],
            "document_id": document_id,
            "page": chunk["page"],
            "text": chunk["text"],
        }

        chunks_ref.document(chunk["chunk_id"]).set(chunk_data)

    return len(chunks)

def get_chunks_by_ids(
    document_id: str,
    chunk_ids: list[str],
) -> list[dict]:

    chunks_ref = (
        client
        .collection("documents")
        .document(document_id)
        .collection("chunks")
    )

    results = []

    for chunk_id in chunk_ids:
        chunk_doc = chunks_ref.document(chunk_id).get()

        if chunk_doc.exists:
            results.append(chunk_doc.to_dict())

    return results