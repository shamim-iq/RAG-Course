# ✂️ Chunking Strategies — Quick Guide

Read [RAG Fundamentals](00_start_here_rag_fundamentals.md) first.

🧭 **Choosing a method?** Follow the [decision guide](02_choosing_a_chunking_strategy.md)
for a short decision tree and examples by use case.

**Chunking splits documents into smaller pieces for search.** Keep enough text
in each piece to explain the problem and the steps to solve it.

```text
Runbook → [Deploy] [Rollback] [Pod Pending]
Question: "How do I roll back?" → retrieve [Rollback]
```

## 🧠 Strategies: how they work and when to use them

🐍 Code rules · 🔢 Embedding model + code · 🤖 LLM (chat model)

| Strategy | How it works / who decides | Useful for | Main limitation |
| --- | --- | --- | --- |
| Whole document | 🐍 Keep one file as one chunk | Short, single-topic incident notes | Large files mix topics and may exceed model limits |
| Fixed size | 🐍 Cut every N characters or tokens | Simple demos and a starting point for comparison | Can cut a command or explanation in half |
| Sentence/paragraph | 🐍 Keep whole sentences/paragraphs, grouping them up to a limit | Incident reports | A sentence may lack context; a paragraph may be too long |
| Recursive | 🐍 Try paragraphs, then smaller breaks until the text fits | Text with uneven paragraph lengths | Does not know where a complete procedure ends |
| Structure-aware | 🐍 Follow headings, tables, records, or code blocks | Runbooks, Word procedures, CSV, Terraform | Requires the structure to survive text extraction |
| Semantic | 🔢 Embed nearby sentences/groups; code splits where meaning changes | Long text with weak headings and changing topics | Extra model work; splits still need checking |
| Hierarchical | 🐍 Link small pieces to a larger section; find a small piece and return its larger section | Questions needing a full procedure around one matching step | Extra links and search logic; may return more text |
| LLM-guided | 🤖 Model suggests sections; code checks and extracts them | Documents where simple rules give poor results | Slower; the model may miss text or suggest bad splits |

**No strategy requires an agent.** Ollama or Bedrock can run the models where
needed. Calling a model is different from an agent choosing tools and steps.

- Counting tokens does not require an LLM call.
- Basic sentence splitting uses rules; some sentence detectors use a language-processing model.
- Hierarchical splitting needs no model by itself, but can use model-made chunks.
- Reading structure from scanned pages may need separate extraction tools.

## 👀 Each strategy in one example

`[ ... ]` means one chunk. These show the idea, not measured model results.

### 1. 📄 Whole document — keep a short note together

```text
Short incident note → [CPU rose. Pods scaled up. Service recovered.]
```

### 2. 📏 Fixed size — count and cut

```text
"Pod Pending" → [Pod Pe] [nding]
                6 characters per chunk; no overlap in this small example
```

⚠️ The code counts characters, so it can cut a word or command.

### 3. 📝 Sentence/paragraph — cut at natural breaks

```text
"CPU rose. Pods scaled up." → [CPU rose.] [Pods scaled up.]
```

Short sentences can also be grouped; paragraph splitting keeps whole paragraphs.

### 4. 🪜 Recursive — use smaller breaks only when needed

```text
Runbook → [Short paragraph: keep] [Long paragraph: too big]
                                           ↓
                              split at newlines/spaces
```

If pieces still exceed the limit, fall back to character cuts. Exact rules vary.

### 5. 🗂️ Structure-aware — follow headings or records

```text
# Deploy   → [Deploy heading + deployment steps]
# Rollback → [Rollback heading + checks + command + verification]
```

For CSV: `[service: api | status: unhealthy]` keeps column names with values.

### 6. 🔢 Semantic — cut where the topic changes

```text
CPU → Pending pods → autoscaling → TLS certificate expiry
                ↓ embedding comparisons suggest a topic change
[CPU + Pending pods + autoscaling] [TLS certificate expiry]
```

The embedding model helps code find related text; the split is not guaranteed.

### 7. 🌳 Hierarchical — find a small piece, return its larger section

```text
Parent: full rollback procedure
   ├── [Checks]
   ├── [Undo command] ← matches the question
   └── [Verification]
            ↓
Return the parent: checks + undo command + verification
```

### 8. 🤖 LLM-guided — ask a model to suggest complete sections

```text
Mixed troubleshooting document + "Keep each problem and its steps together"
                         ↓ LLM suggests cuts
              [Pending checks] [CrashLoopBackOff checks]
```

Ask for section start/end points. Code must check that nothing is missing and
extract the original text, rather than trusting a model to rewrite it.

**“Context-based” is an unclear label.** It may mean heading rules, meaning-based
splits, or LLM-selected sections. Adding an explanation to an existing chunk is
another possibility; that does not necessarily change where the document is cut.

## 💰 Typical cost: lower → higher

Rough order for **creating/managing chunks after text extraction**, not measured
prices. Strategies in the same group can change order.

| Order | Strategies | Extra work |
| --- | --- | --- |
| 1 — Minimal | Whole document, fixed size | Keep or slice text |
| 2 — Low | Sentence/paragraph, recursive, structure-aware | Apply rules or read document structure |
| 3 — Variable | Hierarchical | Link small/large pieces; possibly store more vectors and return more text |
| 4 — Often higher | Semantic | Extra embeddings and comparisons to choose splits |
| 5 — Often highest | LLM-guided | Model reads the document; code checks its proposed splits |

⚠️ Hierarchical and semantic costs can overlap. **More cost ≠ better answers.**

- All approaches may need search embeddings **after** splitting.
- Keeping a whole file is cheap to prepare, but costly to send if it is long.
- More overlap means duplicate text and work; more retrieved text uses more model input.
- Local Ollama has no per-call API fee, but uses RAM, CPU/GPU, electricity, and time.

## 🎯 Effectiveness: what to try first

There is **no universal accuracy order**. These are trial orders, not proven winners.

| Your data | First → next options | What to preserve |
| --- | --- | --- |
| Deployment runbook | Structure-aware → recursive; compare against fixed size | Checks + commands + verification |
| Tiny incident note | Whole document → paragraphs as it grows | What happened, action taken, recovery |
| Long report without useful headings | Paragraph/recursive → semantic → LLM-guided if needed | Related facts together |
| CSV inventory | One labeled record → related record groups | Column names with values, e.g. `service: api` |
| Long manual | Structure-aware → hierarchical | Full procedure around the matching step |

For Word, keep headings with paragraphs and relevant table rows. For Terraform,
keep related resource blocks. For PDFs, use sections where possible: a page can
end halfway through a procedure. Poor extraction may need fixing before splitting.

## 💻 Our current code: 500 characters + 100 overlap

```text
Chunk 1: text[0:500]
Chunk 2: text[400:900]
Chunk 3: text[800:1300]

Move forward: 500 - 100 = 400 characters
Python chooses cuts → Ollama embeds the finished chunks → save
```

- Each document starts separately; the last chunk can be shorter.
- Your chunk starting with `out=120s` shows a command cut in half.
- Overlap repeats nearby text, but cannot guarantee a complete sentence or command.
- **Embedding chunks afterward does not make the splitting semantic.**

| Setting | Meaning | Our default |
| --- | --- | --- |
| Chunk size | Size limit per piece | 500 characters |
| Overlap | Text repeated between neighboring pieces | 100 characters |
| Top-k | Number of highest-ranked chunks retrieved | 3 |
| Token | A model's text unit; not the same as a character or word | Not used to measure our chunks |

`500/100` are learning defaults, not universal recommendations. Keep chunks within
the embedding model's input limit, and leave room for the question and answer in
the chat model's limit. You can combine strategies: **headings → split oversized
sections recursively → enforce a size limit**.

## 🧪 Choose using your own questions

1. Compare fixed size with heading-based splitting for our runbook.
2. Keep the documents, questions, embedding model, and top-k the same.
3. Check retrieved text for the complete answer, its source, and unrelated/repeated text.
4. Count complete answers, verify model claims, and compare time/resource use.

| Question | Required evidence |
| --- | --- |
| How do I roll back? | Compatibility check + undo command + verification |
| Why might a pod be Pending? | Scheduling events + possible causes |
| What happened during the traffic spike? | Capacity problem + autoscaling + recovery |

A similarity score of `0.8` alone does not prove a better result than `0.6`.

✅ **Choose the simplest method that keeps the needed information together.**
Only fixed-character splitting is implemented in
[our code](../Projects/01_document_processing_and_chunking/code/local_rag.py);
the other approaches here are theory.

## 📚 References

- [LangChain: splitting approaches](https://docs.langchain.com/oss/python/integrations/splitters)
- [AWS: chunking options, parent/child retrieval, and semantic processing costs](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html)
