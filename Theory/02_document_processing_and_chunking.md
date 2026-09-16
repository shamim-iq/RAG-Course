# Document Processing and Chunking

## Text Ingestion

Status: 🟡 In Progress — introductory explanation covered; hands-on pending.

### What is it?

- Document ingestion brings source content into a processing pipeline.
- Loading and extracting text are its first steps.

### Why is it needed?

- A file path is not the knowledge inside the file.
- The pipeline must read the content before dividing it into useful pieces.

### How does it work?

```text
DevOps documentation -> Python loader -> text
```

- `.txt` and `.md` files can be read directly as text.
- PDFs require format-specific extraction; that activity comes later.

### Simple example

- Source: `kubernetes_troubleshooting.md`.
- Content: "Check the pod's scheduling events", followed by a `kubectl` command.
- Our loader reads that content into Python for processing.

### Content and metadata

| Field | Meaning | DevOps example |
| --- | --- | --- |
| `content` | Actual information from the document | Check the pod's scheduling events |
| `metadata.source` | Where the information came from | `kubernetes_troubleshooting.md` |
| `metadata.file_type` | Source format | `md` |

- Like a log message with a service label: the message is the information;
  the label helps identify its origin.
- Later, source metadata can identify which runbook supports an answer.
- Reading text is not executing its shell commands or understanding their meaning.

### Key takeaway

- Ingestion makes document content available to the pipeline; it does not yet
  answer operational questions.


## DOCX Ingestion

Status: ⬜ Not Started


## PDF Ingestion

Status: ⬜ Not Started


## CSV Ingestion

Status: ⬜ Not Started


## Chunking

Status: ⬜ Not Started


