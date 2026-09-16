# Document Processing and Chunking

## Objective

Build the document-processing stage of a DevOps Knowledge RAG Assistant using
short runbooks and incident notes. Learn one activity at a time.

## Why it matters in RAG

This project prepares source documents for later use. Concept explanations live
in [Theory](../../Theory/02_document_processing_and_chunking.md); this project tracks hands-on work.

## Activities and checklist

| Activity | Status |
| --- | --- |
| Prepare sample DevOps documents | ✅ Completed |
| [Text ingestion](#current-activity-text-ingestion) | 🟡 In Progress — loader ready; your checks pending |
| DOCX ingestion | 🟡 In Progress — reader added; your checks pending |
| PDF ingestion | 🟡 In Progress — reader added; your checks pending |
| CSV ingestion | 🟡 In Progress — reader added; your checks pending |
| Chunking | 🟡 In Progress — fixed-size implementation in local demo; validation pending |

## Planned flow

```text
DevOps documents -> Load/extract text -> Basic cleaning -> Chunks + metadata -> JSON
```

## Key takeaways

- Reuse the three fictional DevOps documents in `data/`.
- Run each activity and check the result yourself before moving to the next concept.
- Record actual results in [practical notes](notes.md).

## Current status

- User demonstrated successful text ingestion, embeddings, and top-k retrieval.
- Readers are now separated by format; DOCX/PDF/CSV your checks is pending.
- The original ingestion lab remains available. The requested optional demo extends it to local RAG.

See [progress tracker](../00_PROGRESS_TRACKER.md) and
[interview questions](interview_questions.md).

## Current activity: Text ingestion

### Objective

Read the three DevOps documents into Python and inspect their text and source
metadata. See [Theory](../../Theory/02_document_processing_and_chunking.md#text-ingestion).

### Current files

| File under `data/` | Content |
| --- | --- |
| `kubernetes_troubleshooting.md` | Pending pods and CrashLoopBackOff |
| `incident_notes.txt` | Example EKS traffic-spike incident |
| `deployment_runbook.md` | Example staging deployment and rollback |

Script: [ingestion.py](code/ingestion.py). TXT/Markdown/CSV need only Python 3.
DOCX/PDF additionally need `python -m pip install -r code/requirements.txt`
from this project directory.

### Follow the code

1. Locate the project's `data/` folder, one level above `code/`.
2. Visit files in filename order and select a reader by file extension.
3. The selected reader extracts text (plain files use `read_text`).
4. Store that string under `content`, with filename and type under `metadata`.
5. Return the document list and print it so you can inspect it.

The loader reads files directly inside `data/`; it does not scan subfolders.
TXT/Markdown/CSV must be UTF-8 text. Missing folders or unreadable files produce a
normal Python error so the issue is visible during this lab.

### Command to run

From the `RAG` workspace root in PowerShell:

```powershell
python .\Projects\01_document_processing_and_chunking\code\ingestion.py
```

### Expected result

- First line: `Loaded documents: 3`.
- Three sections in this order: deployment runbook, incident notes, Kubernetes notes.
- Each section prints its source, file type, character count, and full text.
- Markdown headings and command blocks remain visible.
- Runbook commands are read as text; the script does not execute them.

### Small experiment

- Add one short follow-up line to `data/incident_notes.txt`, then rerun.
- Expect the same document count, updated incident content, and a larger character count.
- Remove your temporary line afterward if you want to keep the original sample.

### Actual observation

- You demonstrated retrieval of deployment and incident chunks from the existing store.
- Validate the new reader layout with the commands below.
- The three sample files were unchanged after moving them (verified by file checksums).

### Next step

- Share your output or any error before we move to the next Module 02 activity.


## Optional local RAG demo

At your request, the project now includes an demo from document loading through Ollama answers.
Follow [LOCAL_RAG.md](LOCAL_RAG.md) for setup, ingestion, retrieval, and scenario prompts.
This extends the original document-loading exercise; ingestion now uses separate readers.
`code/local_rag.py` uses the existing store; checking generated answers is still pending.
Generated chunks, vectors, retrieval results, and answers go in `local_store/`.

## Code layout and single-format practice

```text
code/
    txt_ingestion.py    # plain incident notes
    md_ingestion.py     # Markdown runbooks
    docx_ingestion.py   # Word body paragraphs and tables
    pdf_ingestion.py    # selectable page text
    csv_ingestion.py    # rows with column labels
    ingestion.py        # selects a reader; attaches source metadata
    local_rag.py        # chunking, embeddings, retrieval, and answers
    requirements.txt   # optional DOCX/PDF dependencies
data/                  # original documents
local_store/           # existing chunks, vectors, and retrieval results
```

From this project directory:

```powershell
python code/ingestion.py --type txt
python code/ingestion.py --type md
python -m pip install -r code/requirements.txt
python code/ingestion.py --type docx
python code/ingestion.py --type pdf
python code/ingestion.py --type csv
```

With the existing samples, expect one TXT document and two Markdown documents.
Other filters return zero until you put matching files in `data/`.
Study one reader, run the corresponding filter, and inspect the extracted text.

- DOCX: main-body paragraphs and top-level tables; no images, headers, or footers.
- PDF: reads stored text, not text in scanned images (OCR); empty pages produce a warning.
- CSV: UTF-8, comma-separated, with a header row; e.g. `service,status` becomes
  `service: api | status: unhealthy`. Chunking can still split a row.
- All readers return text; `ingestion.py` attaches the same metadata format.
- Existing JSON files are preserved. Run ingestion again when you add or change source documents.

Reader references: [python-docx](https://python-docx.readthedocs.io/en/latest/api/document.html)
and [pypdf](https://pypdf.readthedocs.io/en/stable/user/extract-text.html).


