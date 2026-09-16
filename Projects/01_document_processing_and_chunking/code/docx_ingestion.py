"""DOCX -> body paragraphs and tables -> text for chunking."""


def load_docx(file_path):
    """Read main-body text; headers, footers, images, and nested tables are excluded."""
    # Import only when needed so TXT/Markdown do not require extra packages.
    from docx import Document
    from docx.text.paragraph import Paragraph

    # Extract paragraphs and table rows in document order for usable runbook text.
    # You should understand ----------------------------------------------------->
    document = Document(file_path)
    sections = []
    for block in document.iter_inner_content():
        if isinstance(block, Paragraph):
            sections.append(block.text)
        else:
            for row in block.rows:
                cells = []
                for cell in row.cells:
                    cells.append(cell.text)
                sections.append(" | ".join(cells))
    return "\n\n".join(sections)
    # -------------------------------------------------------------------------->
