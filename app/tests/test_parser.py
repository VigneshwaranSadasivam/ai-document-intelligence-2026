from app.services.document_parser import extract_pages_from_pdf


pdf_path = "documents/VIGNESHWARAN_Resume.pdf"

pages = extract_pages_from_pdf(pdf_path)

for page in pages:
    print("=" * 80)
    print(f"PAGE {page['page']}")
    print("=" * 80)
    print(page["text"])