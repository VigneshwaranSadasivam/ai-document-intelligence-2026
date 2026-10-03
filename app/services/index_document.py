from app.services.firestore import (
    get_document_metadata,
    save_document_chunks,
)
from app.services.storage import download_file_from_gcs
from app.services.document_parser import extract_pages_from_pdf
from app.services.chunker import chunk_pages
from app.services.embeddings import generate_embeddings
from app.services.vector_search import upsert_chunks


def index_document(document_id: str):

    document = get_document_metadata(document_id)

    if document is None:
        raise ValueError("Document not found")

    local_pdf = download_file_from_gcs(
        document["gcs_uri"]
    )

    pages = extract_pages_from_pdf(local_pdf)
    print("Pages extracted:", len(pages))
    for page in pages:
        print(
            f"Page {page['page']}: text length = {len(page['text'])}"
        )

    chunks = chunk_pages(
        pages,
        document_id=document_id,
        chunk_size=1000,
        overlap=200,
    )
    print("Chunks created:", len(chunks))

    saved_chunk_count = save_document_chunks(
        document_id,
        chunks,
    )

    embedded_chunks = generate_embeddings(chunks)
    print("Embedded chunks:", len(embedded_chunks))

    result = upsert_chunks(embedded_chunks)

    return {
        "document_id": document_id,
        "filename": document["filename"],
        "total_pages": len(pages),
        "total_chunks": len(chunks),
        "vector_search": result,
    }


if __name__ == "__main__":

    document_id = "doc_29bc0d1b"

    result = index_document(document_id)

    print(result)