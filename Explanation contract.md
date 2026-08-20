\# Explanation Contract



\## Accepted Inputs

Top-level fields only (anything else is rejected):

\- `score\_version` (string, must be `SYNTHETIC-1.0`)

\- `explanation\_version` (string, must be `TEMPLATE-1.0`)

\- `tier` (`T1`–`T4`)

\- `score` (int 0–100 or null)

\- `contributors` (array of `{domain, signal, rank}`)

\- `missing\_domains` (array of approved domains)

\- `case\_id` (synthetic id, not a person id)



Allowed domains: `cycle\_pattern, sleep, stress, physical\_health`.

Allowed signals: `supportive, mixed, needs\_attention, not\_available`.

Audience: `patient` or `provider` (supplied separately).



\## Normalized Representation

Validated input reduces to an audience-independent `facts`:

`tier`, `ordered\_domains` (sorted by rank), `domain\_signals`, `missing\_domains`.



\## Outputs

`render\_explanation(payload, audience)` returns:

`facts` (identical across audiences), `explanation` (audience-specific text from approved templates), `audit\_event` (metadata only).



\## Forbidden Behaviors

No diagnosis, advice, recommendation, prediction, causal claim, invented evidence, or facts absent from input. Enforced by templates + output scan, not a disclaimer.



\## Versioning

`score\_version` and `explanation\_version` are allow-listed and recorded in every audit event, enabling reproducibility.



\## Failure Behavior

Invalid input raises `ExplanationError` before any output is generated. Fails closed — never emits partial or best-guess output.

