import re


SECTION_HEADERS = {
    "PROFILE SUMMARY",
    "WORK EXPERIENCE",
    "EDUCATION",
    "TECHNICAL SKILLS",
    "PROJECT EXPERIENCE",
    "PROFESSIONAL PROJECTS",
    "CERTIFICATIONS",
}


def is_section_header(line: str) -> bool:
    normalized = re.sub(r"\s+", " ", line.strip()).upper()
    compact = normalized.replace(" ", "")

    for header in SECTION_HEADERS:
        header_compact = header.replace(" ", "")

        if compact == header_compact:
            return True

    return False


def split_large_section(
    text: str,
    chunk_size: int,
    overlap: int,
) -> list[str]:

    if overlap >= chunk_size:
        raise ValueError(
            "Overlap must be smaller than chunk size."
        )

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(chunk_text)

        start += chunk_size - overlap

    return chunks


def chunk_pages(
    pages: list[dict],
    document_id: str,
    chunk_size: int = 1500,
    overlap: int = 200,
) -> list[dict]:

    sections = []

    current_section = None
    current_lines = []

    for page in pages:

        page_number = page["page"]

        lines = page["text"].splitlines()

        for line in lines:

            if not line.strip():
                continue

            if is_section_header(line):

                if current_section and current_lines:
                    sections.append({
                        "section": current_section,
                        "page": current_page,
                        "text": "\n".join(current_lines).strip(),
                    })

                current_section = re.sub(
                    r"\s+",
                    " ",
                    line.strip(),
                ).upper()

                current_lines = []
                current_page = page_number

            else:

                if current_section is None:
                    current_section = "GENERAL"
                    current_page = page_number

                current_lines.append(line)

    # Save final section
    if current_section and current_lines:
        sections.append({
            "section": current_section,
            "page": current_page,
            "text": "\n".join(current_lines).strip(),
        })

    # Convert sections into chunks
    chunks = []

    chunk_number = 0

    for section in sections:

        section_text = section["text"]

        section_chunks = split_large_section(
            text=section_text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk_text in section_chunks:

            chunks.append({
                "chunk_id": (
                    f"{document_id}_chunk_{chunk_number:04d}"
                ),
                "document_id": document_id,
                "page": section["page"],
                "section": section["section"],
                "text": chunk_text,
            })

            chunk_number += 1

    return chunks