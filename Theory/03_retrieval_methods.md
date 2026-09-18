# 🔎 Retrieval Methods

📚 **Documents** → 🔎 **Search method** → 🎯 **Top matches** → 🤖 **Answer with context**

Read [RAG fundamentals](00_start_here_rag_fundamentals.md) first. This note
explains common retrieval methods before the model writes an answer.

## 🎯 Why retrieval matters

Retrieval decides which chunks reach the answer step.

If retrieval misses the rollback procedure, the chat model cannot safely answer a
rollback question. If retrieval sends noisy chunks, the answer may include
unrelated details.

```text
Question: "How do I roll back staging?"
          ↓
Retriever finds matching chunks
          ↓
Chat model answers from those chunks
```

Retrieval is not the same as generation. Retrieval finds evidence. Generation
turns evidence into an answer.

## 🔤 Keyword vs semantic search — the basic difference

| | Keyword search | Semantic search |
| --- | --- | --- |
| Main question | “Does this text contain the search words?” | “Does this text express a related idea?” |
| Example retrieval methods | **TF-IDF-based retrieval**, **BM25** | **Dense retrieval** using embeddings, such as a bi-encoder with cosine similarity |
| Model needed? | No neural model for basic TF-IDF/BM25 | Yes, for the embedding-based approach here |
| Best clue | Error names, service IDs, command names | A description in the user's own words |

💡 **Semantic search** is the goal of matching meaning; **dense retrieval** is a
common way to do it. TF-IDF and BM25 are specific keyword-scoring methods.
Our demo uses dense retrieval with Ollama embeddings and cosine similarity.

```text
Saved text: "Rollback procedure: restore the previous release."

"rollback procedure" → keyword search has a direct word match
"undo a bad deploy"  → semantic search may find the same text through meaning
```

- Keyword search can handle case changes, word forms, or synonyms if configured.
- Exact flags/IDs need suitable text handling: splitting punctuation can change matches.
- Semantic search is not guaranteed to recognize every synonym or exact identifier.

## 1. 🔤 Keyword scoring: TF-IDF → BM25

### TF-IDF: give useful words more weight

**TF-IDF = Term Frequency × Inverse Document Frequency.**
In our RAG examples, each chunk is a searchable “document.”

| Part | Simple question | Example |
| --- | --- | --- |
| TF — term frequency | How often does this word appear in this chunk? | Repeated `rollback` can suggest the chunk discusses rollback |
| IDF — inverse document frequency | How rare is this word across all chunks? | A word in only 2 of 100 chunks gets more weight than one in 90 |

```text
Word appears in this chunk + is uncommon across the collection
                              ↓
                    Give that word more weight
```

- TF-IDF builds word weights from counts; it does not learn the meaning of words.
- A common search approach compares query and chunk TF-IDF vectors using cosine similarity.
- A rare word only helps a query if it matches a query term; rarity alone does not make a chunk relevant.

### How BM25 connects to TF-IDF

Both use **matching words, their frequency, and their rarity**. BM25 uses a
different scoring formula with two useful controls:

- **Diminishing benefit from repetition:** the 20th `rollback` adds less than the first few.
- **Length adjustment:** account for a chunk's length relative to the collection's average.

Example: a long page repeating `rollback` should not automatically outrank a
short, focused rollback procedure. BM25 balances these signals; it does not
guarantee that the shorter passage wins.

TF-IDF has several versions, including ones that adjust counts and length.
Think of BM25 as a related keyword-ranking method, not TF-IDF followed by an LLM.
[Elastic's BM25 explanation](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables)

### BM25 in a DevOps search

Here, **sparse retrieval** means keyword search using word counts and weights. A
common method is **BM25**, a keyword scoring method used by many search systems.

```text
Question: "CrashLoopBackOff logs"
          ↓
BM25 prefers chunks containing words like "CrashLoopBackOff" and "logs"
```

BM25 scores text using signals like:

- Whether the query words appear in the chunk.
- How often those words appear.
- How rare those words are across the document set.
- How long the chunk is.

### ✅ Good for

- Exact names: `CrashLoopBackOff`, `kubectl`, `deployment/api`.
- Error codes, service names, ticket IDs, command flags, and namespaces.
- Cases where users know the exact term in the document.

### ⚠️ Limits

- It can miss related wording.
- "Pods cannot schedule" may not match a chunk that says "Pending pods" well.
- It does not understand meaning beyond the words it can match.

## 2. 🔢 Dense retrieval

**Dense retrieval** uses embeddings. An embedding is a list of numbers that
represents the meaning of text.

### Why turn text into vectors?

A **vector** is a list of numbers. Numbers let us compare and sort thousands of
possible matches using the same scoring rule.

**The numbers must represent something useful:** random numbers or character
codes alone do not make meaning-based search possible.

| Representation | What the numbers describe | What matching can capture |
| --- | --- | --- |
| TF-IDF vector | One weight per vocabulary word; most are zero (“sparse”) | Shared words and their importance |
| Learned embedding | A compact list of model-produced values (“dense”) | Patterns learned from language, including related wording |

```text
Toy vocabulary: [rollback, cpu, pending]
Query "rollback" → [1, 0, 0]
Rollback text    → [2, 0, 0]  ← same direction
CPU text         → [0, 2, 0]  ← different direction
```

These are simplified word weights, not calculated TF-IDF values. With this tiny
vocabulary, `undo` has no entry: word matching alone cannot link it to `rollback`.

```text
"undo a bad deploy" → embedding model → query vector
"rollback steps"   → embedding model → chunk vector
                                         ↓
                        vectors may be close despite different words
```

- The model learned language patterns during training; it does not retrain on our files.
- Individual embedding values usually do not have labels such as “CPU” or “rollback.”
- Use compatible query/chunk embeddings from the same retrieval model, following
  its query/document instructions where required.
- **Cosine similarity compares vector directions.** It can compare TF-IDF or
  learned embeddings; the representation determines what the similarity means.
- BM25 normally scores matching terms directly; it does not need cosine similarity.

Embedding-based search compares question and passage vectors to find related text.
[Sentence Transformers: semantic search](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)

Dense retrieval includes creating the query vector and searching stored chunk
vectors. Vector search is part of this process, not a later retrieval method.

```mermaid
flowchart TD
    Q["❓ Question: How do I undo a bad deploy?"]
    S["🗄️ Stored chunk vectors created during ingestion"]
    subgraph D["🔢 Dense retrieval"]
        E["🔢 Same embedding model used for chunks"]
        V["🔢 Query vector"]
        subgraph VS["🔎 Vector search"]
            C["📊 Compare with stored chunk vectors using cosine similarity or dot product"]
            K["🎯 Select top-k matching chunks"]
        end
        R["📚 Return chunk text and source metadata"]
        E --> V --> C --> K --> R
    end
    Q --> E
    S --> C
    classDef input fill:#dbeafe,stroke:#2563eb,color:#111827
    classDef embedding fill:#f3e8ff,stroke:#9333ea,color:#111827
    classDef search fill:#fef3c7,stroke:#b45309,color:#111827
    classDef result fill:#dcfce7,stroke:#15803d,color:#111827
    class Q,S input
    class E,V embedding
    class C,K search
    class R result
```

- 🔢 **Embedding stage:** converts text into vectors.
- 🎯 **Search stage:** scores vector matches and selects the top-k chunks.
  Cosine similarity or dot product is a scoring function within this step.
  Use the function expected by the embedding model; our demo uses cosine similarity.
- 📚 **Result stage:** returns the selected text and metadata for the answer prompt.

Dense retrieval can find related ideas even when the words differ.

Example:

| Question wording | Useful document wording |
| --- | --- |
| undo a bad deploy | rollback procedure |
| pods cannot schedule | pods Pending |
| app keeps restarting | CrashLoopBackOff |

### ✅ Good for

- Natural language questions.
- Runbooks where users ask in different words.
- Incident notes that describe the same issue in several ways.

### ⚠️ Limits

- It may miss exact strings that matter, such as `--timeout=120s`.
- It can retrieve text that feels related but does not answer the question.
- It needs an embedding model and a vector store or vector index.

## 3. 📍 Vector search

**Vector search** is the search step used by dense retrieval.

The system compares the question vector with stored chunk vectors and returns
the closest matches.

```text
Saved chunk vectors:
[rollback chunk vector]
[incident chunk vector]
[pod troubleshooting vector]

Question vector → compare → top-k closest chunks
```

In our local demo, Python compares every stored vector in a JSON file. That is
simple and useful for learning.

In larger systems, a vector database or vector index is used so search stays
fast when there are many chunks.

### ✅ Good for

- Searching many embedded chunks.
- Finding meaning-based matches.
- Returning top-k chunks for the RAG prompt.

### ⚠️ Limits

- A close vector score is not proof that the chunk answers the question.
- Vector search depends on chunk quality.
- Rebuild vectors after changing documents, chunk settings, or embedding model.

## 4. 🔀 Hybrid search

**Hybrid search** combines sparse search and dense search.

```text
Question
  ├─ BM25 finds exact keyword matches
  └─ Dense retrieval finds meaning matches
          ↓
Combine and rank results
```

This is useful because DevOps questions often need both exact terms and meaning.

Example:

```text
"Why did api pods stay Pending in EKS?"
```

- BM25 helps match `api`, `Pending`, and `EKS`.
- Dense retrieval helps match related text about unschedulable pods, node
  capacity, and autoscaling.

### ✅ Good for

- Mixed queries with exact terms and plain language.
- Production RAG systems where missing exact identifiers is risky.
- DevOps docs with commands, service names, error names, and explanations.

### ⚠️ Limits

- It needs extra ranking logic.
- BM25 and dense scores use different scales, so they cannot be blindly compared.
- It may still need re-ranking to put the best evidence first.

## 🔀 How the search methods fit together

| Method | What it matches | Strong when | Weak when |
| --- | --- | --- | --- |
| Sparse / BM25 | Exact words and terms | The query contains error names, commands, or service IDs | The user asks with different wording |
| Dense | Meaning through embeddings | The query is natural language | Exact flags, IDs, or rare terms matter |
| Vector search | Closest stored vectors | You need fast meaning-based lookup | Chunks or embeddings are poor |
| Hybrid | Keywords plus meaning | DevOps questions mix exact terms and intent | Ranking is not tuned |

## 🛠️ How this fits our current project

Our current local RAG demo uses dense retrieval:

```text
Chunks → Ollama embeddings → JSON vector store
Question → query embedding → cosine similarity → top-k chunks
```

It does **not** implement TF-IDF, BM25, or hybrid search yet.

A future hands-on lab could compare:

- BM25 only: good for exact Kubernetes terms.
- Dense only: good for natural wording.
- Hybrid: useful when both matter.

## 🧰 Practical DevOps examples

| User question | Retrieval method to try first | Why |
| --- | --- | --- |
| What should I inspect for `CrashLoopBackOff`? | BM25 or hybrid | Exact error name matters |
| How do I undo a failed staging release? | Dense or hybrid | "Undo" should match rollback |
| Which command checks rollout status? | BM25 | Exact command text matters |
| Why were pods unschedulable during the spike? | Dense or hybrid | Related wording may appear across incident notes |

## 📝 What to remember

| Concept | Depth required |
| --- | --- |
| TF-IDF: frequent in this chunk, rare across the collection | Concept only |
| Sparse/BM25 exact-term matching | Understand well |
| Dense retrieval with embeddings | Understand well |
| Vector search as the lookup over embeddings | Understand well |
| Hybrid search combining sparse and dense results | Understand well |
| Score merging, vector index internals, and ranking formulas | Basic awareness |

✅ Start simple. Use BM25 when exact terms matter, dense retrieval when meaning
matters, and hybrid search when a real system needs both.

Next: [Scoring and re-ranking](04_scoring_and_reranking.md) explains how a second
model can reorder retrieved results before the chat model writes an answer.
