\# Audit Schema



\## Event Fields (metadata only)

\- `case\_id` — synthetic trace id

\- `score\_version`, `explanation\_version` — versions used

\- `input\_sha256` — hash of the input, for traceability

\- `outcome` — e.g. `rendered`



\## Privacy Rationale

No raw inputs are stored — not `contributors`, `missing\_domains`, or `score`.

The input hash allows tracing "which input produced this" without retaining any

health data. `case\_id` is synthetic, not a person identifier.



\## Retention Questions (open)

\- How long are audit events retained, and who may access them?

\- Should the input hash be salted to prevent correlation across events?



\## Example Synthetic Event

```json

{

&#x20; "case\_id": "case\_4\_complete",

&#x20; "score\_version": "SYNTHETIC-1.0",

&#x20; "explanation version": "TEMPLATE-1.0",

&#x20; "input\_sha256": "3a7b...c9",

&#x20; "outcome": "rendered"

}

```

