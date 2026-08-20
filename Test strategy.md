\# Safety and Validation



\## Safety Model

Enforced structurally, not by disclaimer:

1\. Bounded input — only approved score-level fields accepted.

2\. Approved templates — all wording pre-written and neutral; no free generation.

3\. Output scan — forbidden phrases blocked before return.



\## Test Strategy

Automated `unittest` covers: determinism, audience fact-consistency, forbidden language, unknown-field rejection, version rejection, and audit-event PHI safety (6 tests, all passing).



\## Review Gates

Release only if it passes in order: validation → template rendering → output safety scan. Failing any gate stops the pipeline.



\## Evidence Before Expanding Capability

Before adding retrieval, personalization, predictive modeling, or LLM text:

clinical validation, fairness assessment, opt-in consent, and governance (approval, monitoring, rollback). The deterministic layer stays the permanent foundation.

