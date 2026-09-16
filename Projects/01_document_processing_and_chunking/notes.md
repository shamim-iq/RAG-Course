# Practical Notes

## Implemented

- Reused three fictional DevOps documents from the original workspace.
- Moved them into the project's `data/` without changing their contents.
- Added `code/ingestion.py` using standard Python to load `.txt` and `.md` files.
- The script prints content and source metadata; it creates no output files.

## Observations

| Check | Observation |
| --- | --- |
| Sample preservation | File checksums confirmed the contents did not change when moved |
| Manual file inspection | Awaiting your check |
| Loader execution | Implemented; awaiting your manual run |
| Expected document count | 3; not yet validated by execution |

## Key takeaways

- Sample preparation is complete; the ingestion lab is still in progress.
- The Kubernetes notes include headings and command blocks to inspect later.
- Keep expected results separate from results actually observed.
- After running, record whether all three source names and their content appeared.


## Local RAG preview

- Added fixed character chunking, Ollama embeddings, JSON vector storage, and search using cosine similarity (a vector matching score).
- Added local chat answers using selected text and source references.
- Ollama API was reachable; its installed model list was empty.
- You later demonstrated real embeddings and top-k search; generated answers still need checking.
- Setup and scenario prompts: [LOCAL_RAG.md](LOCAL_RAG.md).


## Separate ingestion readers

- All Python source is now in `code/`; the old scripts in the project root were removed.
- TXT, Markdown, DOCX, PDF, and CSV each have their own reader.
- Verified original sample text, type filtering, CSV quoted fields, imports, and paths.
- DOCX/PDF execution is pending installation of the optional reader packages.
- Existing `data/` and `local_store/` contents were preserved.
- You previously confirmed real embeddings and top-k retrieval; answer generation is pending.
