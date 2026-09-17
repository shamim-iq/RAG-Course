# 🧭 Start Here — RAG Fundamentals

**Read this first.** This is the introductory guide for our DevOps RAG project.
Understand these terms before studying chunking strategies or the full Python code.

**Visual map:** 📄 Documents → 📥 Ingestion → ✂️ Chunks → 🔢 Embeddings → 🗄️ Store

**Question flow:** ❓ Question → 🔎 Retrieval → 📚 Context → 🤖 Model → 💬 Answer

## 1. What is RAG?

**RAG = Retrieval-Augmented Generation.**

- **Retrieve:** find document passages relevant to a question.
- **Augment:** add those passages to the model's input.
- **Generate:** ask the model to write an answer using that evidence.

Example: "How do I roll back staging?" → find our rollback runbook → answer from it.
This supplies information at question time; it does not train the model on our files.

## 2. The two flows

```text
PREPARE KNOWLEDGE — when documents change

Runbooks → Load/extract text → Chunks → Embeddings → Store
                                └──── text + source metadata ────┘

ANSWER A QUESTION — for each question

Question → Query embedding → Compare with stored vectors → Top-k chunks
                                                               ↓
                                                  Their text + question
                                                               ↓
                                                          LLM → Answer
```

We store text as well as vectors: search uses the numbers; the answering model
receives the selected text.

## 3. Source, loading, extraction, and ingestion

| Term | Simple meaning | Our example |
| --- | --- | --- |
| Data source | Where information lives | Files in `data/`; a company could use Confluence or GitHub |
| Document | One source item | `deployment_runbook.md` |
| Loading | Opening or fetching an item | Python opens a local runbook |
| Text extraction | Getting readable text from the format | Read TXT directly; use a PDF reader for PDF text |
| Ingestion | Bringing source information into the pipeline | Load documents and prepare them for later use |

- Loading and extraction are parts of ingestion; for plain text they happen together.
- Some systems use "ingestion" for the whole process of preparing and saving searchable content. Our `ingest`
  command includes chunking, embedding, and saving too.
- Reading a `kubectl` command from a document does not execute it.

**Takeaway:** the pipeline needs the document's contents, not just its filename.

## 4. Content and metadata

| Part | What it contains | Why keep it? |
| --- | --- | --- |
| Content | Runbook instructions or incident details | Provides the information needed to answer |
| Metadata | Source filename, file type, chunk index | Identifies where a retrieved passage came from |

```text
Text:   "Verify API health after rollback."
Source: deployment_runbook.md
```

**Takeaway:** metadata is like a service label on a log message—it gives the
information a clear source.

## 5. Chunk and chunk size

- **Chunk:** a smaller piece of a document.
- **Chunking:** splitting a document into those pieces.
- **Chunk size:** the configured size limit for a piece.
- Why: a question about rollback should not require unrelated deployment or incident text.

```text
One runbook: [Deployment instructions | Rollback instructions]
                            ↓
Ideal pieces: [Deployment]  [Rollback]
```

Our current splitter cuts by character count, so its pieces may not match those
ideal topic boundaries. The final piece can be shorter than the limit.

**Takeaway:** chunks should contain enough context to be useful when retrieved alone.

## 6. Overlap

**Overlap** is text repeated between neighboring chunks to reduce context loss.

```text
Size = 500 characters; overlap = 100 characters

Chunk 1: characters   0–499
Chunk 2: characters 400–899
                    └─ 400–499 appear in BOTH chunks

Forward step = 500 - 100 = 400 characters
```

- A sentence might cross a boundary; overlap gives the next chunk some earlier text.
- More overlap also means more duplicated content and embedding work.
- It does not guarantee that a full sentence or command stays together.
- `500/100` are our learning defaults, not universal best settings.

**Takeaway:** overlap helps preserve context across cuts.

## 7. Characters versus tokens

- **Character:** a letter, space, punctuation mark, or newline counted by our script.
- **Token:** a piece of text a model reads; it may be a word part or punctuation.
- Character count and token count are different; there is no fixed conversion.
- Models have token limits, even though our simple chunker measures characters.

**Takeaway:** always check what unit a chunk-size setting uses.

## 8. Embedding and vector

An **embedding** represents text as a list of numbers—a **vector**—for comparison.

```text
"Roll back the API" → Embedding model → [0.12, -0.08, 0.31, ...]
```

The numbers above are examples. You do not need to interpret individual values.

- **Document embedding:** represents a document chunk; created during ingestion.
- **Query embedding:** represents the user's question; created when asking.
- Use the same embedding model/settings for both so their vectors are comparable.
- Related wording can have similar vectors even without exactly matching words.

**Takeaway:** embeddings support similarity search; they are not generated answers.

## 9. Vector storage

Keep three things together:

```text
Chunk text + metadata + embedding
```

- Our `local_store/vectors.json` stores these records in a readable file.
- Python compares the query with every stored vector in this small demo.
- A vector database stores and searches vectors; our JSON
  file is a learning substitute, not a database server.
- Rebuild after changing source documents, chunk settings, or the embedding model.

**Takeaway:** saved vectors avoid embedding every source document for each question.

## 10. Similarity, retrieval, and top-k

- **Cosine similarity:** compares vector directions; higher scores mean closer matches.
- **Retrieval:** selecting relevant stored passages for a question.
- **Top-k:** keep the k highest-ranked chunks; `k=2` means up to two chunks.
- Scores are not confidence percentages, and the highest score may not contain
  the most complete answer.

```text
Question vector → compare with every chunk vector → rank scores

0.641  Deployment chunk  ┐
0.629  Rollback chunk    ┘ top-k = 2 keeps these
0.439  Incident chunk      left out
```

These scores come from your demonstrated retrieval. Both selected chunks came
from the same file: top-k counts chunks, not documents.

**Takeaway:** chunk size controls how much text is in each piece; top-k controls
how many pieces reach the next stage. Our demo has no minimum score for accepting a match.

## 11. Context, prompt, and answer generation

| Term | Meaning in our demo |
| --- | --- |
| Context | Text of retrieved chunks, with source labels |
| Prompt | Instructions, context, and the user's question sent to the model |
| LLM (large language model) / chat model | Model that writes the answer |
| Citation | A chunk reference such as `[2]` identifying supporting evidence |

```text
Retrieved rollback instructions + "How do I roll back?"
                              ↓
                          Chat model
                              ↓
                       Answer with [2]
```

- The embedding model creates vectors; the chat model writes answers.
- Ollama runs these local models; Python handles reading and retrieval.
- `--retrieve-only` stops before generation, making the selected evidence visible.
- The model can still make mistakes. Check answers and citations against the text.
- Our historical documents do not reveal the current state of an EKS cluster.

**Takeaway:** RAG supplies evidence to the model; it does not guarantee correctness.

## What to remember

| Concept | Depth required |
| --- | --- |
| Ingestion, metadata, chunks, size, overlap | Understand well |
| Document/query embeddings and their shared model | Understand well |
| Cosine similarity | Concept only |
| Top-k, context, and answer generation | Understand well |
| API requests, saved-file format, command-line options, and the similarity formula | Basic awareness |

## Read next

1. [Document processing notes](02_document_processing_and_chunking.md)
2. [Chunking strategies: which to use when](02_chunking_strategies.md)
3. [Code guide](../Projects/01_document_processing_and_chunking/code/README.md)
4. [Scoring and re-ranking](04_scoring_and_reranking.md) — how matches are ordered before answering.
