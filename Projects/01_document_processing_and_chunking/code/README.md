# Code Guide

Update this guide whenever a Python file is added, renamed, removed, or changes
purpose in `code/`. Keep its link, use case, and role in shared steps current.

## Files by use case

| Python file | Use case | What it does |
| --- | --- | --- |
| [txt_ingestion.py](txt_ingestion.py) | `.txt` incident notes | Reads plain text. |
| [md_ingestion.py](md_ingestion.py) | `.md` runbooks | Reads text, keeping headings and commands. |
| [docx_ingestion.py](docx_ingestion.py) | `.docx` operational procedures | Reads main paragraphs and tables. |
| [pdf_ingestion.py](pdf_ingestion.py) | Text-based `.pdf` manuals | Extracts page text; does not read text from scanned images. |
| [csv_ingestion.py](csv_ingestion.py) | `.csv` incident or service records | Converts rows into text with column labels. |
| [ingestion.py](ingestion.py) | Loading any supported format | Selects the matching reader and adds source details such as the filename (metadata). |
| [local_rag.py](local_rag.py) | Building the vector store or asking questions | Runs chunking, embeddings, retrieval, and optional answer generation. |

## Shared files across use cases

The same shared files work for Kubernetes, deployments, incidents, or other topics.
Which functions run depends on the command:

| Workflow | Shared code used | Format readers used |
| --- | --- | --- |
| Inspect extracted text | `ingestion.py` | Only readers matching the selected files |
| Build/rebuild vectors (`ingest`) | `local_rag.py` → `ingestion.py` | Readers matching files in `data/` |
| Search existing vectors (`ask --retrieve-only`) | `local_rag.py` | None; reads the saved vector store |
| Generate an answer (`ask`) | `local_rag.py` | None; retrieves saved chunks and calls Ollama |

No file needs to do work for **every command**. `ingestion.py` is
shared across ingestion formats; `local_rag.py` is shared across RAG topics.
Asking questions does not reload source documents, even though the script imports the reader files.

## Reading order

`txt_ingestion.py` → `ingestion.py` → `local_rag.py`

Read the other format readers when working with those file types.
Search **You should understand** to find the key learning sections.

## Data flow

```text
../data/ → Format reader → ingestion.py → local_rag.py → ../local_store/
```

[requirements.txt](requirements.txt) lists the optional DOCX/PDF reader packages.

Run from the project directory (one level above `code/`):

```powershell
python code/ingestion.py --type txt
python code/local_rag.py ingest
python code/local_rag.py ask "How do I roll back the staging API deployment?" --retrieve-only
```
