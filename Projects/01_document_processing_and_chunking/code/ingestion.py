"""Files -> choose reader by extension -> content + source metadata.

Run this file to inspect extraction before embedding anything.
"""

import argparse
from pathlib import Path

from txt_ingestion import load_txt
from md_ingestion import load_md
from docx_ingestion import load_docx
from pdf_ingestion import load_pdf
from csv_ingestion import load_csv

DATA = Path(__file__).resolve().parent.parent / "data"


def load_documents(data_directory, file_type=None):
    """Load supported files directly inside data_directory, optionally filtering a type."""
    documents = []
    for file_path in sorted(data_directory.iterdir()):
        if not file_path.is_file():
            continue
        extension = file_path.suffix.lower().lstrip(".")
        if file_type and extension != file_type:
            continue

        # Each format needs its own extractor; the rest of RAG receives the same shape.
        # You should understand ----------------------------------------------------->
        if extension == "txt":
            content = load_txt(file_path)
        elif extension == "md":
            content = load_md(file_path)
        elif extension == "docx":
            content = load_docx(file_path)
        elif extension == "pdf":
            content = load_pdf(file_path)
        elif extension == "csv":
            content = load_csv(file_path)
        else:
            continue

        if not content.strip():
            print(f"Skipping {file_path.name}: no extracted text.")
            continue
        documents.append({
            "content": content,
            "metadata": {"source": file_path.name, "file_type": extension},
        })
        # -------------------------------------------------------------------------->
    return documents


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--type", choices=["txt", "md", "docx", "pdf", "csv"])
    args = parser.parse_args()
    try:
        documents = load_documents(DATA, args.type)
    except ImportError:
        parser.exit(1, "Install readers: python -m pip install -r code/requirements.txt\n")
    print(f"Loaded documents: {len(documents)}")
    for document in documents:
        print("\n" + "=" * 50)
        print(f"Source: {document['metadata']['source']}")
        print(f"File type: {document['metadata']['file_type']}")
        print(f"Characters: {len(document['content'])}")
        print(document["content"])
