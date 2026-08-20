\# Decisions



\## Template vs. LLM

Chosen: deterministic templates, no LLM at this stage.

Reason: the task requires reproducible, explanation-only, bounded, auditable

output. LLMs are probabilistic (break reproducibility) and can hallucinate

(break explanation-only). Templates satisfy all four by construction.



\## Assumptions

\- The upstream score and contributions are already computed and correct.

\- `SYNTHETIC-1.0` / `TEMPLATE-1.0` are the only supported versions.

\- Signals may be surfaced descriptively (e.g. "showed less support") without

&#x20; becoming advice.



\## Tradeoffs

Templates are less fluent and less flexible than an LLM, but gain determinism,

safety, and auditability — the right priority for a clinical foundation.



\## Next Responsible Steps

\- If natural language is later needed, use an LLM only to polish approved

&#x20; template text, still passing the output safety scan.

