# 🔎 Scoring and Re-ranking — From Question to Answer

Read [RAG Fundamentals](00_start_here_rag_fundamentals.md) first.

**Scoring** gives each chunk a matching score. **Ranking** sorts those scores.
**Re-ranking** takes the first results and checks their relevance again.

## 🧭 What happens when you ask a question?

```text
"How do I roll back the staging API?"
                    ↓
Bi-encoder: turn the question into a vector
                    ↓
Compare with stored chunk vectors → retrieve promising chunks
                    ↓
Optional cross-encoder: read question + each chunk together → re-rank
                    ↓
Choose the best few chunks → send their text + question to the chat model
                    ↓
Answer with source references → check against the evidence
```

For a larger collection, you might retrieve 20 chunks and keep 3 after re-ranking.
These are example counts, not recommended defaults for every project.

## 1. ⚡ Bi-encoder — find possible matches quickly

An **encoder** turns text into numbers. A bi-encoder processes the question and
chunk **separately**, commonly using the same embedding model for both.

```text
During ingestion: chunk    → embedding model → chunk vector → save
For each query:   question → embedding model → query vector
                                                  ↓
                        Compare query vector with saved chunk vectors
```

- “Bi” describes the two separate text paths, not necessarily two different models.
- Chunk vectors can be prepared once and reused for many questions.
- This is fast for finding likely matches, but it can favor related wording
  over the passage that gives the exact answer.

This separate-encoding approach supports efficient first-stage search.
[Sentence Transformers: bi-encoders and cross-encoders](https://www.sbert.net/examples/cross_encoder/applications/README.html)

## 2. 📐 Cosine similarity — compare the vectors

Think of vectors as arrows. **Cosine similarity compares their directions.**

```text
Query vector + chunk vector → cosine comparison → score → sort highest first
```

- Scores range from **−1 to 1**; closer directions have higher scores.
- `1` means the same direction—not proof that the text answers the question.
- `0.641` does **not** mean “64.1% accurate.”
- In our code, the embedding model creates vectors; Python's
  `cosine_similarity()` calculates the comparison afterward.
- Cosine is one comparison method. Some embedding models use other methods,
  such as a dot product; use the method intended for the model.

**You need the idea, not the mathematical formula.**

## 3. 🎯 Cross-encoder — examine each possible match more closely

A cross-encoder reads the **question and one chunk together**, then produces a
score for how relevant that pair is.

```text
[Question + deployment chunk] → cross-encoder → relevance score
[Question + rollback chunk]   → cross-encoder → relevance score
                                             ↓
                                  Sort using the new scores
```

- Unlike the bi-encoder stage, it does not compare two separately stored vectors.
- It must process new question/chunk pairs, so use it on a shortlist rather
  than every document in a large collection.
- It can improve ordering, but may still make mistakes.
- Its score scale depends on the model; do not compare it directly with cosine
  scores or assume it is an answer-confidence percentage.
- It scores passages; the **chat model** still writes the final answer.

This two-stage pattern combines quick search with a more detailed second check.
[Sentence Transformers: retrieve and re-rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

## 🛠️ Example from our rollback question

| Chunk | Your observed cosine result | Possible result after re-ranking |
| --- | --- | --- |
| Deployment instructions | 0.641 — first | Second: related, but does not explain rollback |
| Rollback procedure | 0.629 — second | First: contains the undo command and checks |
| Incident notes | 0.439 — third | Third: does not explain this procedure |

The last column is **illustrative**, not an executed cross-encoder result.
Re-ranking can only reorder the chunks it receives. If initial retrieval keeps
only the deployment chunk, a re-ranker cannot recover the missing rollback chunk.

## ⚖️ Roles at a glance

| Component | Input → output | Main job |
| --- | --- | --- |
| Bi-encoder | Each text separately → vector | Prepare text for fast matching |
| Cosine comparison | Two vectors → similarity score | Rank possible matches |
| Cross-encoder | Question + chunk together → relevance score | Reorder the shortlist |
| Chat model / LLM | Question + chosen passages → answer | Explain the evidence in words |

## ✅ What helps produce accurate answers?

- **Correct sources:** outdated runbooks can produce outdated answers.
- **Useful chunks:** keep commands with their checks and explanations.
- **Good retrieval:** include the needed evidence in the first results.
- **Optional re-ranking:** prioritize passages that directly answer the question.
- **Enough context:** do not drop necessary checks to keep the answer short.
- **Clear instructions:** request source references and “not found” when evidence is missing.
- **Check the answer:** verify each claim against the selected text. A citation alone is not proof.

⚠️ No score or re-ranker guarantees correctness. For rollback, check whether the
answer includes **compatibility checks + undo command + health verification**.
Compare the same test questions with and without re-ranking, including time taken.

## 💻 What our project currently does

```text
Ollama embeddings → Python cosine scores → top-k chunks → optional chat answer
```

- Our separate question/chunk embeddings follow the bi-encoder pattern.
- **No cross-encoder or re-ranking step is implemented.**
- `--retrieve-only` shows the first-stage matches without calling the chat model.
- A minimum matching score would need testing; top-k currently returns the
  nearest chunks even when none contains the answer.
- Re-ranking is optional and needs no agent. This document adds theory only.
