# 🔐 IAM, SSO, and API permissions

## 🪪 Identities and temporary access

| Term | Simple meaning |
| --- | --- |
| IAM user | An AWS identity that can have long-lived credentials |
| IAM role | Permissions assumed through a temporary session |
| IAM policy | Rules allowing or denying actions on resources |
| IAM Identity Center | Central workforce access, commonly called AWS SSO (single sign-on) |
| Permission set | Identity Center's template for permissions in an AWS account |

- **Concept:** engineers authenticate through Identity Center and receive temporary role credentials.
- **Analogy:** a time-limited employee pass replaces a permanent shared key.
- **AWS example:** an engineer configures an SSO CLI profile, signs in through the browser, and the CLI obtains temporary credentials for the assigned account/role. No commands are needed for this theory.
- **If misconfigured:** a permanent key or overpowered permission set gives longer-lived or excessive access.
- **Takeaway:** temporary credentials reduce persistent-key handling; they still need least privilege and session controls.

[AWS CLI SSO guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html)

## 🚪 API permission is not document permission

- **Concept:** IAM controls AWS operations; the app also needs rules for documents inside the result set.
- **Analogy:** entering the library is different from opening a confidential file.
- **AWS example:** both A and B may call the chatbot API. The application grants A general content and B general plus restricted content.
- **If misconfigured:** treating “logged in” as “may read everything” leaks restricted reports.
- **Takeaway:** authentication establishes identity; authorization limits its access.

| Identity | Intended role |
| --- | --- |
| Engineers A and B | Invoke the protected chatbot endpoint |
| Lambda execution role | Retrieve from approved Knowledge Bases and call the selected model |
| Knowledge Base service role | Read approved source data and access the configured store |
| Data administrator | Maintain document classifications and ingestion settings |

Lambda calls AWS using its own role. AWS does not automatically inherit the engineer's document permissions through that role.

## 🗄️ Separate Knowledge Bases

- **Concept:** split general and restricted documents into separately permissioned resources.
- **Analogy:** two library rooms with separate keys are easier to control than a mixed shelf.
- **AWS example:** scope `bedrock:Retrieve` to the general Knowledge Base ARN for a general-only role; grant restricted retrieval only to the appropriate backend role. ARN means AWS resource identifier.
- **If misconfigured:** broad Bedrock permissions, mixed source prefixes, or direct store access undo the separation.
- **Takeaway:** separate stores reduce filter dependence only when every access route is restricted.

**API caveat:** AWS's example scopes `Retrieve` to a Knowledge Base ARN but uses
`Resource: "*"` for `RetrieveAndGenerate`. Do not assume every operation supports the same resource scoping.
Our main design uses scoped `Retrieve` plus a separate model call; engineers do not receive direct Bedrock retrieval permissions.
[AWS retrieval permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-prereq-permissions-general.html)

## 🎤 Interview FAQ

1. **Why prefer SSO credentials?** They expire and avoid distributing permanent keys.
2. **Does a role identify every human uniquely?** No. Preserve a trusted user mapping; shared role membership alone may not distinguish A from B.
3. **Can IAM separate Knowledge Bases?** Yes for supported actions such as Retrieve; check each operation's resource support.
4. **Can IAM alone filter arbitrary documents in a shared index?** Not by automatically applying each user's S3 permissions.
