# 🗄️ Vector Databases — A DevOps Guide

**Goal:** understand, use, troubleshoot, and operate vector storage—not learn
database algorithms in depth. Start with [RAG fundamentals](00_start_here_rag_fundamentals.md).

## 1. What is a vector database?

- Stores embeddings: lists of numbers representing text for comparison.
- Finds records with vectors close to a question's vector.
- Helps return the matching text and its source to the RAG application.
- The embedding model creates vectors; the database stores/searches them. Some
  products can call an embedding model for you.

```text
Runbook → chunks → embedding model → vector database

Question → same embedding model → search + allowed-data filters
                                           ↓
                                matching text + source
                                           ↓
                                 chat model → answer
```

**It finds evidence; it does not guarantee that the final answer is correct.**

## 2. What gets stored?

| Field | Simple example | Why keep it? |
| --- | --- | --- |
| Record ID | `deployment-runbook:chunk-2` | Identify a record for updates/deletion |
| Embedding | `[0.12, -0.08, ...]` | Compare with the query vector |
| Text or reference to text | `kubectl rollout undo ...` | Supply readable evidence to the model |
| Metadata | source, team, environment, updated date | Filter results and show their origin |

The vector numbers above are illustrative. Text can live in the database or
another store, provided each result points to the correct text.

- **Collection:** a logical group of records, such as `devops_runbooks`.
- **Search index:** a structure that makes finding matching vectors faster.
- These are different concepts; product names for them vary.

## 3. 🔎 Regular lookup, keywords, and vectors

| Search | Example | What it matches |
| --- | --- | --- |
| Exact-value lookup | `environment = staging` | A stored field's value |
| Keyword search, such as BM25 | `CrashLoopBackOff` | Words and terms |
| Vector search | “How do I undo a failed release?” | Related meaning, such as rollback instructions |
| Hybrid search | “Undo the release for service api-v2” | Keywords + meaning |

Ordinary exact-value queries do not provide embedding similarity by themselves.
But a regular database can support vector search: PostgreSQL with **pgvector**
supports exact and approximate nearest-neighbor search.
[pgvector documentation](https://github.com/pgvector/pgvector)

✅ A separate vector database is an option, not a requirement for every RAG system.

## 4. 📐 Similarity, top-k, and filters

- **Nearest neighbors:** vectors closest to the question vector under the chosen comparison.
- **Top-k:** return up to k best matches, not k guaranteed correct answers.
- **Similarity:** generally, higher means closer. **Distance:** generally, lower means closer.
- **Threshold:** a minimum similarity or maximum distance used to reject weak matches.
  Test it with your questions; scores are not confidence percentages.

```text
Question: "How do I roll back staging?"
Filter: environment=staging AND team=platform
                         ↓
Search eligible records → top 3 → text + sources
```

Filtering before, during, or after vector lookup depends on the product/index.
Check whether restrictive filters leave fewer than k results.

🔐 Filters for document access must come from trusted user permissions. A
user-entered `team=platform` label is not authorization. Unauthorized text must
never reach the answering model.

## 5. ⚡ Indexes: speed versus missed matches

| Approach | Simple meaning | Trade-off |
| --- | --- | --- |
| Exact search | Find the true nearest vectors; our demo compares every vector | Simple for small data, more work as data grows |
| Approximate search | Use an index to find likely nearest vectors faster | May miss some of the true nearest vectors |

- **Recall:** how many desired matches were found. For index checks, compare
  approximate results with exact nearest-neighbor results.
- Perfect nearest-neighbor recall does not mean perfect answers: embeddings can
  still rank an unhelpful passage highly.
- Recognize index names such as HNSW and IVF; learn their speed/memory/search-quality
  trade-offs when using them. No algorithm derivations needed now.

## 6. 🔄 Keep the stored knowledge current

| Operation | What it does | DevOps example |
| --- | --- | --- |
| Insert | Add a new record | Add a new troubleshooting runbook |
| Upsert | Insert or update using the record ID | Re-run ingestion without adding duplicate records |
| Delete | Remove records | Remove chunks from a retired procedure |
| Update metadata | Change source labels/details | Change the owning team without changing text |

When a document changes:

```text
Read new version → chunk → embed → replace its records → remove obsolete chunks
```

- Use consistent IDs and track the source/version. If five chunks become three,
  upserting three records alone may leave two old ones behind.
- **Embedding dimensions:** the number of values in a vector. Check the store
  accepts that size and uses the model's intended comparison method.
- Use compatible query/document embeddings. Same vector length alone is not enough.
- Changing the embedding model usually requires **re-embedding** source text.
- **Rebuilding a search index** may reuse existing vectors; it is not the same operation.
- For larger migrations, prepare and test a new collection before switching traffic.

## 7. 🛠️ What matters operationally?

| Area | What to understand or check |
| --- | --- |
| Persistence | Does data survive a restart? Where are the files/volumes? |
| Scaling | Vector count and dimensions, memory, disk, query traffic, filters, update rate |
| Backup/restore | Save data, metadata, and configuration; test recovery and know what can be rebuilt |
| High availability | Replicas and failover reduce downtime; replication is not a backup |
| Security | Authentication, allowed networks, encrypted connections, secrets, user/document permissions |
| Monitoring | Search/indexing time, errors, memory/disk, query volume, and document freshness |
| Quality | Do known questions retrieve the required evidence after updates? |
| Cost | Storage, replicas, model calls, rebuilds, and query load |

Example: a fast response that returns yesterday's rollback command is still a failure.

## 8. ⚖️ Choosing a product: avoid fixed rules

🧭 See [Vector storage choices by use case](05_vector_database_choices.md) for a
short comparison, including Elasticsearch and OpenSearch for enterprise retrieval.

| Option | What you take responsibility for |
| --- | --- |
| Local/embedded database | Files, persistence, backups, and limits of one-machine use |
| Self-hosted service | Deployment, upgrades, storage, scaling, backups, and availability |
| Managed service | Provider handles more infrastructure; you still own data access, quality, configuration, and cost |

- Learn the course database practically first; compare other products by your needs.
- **Chroma:** a starting point for collection/add/query exercises; its query API
  accepts text or embeddings and can return distances.
  [Chroma query guide](https://docs.trychroma.com/docs/querying-collections/query-and-get)
- **FAISS:** a vector similarity-search library, not a complete database service.
  [FAISS documentation](https://github.com/facebookresearch/faiss)
- Prefer testing requirements over rules such as “below 50 million vectors, use X.”
- Index-build memory spikes vary; “2–3× memory” is not universal.
- Hybrid-search charges depend on the service; check its pricing.
- Document changes need updates; not every metadata or schema change requires
  regenerating all embeddings.

## 9. 🎓 How deeply should you learn?

| Topics | Depth required |
| --- | --- |
| Stored records, top-k, filters, score meaning | Understand well |
| Add/upsert/delete, duplicates, stale data, model compatibility | Understand well |
| Persistence, security, monitoring, recovery, scaling trade-offs | Understand well |
| Exact/approximate search and index trade-offs | Concept only |
| Hybrid search and managed/self-hosted choices | Concept only |
| Index algorithm details and vendor-specific tuning knobs | Basic awareness |

## 10. 🧪 Future small lab

Using one database and our existing sample documents:

1. Store chunks, embeddings, IDs, and metadata.
2. Search for rollback steps and filter by environment.
3. Update a document; confirm its old chunks disappear.
4. Run ingestion twice; confirm there are no duplicates.
5. Restart storage; confirm records survive.
6. Ask an unrelated question; inspect the nearest matches rather than assuming relevance.

This is a learning checklist only; no new database project is created yet.
Our current JSON store is still the small working example.

📚 Related: [Retrieval methods](03_retrieval_methods.md) ·
[Scoring and re-ranking](04_scoring_and_reranking.md)

## 🎤 Interview FAQ

Key practice questions for this topic; answers are kept short.

1. **What does a vector database store?**
   Vectors linked to record IDs, metadata, and readable text or a reference to that text. This supports matching and tracing results to their sources.

2. **Exact versus approximate nearest-neighbor search?**
   Exact search finds the true closest vectors under the chosen measure. Approximate search can be faster but may miss some of those matches.

3. **How do you prevent stale or duplicate chunks?**
   Use stable IDs, track source versions, update changed records, and delete obsolete chunks. Upserting new chunks alone may leave old ones behind.

4. **What happens if the embedding model changes?**
   Usually re-embed the source text and test a new store before switching. Equal vector dimensions do not make different model outputs compatible.

5. **What should a platform engineer monitor?**
   Search and indexing time, errors, memory/disk, update freshness, and whether test questions retrieve the required evidence.

6. **Are metadata filters enough to protect private documents?**
   Only when access restrictions are enforced from trusted permissions. A user-supplied team label is not authorization; unauthorized text must not reach the model.
