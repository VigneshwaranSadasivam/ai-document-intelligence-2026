from app.services.document_parser import (
    extract_pages_from_pdf,
)

from app.services.chunker import chunk_pages


pdf_path = "documents/VIGNESHWARAN_Resume.pdf"


pages = extract_pages_from_pdf(pdf_path)

chunks = chunk_pages(
    pages,
    document_id=document_id,
    chunk_size=1000,
    overlap=200,
)


print(f"Total pages: {len(pages)}")
print(f"Total chunks: {len(chunks)}")


for chunk in chunks:

    print("\n" + "=" * 80)

    print(
        f"{chunk['chunk_id']} | "
        f"Page {chunk['page']}"
    )

    print("=" * 80)

    print(chunk["text"])