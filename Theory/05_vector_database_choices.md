# 🧭 Vector Storage — Which Option Fits Which Use Case?

Read [Vector database basics](05_vector_databases.md) first.
These are options to evaluate, not a ranking or fixed size-based rule.

## 🗂️ Four types of solution

| Type | Examples | Why consider it? |
| --- | --- | --- |
| Easy local learning setup | Chroma locally | Practice storing chunks and querying them on a laptop |
| Database with vector support | PostgreSQL + pgvector | Keep vectors close to existing application data |
| Purpose-built vector database | Qdrant, Milvus, Pinecone | Run a separate service focused on vector storage/search |
| Search platform with vector support | Elasticsearch, OpenSearch, Azure AI Search | Combine keyword search, vector search, and filters |

Deployment is a separate choice: **local, self-hosted, or managed**.
For example, Chroma also has a cloud service; it is not limited to demos.
[Chroma deployment options](https://docs.trychroma.com/reference)

## 🛠️ Choose from your situation

| Situation | Options to explore | Small example / main check |
| --- | --- | --- |
| Learning RAG locally | Chroma | Store our runbook chunks; test persistence after restart |
| Already use PostgreSQL | pgvector | Store runbook vectors beside source/owner records; test load on the existing DB |
| Need a dedicated vector service | Qdrant | Team knowledge search; choose and operate an appropriate deployment |
| Need separate components that can scale across machines | Milvus Distributed | A growing document collection; weigh extra infrastructure work |
| Prefer a managed vector service | Pinecone | Focus on the app; check cost, region, data access, and recovery options |
| Already run Elastic/OpenSearch or need keyword + meaning search | Elasticsearch / OpenSearch | Search exact error names alongside descriptions of symptoms |
| Want managed search in Azure | Azure AI Search | Search internal documents using text, vectors, and filters |

These are starting points, not exclusive uses. Compare [pgvector](https://github.com/pgvector/pgvector),
[Qdrant deployments](https://qdrant.tech/documentation/installation/),
[Milvus deployments](https://milvus.io/docs/install-overview.md),
[Pinecone](https://www.pinecone.io/), and
[Azure hybrid search](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview).

## 🏢 Elasticsearch and OpenSearch for enterprise retrieval

**Both can serve as the vector-storage and retrieval layer of an enterprise RAG
system.** They are broader search platforms, not only vector databases.

### ⚙️ How their functions help RAG

| Function | How it works | Why it helps RAG |
| --- | --- | --- |
| 🗄️ Store records | Save chunk text, vector, and source details together in a search index (a named group of records) | Return readable evidence with its source |
| 🔤 Keyword search | Build a word-to-record lookup; BM25 scores matching terms | Find error names such as `CrashLoopBackOff`; configure exact-value fields for IDs |
| 🔢 Vector search | Use a vector index to find stored vectors close to the question vector | Connect “app keeps restarting” with relevant troubleshooting text |
| 🔀 Hybrid search | Combine keyword and vector rankings or adjusted scores | Cover both exact terms and related meaning; raw scores should not simply be added |
| 🏷️ Filtering | Restrict eligible records using fields such as environment and team | Keep staging questions focused on staging documents |
| 🔄 Update/delete | Replace changed records and remove old ones | Avoid returning retired runbooks; the ingestion process must send these changes |

### 📥 Setup once, then search for each question

1. **Define fields:** chunk text, vector, source, and filter fields. Match vector
   dimensions and comparison settings to your embedding model.
2. **Load knowledge:** extract text → chunk → create embeddings → store records.
3. **Ask:** embed the question using the compatible model; run keyword/vector
   search with the required filters.
4. **Answer:** return selected text and sources to your application, which passes
   them with the question to the chat model. Re-ranking is optional.

An embedding model is still needed. Your application can create the vectors,
or you can configure a supported model integration. Storing text alone does not
automatically make it searchable by meaning.

Both document hybrid retrieval combining text and vector search:
[Elasticsearch](https://www.elastic.co/docs/solutions/search/hybrid-search) ·
[OpenSearch](https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/index/).

```text
"Why is api-v2 restarting in staging?"
        ├─ Keywords → api-v2, staging
        └─ Vectors  → related CrashLoopBackOff guidance
                         ↓
           Filter allowed documents + combine results
                         ↓
                 Useful chunks → chat model
```

Access restrictions must come from trusted user permissions and apply to both
search paths. A user-supplied team filter alone does not enforce access control.

✅ **Their role:** store and find evidence. **The chat model's role:** write the
answer using that evidence. Neither a high search score nor hybrid search proves
that the answer is correct.

**Good reason to evaluate them:** your team already operates the platform, or
the application needs both exact terms and meaning-based retrieval.

**Operational checks:** memory/storage, replicas, backups, upgrades, access
permissions, search time, and result quality. Confirm features and licensing for
the chosen version/service. Existing log-search capacity may not cover RAG load.

## ⚠️ Two common mix-ups

- **FAISS is a search library**, not a complete database service. It suits local
  vector-search experiments, but you must add surrounding data-management features.
  [FAISS documentation](https://github.com/facebookresearch/faiss)
- **“Enterprise-grade” is not automatic reliability.** Deployment, permissions,
  tested recovery, monitoring, and workload testing still matter.

## ✅ A quick decision check

1. **Existing platform?** Check whether it can meet the need before adding another service.
2. **Search needs?** Exact identifiers, related meaning, or both?
3. **Operations?** Who handles upgrades, scaling, access, and recovery?
4. **Real workload?** Test your filters, update rate, response time, and costs.

Avoid rules such as “under 50 million vectors means product X.” Vector size,
traffic, hardware, and filters matter too. For our course, learn **one database
practically**; keep the others at this comparison level initially.

## 🎤 Interview FAQ

Key practice questions for this topic; answers are kept short.

1. **Do all RAG systems need a separate vector database?**
   No. An existing database with vector support, such as PostgreSQL with pgvector, may meet the need. Test the workload and operational impact.

2. **When would you evaluate Elasticsearch or OpenSearch?**
   When keyword matches, vector matches, and filters are all useful, especially if the team already operates the platform.

3. **How do Elasticsearch and OpenSearch help a RAG pipeline?**
   They store searchable records and return ranked text with source details. The application passes that evidence to the answering model.

4. **Is FAISS a full database service?**
   No. It is a vector-search library. Persistence workflows, metadata handling, access controls, and other surrounding features need separate consideration.

5. **Managed versus self-hosted: what changes?**
   Managed services handle more infrastructure. You still own data permissions, quality, configuration, and cost; self-hosting adds more deployment and recovery work.

6. **Would you choose a product only by vector count?**
   No. Also test vector dimensions, query traffic, filters, updates, response time, recovery, and total cost.
