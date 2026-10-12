# 🔐 Bedrock RAG Security

**Goal:** explain how engineers receive answers only from documents they may read.
Theory only: no deployment, implementation code, AWS commands, or credentials.

AWS behaviour checked against official documentation on **12 October 2026**.
These are proposed designs, not tested infrastructure.

## 👥 Our example

| Engineer | General runbooks | Restricted incident reports |
| --- | --- | --- |
| A | ✅ Allowed | ❌ Denied |
| B | ✅ Allowed | ✅ Allowed |

Think of a company library: a building pass proves who you are and lets you enter.
It does not open every confidential file.

**Authentication** checks identity. **Authorization** checks what that identity may do.
A secure chatbot needs both.

## 📚 Read in order

| Guide | Main question |
| --- | --- |
| [1. Knowledge Bases](01-bedrock-knowledge-base.md) | Why doesn't S3 access automatically protect indexed text? |
| [2. IAM, SSO, and policies](02-iam-sso-and-policies.md) | Who can call which AWS API? |
| [3. Document authorization](03-document-level-authorization.md) | Which documents may A or B read? |
| [4. Lambda security flow](04-lambda-and-security-flow.md) | Where are decisions enforced? |
| [5. Guardrails](05-bedrock-guardrails.md) | Which content checks complement access control? |
| [6. End-to-end architecture](06-end-to-end-architecture.md) | How do the layers work together? |
| [7. Interview questions](07-interview-questions.md) | Can I explain failures and fixes? |

## 🎯 Design choice

Start with standard Knowledge Bases, trusted metadata filters, and
**Retrieve → check document access → generate**. Lambda is the trusted backend.
For two stable audiences, separate Knowledge Bases can simplify the boundary.

Managed Knowledge Bases offer a separate ACL-aware option; support varies by connector.
See guide 3 before assuming that feature exists in an S3/OpenSearch setup.

## 🧠 Learning depth

- **Understand well:** service identities, document checks, bypass prevention, revocation.
- **Concept only:** native ACL filtering and centralized policy decisions.
- **Basic awareness:** detailed policy syntax and connector setup.

## 🎤 Interview FAQ

1. **What is the security objective?** Only authorized evidence and answers reach each engineer.
2. **Does login solve it?** No. A valid user can still be forbidden from a particular document.
3. **Is this a deployed solution?** No. It is a design to explain and later test.
4. **What is the most important boundary?** Block unauthorized text before it enters generation.
