# RAG Course — DevOps Learning Workspace

Practical RAG learning through short Kubernetes runbooks, incident notes, and
deployment procedures. We add topics one step at a time using readable Python.

## Start here

- **[Read first: RAG fundamentals](Theory/00_start_here_rag_fundamentals.md)**
- [Progress tracker](Projects/00_PROGRESS_TRACKER.md)
- [Theory notes](Theory/02_document_processing_and_chunking.md)
- [Retrieval methods](Theory/03_retrieval_methods.md)
- [AWS RAG with Bedrock Knowledge Bases](Theory/05_aws_bedrock_knowledge_bases.md)
- [RAG evals and groundedness](Theory/06_evals_and_groundedness.md)
- [Document processing project](Projects/01_document_processing_and_chunking/README.md)
- [Python code guide](Projects/01_document_processing_and_chunking/code/README.md)
- [Local Ollama RAG demo](Projects/01_document_processing_and_chunking/LOCAL_RAG.md)

## Quick start

Requires Python 3. From the repository root:

```powershell
cd Projects/01_document_processing_and_chunking
python code/ingestion.py --type txt
```

TXT, Markdown, and CSV use standard Python. Optional DOCX/PDF readers:

```powershell
python -m pip install -r code/requirements.txt
```

For local embeddings and answers, follow the Ollama setup in the demo guide.
Generated vectors and retrieval results in `local_store/` stay local and are
excluded from Git; recreate them with `python code/local_rag.py ingest`.

The sample documents are fictional learning data. The assistant reads them;
it does not connect to or modify a live cluster.
