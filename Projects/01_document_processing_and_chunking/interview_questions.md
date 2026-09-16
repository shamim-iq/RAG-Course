# Interview Questions: Ingestion Basics

Preparation material for the introductory topic. Practice status: not yet validated.
Extend this file as new activities are covered.

## Fundamentals

1. **What does document ingestion mean?**
   Bringing source content into a processing pipeline, starting with loading
   and text extraction.
2. **Why is a file path insufficient as knowledge?**
   It identifies a location; the pipeline must read the file's content.
3. **How can Markdown and plain text be loaded initially?**
   Read them as text using standard Python file handling.
4. **Does loading documents mean the assistant can answer questions?**
   No. It only makes their content available for later processing.

## Scenarios

1. **A loader returns only runbook filenames. Is ingestion complete?**
   No. It must also read the actual runbook content.
2. **A team adds PDF runbooks. Can we assume the text loader is sufficient?**
   No. PDF content needs format-specific extraction.
3. **The sample files exist, but the loader has never run. Is the lab complete?**
   No. Record preparation as complete and execution/validation as pending.

## DevOps relevance

1. **Which operational documents are useful sources for this project?**
   Kubernetes troubleshooting notes, deployment runbooks, and incident records.
2. **Does ingesting a rollback runbook execute its commands?**
   No. The loader reads commands as text; ingestion does not perform a rollback.

