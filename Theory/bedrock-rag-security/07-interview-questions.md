# 🎤 Security interview practice

Use the A/B scenario from [the overview](README.md).
These are practice questions, not a measured ranking of interview frequency.

## 🎤 Interview FAQ

1. **A cannot download the S3 incident report but the chatbot reveals it. Why?**
   Ingestion used the Knowledge Base service role. Retrieval exposed an indexed copy without enforcing A's document permissions. The locked-original/unlocked-copy analogy explains the gap.

2. **Can IAM alone protect documents in a shared Knowledge Base?**
   IAM controls supported APIs and resources. It does not automatically carry the engineer's S3 permissions into indexed chunks. Use trusted document checks or a properly configured supported ACL path.

3. **Why introduce Lambda?**
   It maps verified identity to current permissions, builds mandatory filters, checks returned documents, and controls generation. A pass-through Lambda adds no such protection.

4. **Why use Retrieve instead of RetrieveAndGenerate here?**
   We need a checkpoint before generation. Retrieve lets us inspect source IDs and exclude unauthorized evidence before calling the model.

5. **Can A send B's email or request restricted metadata?**
   The backend must ignore identity and access claims from request content. Derive them from verified identity and authoritative permissions, not the question.

6. **What is the difference between IAM and Guardrails?**
   IAM controls AWS access; document rules control evidence; Guardrails checks configured content. A content inspector cannot decide who owns a confidential-file permission.

7. **What changes with native ACL-aware retrieval?**
   Managed Knowledge Bases can filter with supported connector ACLs. The application still verifies user context, protects the retrieval API, and accounts for permission freshness. Managed S3 ACLs are customer-provided, with no live permission recheck.

8. **B loses restricted access. What must change?**
   Update current policies, invalidate cached decisions and answers, and remove or reauthorize old chat context. Sync affected indexed ACLs and block access during the delay. Already delivered information cannot be recalled.

9. **How would you investigate a leak?**
   Stop the affected access path. Correlate protected app request IDs with enabled CloudTrail events; inspect caller mapping, mandatory filters, source labels, role permissions, and caches. Preserve evidence without copying restricted text into tickets.

10. **How would you prove the fix works?**
    Test A and B against the same documents, including direct API bypass, forged identity/filter inputs, missing labels, policy errors, and revocation. Check retrieved text, model input, output, citations, downloads, history, and logs—not just the visible answer.
