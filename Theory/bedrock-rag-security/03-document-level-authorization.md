# 🏷️ Document-level authorization

## 📋 Classification and ACLs

An **ACL (access control list)** says who may read a document.
A classification such as `restricted` describes the document; it does not enforce anything alone.

- **Concept:** combine verified user permissions with trusted document labels.
- **Analogy:** the confidential-file sticker tells the librarian which access rule to apply.
- **AWS example:** A is allowed `general`; B is allowed `general` and `restricted`. Lambda creates the search filter from that permission decision.
- **If misconfigured:** accepting `restricted=true` from the browser lets A choose their own access.
- **Takeaway:** the server chooses mandatory filters. A question or model-generated filter cannot broaden access.

| Data | Trusted owner |
| --- | --- |
| User identity and group membership | Identity system / server-side mapping |
| Document ID, classification, allowed users | Document owner and controlled ingestion |
| Effective search filter | Backend authorization logic |

All chunks need correct labels and a stable source-document ID. Missing or unknown labels are denied.
User search preferences are combined with mandatory access filters using **AND**, never used to replace them.

## ⚖️ Verified Permissions

- **Concept:** Amazon Verified Permissions evaluates “may this person read this document?” using application policies.
- **Analogy:** the librarian consults the company's access register.
- **AWS example:** Lambda supplies trusted identity, action `read`, document ID, and relevant attributes; the service returns ALLOW or DENY.
- **If misconfigured:** invented group attributes or ignoring DENY makes the decision meaningless.
- **Takeaway:** Verified Permissions decides; Lambda enforces. It does not automatically create search filters or discover your document permissions.

[Verified Permissions decision API](https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_IsAuthorized.html)

## 🧩 Native ACL-aware retrieval: a different option

For **Bedrock Managed Knowledge Bases**, AWS documents:

| Connector | Permission filtering | Live permission recheck |
| --- | --- | --- |
| SharePoint, OneDrive, Google Drive, Confluence | Synced ACLs | Supported |
| S3, Custom | Customer-provided ACL data | Not supported |
| Web Crawler | No ACL support | Not applicable |

The application must authenticate users and supply verified identity context.
AWS warns that this filtering is **not a standalone security boundary**.
Use the connector's identity format; do not accept an arbitrary user email from the request.
[AWS connector matrix and identity rules](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-acl.html)

- **Analogy:** a librarian can check a named reader's access list, but someone must first verify the reader's badge.
- **AWS example:** Managed S3 uses configured ACL files, not automatic interpretation of the engineer's S3 IAM permissions. Its documented entries identify users by email. Per-document ACLs override matching global entries.
- **If misconfigured:** an app that trusts a caller-supplied B identity can filter as B for A.
- **Takeaway:** verify identity upstream and block direct bypass routes.

Managed S3 ACL changes need affected content reindexed; missing ACL entries prevent ingestion.
[AWS S3 ACL details](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-ds-s3-acl.html)

## 🔄 Revoking access

- **Concept:** a former permission must stop authorizing future answers.
- **Analogy:** withdrawing a confidential-room pass also means invalidating cached door approvals.
- **AWS example:** B loses incident-report access. Update the authoritative policy immediately, invalidate permission caches, and deny restricted results while indexed ACLs catch up.
- **If misconfigured:** stale filters, cached answers, or old chat history can reveal previously authorized text.
- **Takeaway:** recheck access on requests and before generation; sync is not an immediate revocation mechanism.

Also clear or reauthorize cached answers, source downloads, and conversation context.
Check access again before releasing a response when revocation may occur during processing.
Already delivered information cannot be recalled.

## 🎤 Interview FAQ

1. **Is metadata an access control by itself?** No. Trusted code must enforce it on every path.
2. **What if permission lookup fails?** Deny affected access; never retry without filters.
3. **Does native ACL filtering authenticate people?** No. The application supplies verified identity.
4. **When are separate Knowledge Bases useful?** For a few stable access groups where isolated data and permissions simplify enforcement.
