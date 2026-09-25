from google.cloud import firestore


client = firestore.Client()


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