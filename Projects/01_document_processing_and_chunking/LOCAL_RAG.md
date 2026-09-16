# Local Ollama RAG Demo

A small preview of chunking, embeddings, retrieval, and answers, added at your
request. The other course activities remain separate and incomplete.

## Understand the flow

```text
data/ -> 500-character chunks -> Ollama embedding model -> local_store/vectors.json
Question -> same embedding model -> compare every vector -> top 3 chunks
         -> Ollama chat model receives question + chunks -> answer with citations
```

- **Chunk:** a piece of a document; 100 characters overlap with its neighbor.
- **Embedding:** a list of numbers representing text for similarity comparison.
- **Retrieval:** Python selects the highest cosine similarity scores.
- **Generation:** the chat model writes an answer using the selected text.
- This is a fixed RAG workflow, not an agent choosing its own actions. The model does not open
  the JSON database; Python reads it and passes selected evidence to the model.

## 1. Download models (once)

Your Ollama service was reachable, but its model list was empty. From PowerShell:

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull embeddinggemma
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull qwen2.5:1.5b
```

The embedding model creates vectors; the chat model writes answers. Downloads
need internet; after downloading, the models run on your laptop. TXT/Markdown/CSV use standard Python. For DOCX/PDF, install `code/requirements.txt`. Keep Ollama running. If embeddinggemma reports a version
error, update Ollama (the model requires version 0.11.10 or newer).

## 2. Build the local store

From the `RAG` workspace root:

```powershell
cd .\Projects\01_document_processing_and_chunking
python code/local_rag.py ingest
```

Expect filenames with chunk counts and saved-file paths:

| Generated file in `local_store/` | Inspect this for |
| --- | --- |
| `chunks.json` | Chunk text, source, and chunk index |
| `vectors.json` | Same chunks plus embeddings and the embedding model name |
| `last_retrieval.json` | Latest question, matched text, sources, similarity scores |
| `last_answer.json` | Latest generated answer and the evidence supplied to it |

The last two files appear when you ask questions. Each run replaces the relevant
files; `last_answer.json` remains from the previous answer during retrieval-only runs.
Re-run ingestion after editing documents or changing chunk settings/model. If
ingestion fails, an older vectors file may remain; fix the error and rebuild
successfully before asking questions. Do not edit stored vectors manually.

## 3. See retrieval before generation

```powershell
python code/local_rag.py ask "What caused pending pods during the traffic spike?" --retrieve-only
```

Expect three text passages and their matching scores; inspect which comes from the incident.
Scores show how closely text matches; they do not prove an answer or diagnosis is correct.

## 4. Ask the local assistant

Run these prompts through the script, not directly in `ollama run`:

```powershell
python code/local_rag.py ask "What happened during the API traffic spike, and how long did recovery take?"
python code/local_rag.py ask "What should I check when a pod is Pending?"
python code/local_rag.py ask "How do I roll back the staging API deployment?"
python code/local_rag.py ask "What should I inspect for CrashLoopBackOff?"
python code/local_rag.py ask "What is our Azure SQL backup retention policy?"
```

| Scenario | What to check in the evidence and answer |
| --- | --- |
| Historical incident | Capacity/autoscaling details; about 8 minutes to recover |
| Pending pod | Scheduling events, CPU/memory, taints, PVCs |
| Rollback | Rollout undo, rollout status, and compatibility checks |
| CrashLoopBackOff | Previous container logs, exit codes, configuration, probes |
| Missing documentation | Should say the information was not found |

Small models may omit details or invent claims despite the prompt. Compare each
answer and citation with the printed passages. Top-k always returns nearest
matches, including for unrelated questions; there is no minimum matching
score here. The missing-document question tests whether the model says it lacks the information.
The demo reads historical documents and has no live EKS access.

## 5. Simple experiment

```powershell
python code/local_rag.py ingest --chunk-size 300 --overlap 50
python code/local_rag.py ask "How do I roll back the staging API deployment?" --top-k 2
```

Compare chunk counts, broken sentences, selected evidence, and answer completeness.
Restore defaults with `python code/local_rag.py ingest`. Fixed character boundaries
can split commands and sentences; structure-aware chunking is a later improvement.

## Actual observations

- Ollama reachable; no installed models at setup time.
- You demonstrated real embeddings and top-k search. Checking generated answers is still pending.
- A JSON file + comparing every stored vector is a learning substitute for a vector database,
  suitable for these three documents, without running a database service.

## Code reading order

Start with `build_index`, then `ask`; follow the helper functions when needed.
Search `You should understand` for the complete sections worth studying closely.
`ollama` is only the function that sends requests to Ollama; `code/ingestion.py` chooses a reader for each file type.

| Code Section | What I Need to Know | Depth Required |
| --- | --- | --- |
| Ingestion | Files become text with source metadata | Understand well |
| Chunking | Character limits and overlap repeat some text near each cut | Understand well |
| Embeddings | Document and query vectors must use the same model | Understand well |
| Vector storage | Keep chunk text, metadata, and vector together | Understand well |
| Cosine similarity | Compares query and chunk vectors; not confidence | Concept only |
| Top-K | Rank scores and select the closest chunks | Understand well |
| Context and LLM | Send selected evidence with the question; verify citations | Understand well |
| argparse | Reads command-line options | Basic awareness |
| HTTP, JSON, filesystem | Connect to Ollama and read/write files | Basic awareness |

Sources: [Ollama embeddings API](https://docs.ollama.com/api/embed),
[chat API](https://docs.ollama.com/api/chat),
[EmbeddingGemma](https://ollama.com/library/embeddinggemma),
[Qwen2.5 1.5B](https://ollama.com/library/qwen2.5:1.5b).


