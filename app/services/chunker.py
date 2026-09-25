def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[dict]:

    if overlap >= chunk_size:
        raise ValueError(
            "Overlap must be smaller than chunk size."
        )

    chunks = []

    chunk_id = 0

    for page in pages:

        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append(
                    {
                        "chunk_id": f"chunk_{chunk_id:04d}",
                        "page": page_number,
                        "text": chunk_text,
                    }
                )

                chunk_id += 1

            start += chunk_size - overlap

    return chunks