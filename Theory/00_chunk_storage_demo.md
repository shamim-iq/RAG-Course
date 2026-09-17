# 📄 Demo: One File to Stored Chunks

This is a reading example, not a program or a live vector database.
The vectors are invented, with only three numbers to keep them readable.
They are not real model output and should not be used to test search quality.

## 📥 1. Original file

Imagine `deployment_runbook.txt` contains these three paragraphs:

```text
Deployment: Apply the API manifest with kubectl apply -f api.yaml.

Health check: Check progress with kubectl rollout status deployment/api.

Rollback: Undo a failed deployment with kubectl rollout undo deployment/api.
```

## ✂️ 2. Split into chunks

For this example, code splits on blank lines. Each paragraph becomes one chunk.
There is no overlap. No model chooses the boundaries here.

```text
deployment_runbook.txt
  ├─ Chunk 0: Deployment paragraph
  ├─ Chunk 1: Health check paragraph
  └─ Chunk 2: Rollback paragraph
```

Each chunk then goes through the same embedding model to get its own vector.
Our project's character-count splitter uses different boundaries.

## 🗄️ 3. Store one record per chunk

Below is JSON with comments (`jsonc`) for explanation. Plain JSON does not allow
comments. This layout is illustrative; database field names can differ.

```jsonc
[
  {
    // A unique ID for this chunk, not for the whole file.
    "id": "deployment-runbook-chunk-0",
    // Only this field is the embedding: numbers used for vector search.
    "vector": [0.12, -0.08, 0.31],
    // Keep the readable text so the answering model can use it later.
    "text": "Deployment: Apply the API manifest with kubectl apply -f api.yaml.",
    "metadata": {
      // The shared document ID connects all three records to one file.
      "document_id": "deployment-runbook",
      "filename": "deployment_runbook.txt",
      "file_type": "txt",
      // Indexing starts at 0. This is the first chunk.
      "chunk_index": 0
    }
  },
  {
    "id": "deployment-runbook-chunk-1",
    // A separate vector for the health-check text.
    "vector": [0.25, 0.40, -0.11],
    "text": "Health check: Check progress with kubectl rollout status deployment/api.",
    "metadata": {
      "document_id": "deployment-runbook",
      "filename": "deployment_runbook.txt",
      "file_type": "txt",
      "chunk_index": 1
    }
  },
  {
    "id": "deployment-runbook-chunk-2",
    // The vector, text, and metadata all describe this rollback chunk.
    "vector": [-0.15, 0.62, 0.20],
    "text": "Rollback: Undo a failed deployment with kubectl rollout undo deployment/api.",
    "metadata": {
      "document_id": "deployment-runbook",
      "filename": "deployment_runbook.txt",
      "file_type": "txt",
      "chunk_index": 2
    }
  }
]
```

One file produced **three records**, each with its own vector and text.
Text stays text. Metadata stays structured fields; it is not an embedding.
`chunk_index: 2` means the third chunk, not the total number of chunks.

## 🔎 4. Retrieve a chunk

For "How do I undo a failed deployment?", the desired match is chunk 2:

```text
Question → Same embedding model → Query vector
                                      ↓
                   Compare with stored chunk vectors
                                      ↓
                  Return matching text + source metadata
                                      ↓
                  Use rollback text in the answer prompt
```

This is the intended result, not a calculated result from the invented vectors.
Retrieval can return individual chunks without returning the whole file.

For PDF, DOCX, or CSV, extraction happens before chunking. Only extracted and
saved content is represented; images, layout, or tables are not automatically
preserved. Page numbers or section names require code that captures them.

**Understand well:** one file can produce many chunk records.
**Concept only:** embeddings let search compare chunks with a question.
**Basic awareness:** databases may use a different record layout or store text separately.

Back to [RAG fundamentals](00_start_here_rag_fundamentals.md).
