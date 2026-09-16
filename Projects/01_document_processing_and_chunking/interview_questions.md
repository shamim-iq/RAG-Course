# Interview Questions: Ingestion Basics

Preparation material for the introductory topic. Practice status: answers not yet reviewed together.
Extend this file as new activities are covered.

## Fundamentals

1. **What does document ingestion mean?**
   Reading source documents and extracting their text so the program can use it.
2. **Why is knowing a filename not enough?**
   It identifies a location; the pipeline must read the file's content.
3. **How can Markdown and plain text be loaded initially?**
   Read them as text using standard Python file handling.
4. **Does loading documents mean the assistant can answer questions?**
   No. It only makes their content available for later processing.

## Scenarios

1. **A loader returns only runbook filenames. Is ingestion complete?**
   No. It must also read the actual runbook content.
2. **A team adds PDF runbooks. Can we assume the text loader can read them?**
   No. PDF files need a PDF reader to extract their text.
3. **The sample files exist, but the loader has never run. Is the lab complete?**
   No. Record preparation as complete and running and checking the code as pending.

## DevOps relevance

1. **Which operational documents are useful sources for this project?**
   Kubernetes troubleshooting notes, deployment runbooks, and incident records.
2. **Does ingesting a rollback runbook execute its commands?**
   No. The loader reads commands as text; ingestion does not perform a rollback.

