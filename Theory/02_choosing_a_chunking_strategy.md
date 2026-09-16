# 🧭 Choosing a Chunking Strategy

**Start with the simplest method that keeps the answer together.** These are
choices to test, not a guaranteed accuracy ranking.
See [strategy explanations](02_chunking_strategies.md) for how each method works.

## 1. ❓ Start with the question

Ask: **What information must stay together to answer this?**

```text
"How do I roll back staging?"
              ↓
Compatibility checks + rollback command + health verification
              ↓
Keep these in one section, if they fit within the model's limits.
```

Choosing by file extension alone is not enough: two PDFs may contain a short
incident note and a long manual, which need different treatment.

## 2. 🌳 Follow this decision tree

```text
Can you read the extracted text correctly?
├─ No  → Fix extraction first; scans may need OCR (reading text from images).
└─ Yes
   ├─ Short, single topic, fits model limits? → Whole document
   ├─ Clear headings, records, or code blocks? → Structure-aware
   │    └─ Section too large? → Split that section using smaller breaks
   └─ Mostly plain paragraphs? → Paragraph or recursive splitting
        └─ Related information still gets separated?
             → Try semantic splitting if the extra model work is affordable
```

**Two further options when the results show a need:**

- 🌳 Search finds a small step but the answer needs its whole procedure → try
  **hierarchical retrieval**: find a small chunk, then supply its larger section.
- 🤖 Rules and meaning comparisons still produce poor sections → try
  **LLM-guided splitting**, checking that the model's cuts lose no original text.

📏 **Fixed size** is a useful first experiment for comparison. It can be enough
if your questions get complete answers; you do not have to replace it.

## 3. 🛠️ Match the use case

| Example question and source | First choice to test | What a useful chunk contains |
| --- | --- | --- |
| “What happened?” — short incident note | Whole document | `[Problem + action + recovery]` |
| “How do I roll back?” — Markdown runbook | Structure-aware | `[Rollback heading + checks + commands]` |
| “What caused the outage?” — long incident report | Paragraph/recursive | `[Related cause and explanation]` |
| “Which service owns this alert?” — CSV inventory | Structure-aware: records | `[service: api, owner: platform, alert: high CPU]` |
| “What does this resource do?” — Terraform | Structure-aware: code blocks | `[Resource block + explanation]`; retain needed references |
| “How do I recover the service?” — long manual | Sections; then hierarchical if needed | Match `[Recovery command]`, return `[Full recovery procedure]` |
| “What changed between CPU and TLS issues?” — unstructured notes | Try semantic if simple splits fail | `[CPU-related facts] [TLS-related facts]` |

For broad questions covering several topics, retrieving more relevant chunks
may help more than changing the splitter. Inspect the selected text first.

## 4. 💰 Check what your laptop or service must do

| Approach | Who chooses the cuts? | Typical extra work after text extraction |
| --- | --- | --- |
| Whole document / fixed size | 🐍 Code | Minimal |
| Paragraph / recursive / structure-aware | 🐍 Code rules | Low for simple text |
| Hierarchical | 🐍 Code links smaller and larger chunks | More links, storage, and possibly answer text |
| Semantic | 🔢 Embedding model + code comparisons | Extra model calls or local processing |
| LLM-guided | 🤖 Chat model suggests cuts; code checks them | Often the most model work |

- These are rough costs, not measured prices; implementations can change the order.
- Local models still use memory, processing power, and time.
- All methods may need embeddings afterward for search. No agent is required.
- Small chunks with heavy overlap can create many repeated matches.
- Keep each chunk within the embedding model's limit; leave space for the question
  and answer when sending selected chunks to the chat model.

## 5. 🧪 Let results decide

Compare two choices using the **same documents, questions, embedding model, and top-k**.
Top-k is the number of chunks retrieved. Start with a few realistic questions.

| Check | Simple example |
| --- | --- |
| Complete evidence? | Rollback result includes checks, command, and verification |
| Text intact? | No command starting halfway through, such as `out=120s` |
| Little unrelated text? | Rollback results are not mostly CPU incident notes |
| Answer supported? | Every suggested step appears in the selected text |
| Affordable? | Compare processing time, memory use, and amount of stored text |

If top-k is unchanged, larger chunks still send more text. Note that difference
when judging results. **A higher similarity score alone does not prove better answers.**

## ✅ Decision for our current project

```text
Current: fixed 500-character chunks + 100-character overlap
Observed: one chunk starts inside a command
Next comparison: split the deployment runbook by headings
Keep together: rollback checks + undo command + verification
```

This is a suggested experiment, not an implemented code change. Keep the method
that answers your test questions well with the least unnecessary work.

📚 Further reading: [AWS chunking guide](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html)
describes fixed-size, semantic, and parent/child chunking. The choices above are
practical suggestions for our sample documents, not published benchmark results.
