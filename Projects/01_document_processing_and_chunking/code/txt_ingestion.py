"""TXT file -> plain text for the RAG pipeline."""


def load_txt(file_path):
    """Read a UTF-8 incident note without changing its contents."""
    # Read the actual information that will later be chunked and embedded.
    # You should understand ----------------------------------------------------->
    text = file_path.read_text(encoding="utf-8")
    return text
    # -------------------------------------------------------------------------->
