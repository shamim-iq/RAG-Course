# Learning code preferences

## Plain-language rule for all documentation

- Apply this rule to every new or edited documentation file, including README
  files, theory, practical notes, interview questions, and progress trackers.
- Use short sentences, familiar words, bullets, and concrete DevOps examples.
- Avoid jargon. Keep necessary terms such as embedding, retrieval, and token,
  but explain them in plain words when first introduced. Expand unfamiliar acronyms.
- Prefer "run the model" to "inference", "check the result" to "validation",
  and "minimum matching score" to "relevance threshold".
- Keep commands, code names, paths, and technical meaning accurate. Do not rename
  them just to simplify prose. Avoid repeating definitions when a short link helps.
- Keep docs brief; remove repeated explanations and keep useful diagrams/tables.

## Code and learning conventions

- Use light, meaningful emojis and symbols in learning documentation to aid
  scanning (e.g. 📥 ingestion, ✂️ chunking, 🔢 embeddings, 🎯 effectiveness).
  Keep text labels so meaning does not depend on icons. Compare strategy costs
  with explicit assumptions; present effectiveness by scenario, never as an
  unsupported universal accuracy ranking.
- When documenting chunking strategies, identify what selects boundaries:
  code rules/parsers, an embedding model plus code, or a generative LLM. Distinguish
  boundary selection from subsequent embedding and from agent orchestration.

- Keep hands-on code simple, readable, and related to realistic DevOps examples.
- Add concise function docstrings and comments explaining intent, decisions, and
  data flow. Avoid commenting every line or explaining obvious syntax.
- Highlight only complete sections central to the concept being learned, using
  these exact Python markers:
  `# You should understand ----------------------------------------------------->`
  and `# -------------------------------------------------------------------------->`.
- Immediately above each highlighted section, explain WHAT it does and WHY it
  matters in 1–3 short comment lines. Do not highlight every line.
- For RAG, highlight ingestion, chunking/overlap, embeddings, vector storage,
  query embeddings, similarity comparison, Top-K, context, and LLM generation.
- Leave CLI/HTTP/JSON/filesystem boilerplate and cosine-math implementation
  unmarked. Teach cosine similarity conceptually rather than requiring formulas.
- Prefer explicit loops and descriptive names over compact Python tricks;
  avoid frameworks, excessive validation, exception layers, and abstractions.
- Include a short data-flow overview at the top of pipeline files. Before
  simplifying code, state the planned simplifications and highlighted sections.
- Provide a concise learning summary using only these depth levels:
  Understand well, Concept only, Basic awareness.
- Calibrate explanations for a DevOps/Platform Engineer with about four years
  of experience who needs to read, modify, troubleshoot, and operate RAG systems.
- Explain useful parameters and their units, such as characters versus tokens.
- Apply these conventions to future code created or substantially updated here.
- Keep execution and validation commands available for the user to run manually.
- Whenever a Python file is added, renamed, removed, or changes purpose under a
  project's `code/` directory, update that directory's `README.md` in the same
  change. Include a clickable file link, brief purpose, concrete use case, and
  whether it is format-specific or shared across workflows. Distinguish loading
  documents from querying an existing store; do not imply every reader runs for
  every command. Keep the guide brief.
