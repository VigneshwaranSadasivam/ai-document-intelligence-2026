import fitz


def extract_pages_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extract text from a PDF while preserving page numbers.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text().strip()

        if not text:
            continue

        pages.append(
            {
                "page": page_number,
                "text": text,
            }
        )

    document.close()

    return pages