"""Text-based PDF -> page text -> text for chunking (no OCR)."""


def load_pdf(file_path):
    """Extract selectable text; complex page layouts may lose reading order."""
    from pypdf import PdfReader

    # Extract each page before chunking; PDF bytes cannot be read as plain text.
    # You should understand ----------------------------------------------------->
    reader = PdfReader(file_path)
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if not text.strip():
            print(f"Warning: {file_path.name}, page {page_number}: no text; may need OCR.")
        pages.append(text)
    return "\n\n".join(pages)
    # -------------------------------------------------------------------------->
