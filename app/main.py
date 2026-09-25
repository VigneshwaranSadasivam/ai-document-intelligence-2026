from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.services.vertex_ai import analyze_document
from app.services.storage import (
    upload_file_to_gcs, 
    download_file_from_gcs
)
from app.services.firestore import (
    create_document_metadata,
    get_document_metadata,
    update_document_analysis,
)
from app.services.document_parser import extract_pages_from_pdf
from app.services.chunker import chunk_pages
from app.services.embeddings import (
    generate_embedding,
    generate_embeddings,
)
from app.services.vector_search import search_similar_chunks

import uuid

app = FastAPI(
    title="AI Document Intelligence",
    version="0.1.0",
)


class DocumentAnalyzeRequest(BaseModel):
    document_uri: str


@app.get("/")
def root():
    return {
        "message": "AI Document Intelligence API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/api/v1/documents")
async def upload_document(
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    document_id = (
        f"doc_{uuid.uuid4().hex[:8]}"
    )

    file_bytes = await file.read()

    gcs_uri = upload_file_to_gcs(
        file_bytes=file_bytes,
        document_id=document_id,
        filename=file.filename,
    )

    create_document_metadata(
        document_id=document_id,
        filename=file.filename,
        gcs_uri=gcs_uri,
    )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "status": "uploaded",
        "gcs_uri": gcs_uri,
    }

@app.post(
    "/api/v1/documents/{document_id}/analyze"
)
def analyze_document_endpoint(
    document_id: str,
):

    document = get_document_metadata(
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    try:

        result = analyze_document(
            document["gcs_uri"]
        )

        update_document_analysis(
            document_id=document_id,
            analysis=result.model_dump(),
        )

        return {
            "document_id": document_id,
            "status": "completed",
            "analysis": result,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Document analysis failed: {str(exc)}",
        )

@app.get(
    "/api/v1/documents/{document_id}/chunks"
)
def get_document_chunks(
    document_id: str,
):

    document = get_document_metadata(
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    gcs_uri = document["gcs_uri"]

    try:

        local_pdf = download_file_from_gcs(
            gcs_uri
        )

        pages = extract_pages_from_pdf(
            local_pdf
        )

        chunks = chunk_pages(
            pages,
            chunk_size=1000,
            overlap=200,
        )

        return {
            "document_id": document_id,
            "filename": document["filename"],
            "total_pages": len(pages),
            "total_chunks": len(chunks),
            "chunks": chunks,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Chunking failed: {str(exc)}",
        )

@app.get(
    "/api/v1/documents/{document_id}/embeddings"
)
def generate_document_embeddings(
    document_id: str,
):

    document = get_document_metadata(
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    try:

        # 1. Download PDF
        local_pdf = download_file_from_gcs(
            document["gcs_uri"]
        )

        # 2. Extract pages
        pages = extract_pages_from_pdf(
            local_pdf
        )

        # 3. Create chunks
        chunks = chunk_pages(
            pages,
            chunk_size=1000,
            overlap=200,
        )

        # 4. Generate embeddings
        embedded_chunks = generate_embeddings(
            chunks
        )

        return {
            "document_id": document_id,
            "filename": document["filename"],
            "total_pages": len(pages),
            "total_chunks": len(embedded_chunks),
            "chunks": embedded_chunks,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Embedding generation failed: {str(exc)}",
        )

@app.get("/api/v1/documents/{document_id}/search")
def search_document(
    document_id: str,
    query: str,
    top_k: int = 3,
):
    document = get_document_metadata(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    try:
        local_pdf = download_file_from_gcs(
            document["gcs_uri"]
        )

        pages = extract_pages_from_pdf(local_pdf)

        chunks = chunk_pages(
            pages,
            chunk_size=1000,
            overlap=200,
        )

        embedded_chunks = generate_embeddings(chunks)

        query_embedding = generate_embedding(query)

        results = search_similar_chunks(
            query_embedding,
            embedded_chunks,
            top_k=top_k,
        )

        return {
            "document_id": document_id,
            "query": query,
            "results": results,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(exc)}",
        )