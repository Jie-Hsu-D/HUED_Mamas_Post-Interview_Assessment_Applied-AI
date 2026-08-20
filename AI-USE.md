\# AI Use



\- \*\*Tool:\*\* Claude (Anthropic).



\- \*\*Where and how used:\*\*

&#x20; - Explaining unfamiliar concepts (e.g. deterministic vs. LLM output,

&#x20;   hallucination, PHI, auditability) so I could reason about the design myself.

&#x20; - Reviewing my design for gaps and drafting the pipeline structure and the

&#x20;   documentation.

&#x20; - Explaining the code line by line so I understand every function.



\- \*\*Material outputs adopted:\*\* The overall pipeline structure (validate →

&#x20; build facts → render → safety scan → audit), the template/LLM decision, and

&#x20; first drafts of these documents — all reviewed and edited by me.



\- \*\*Verification performed:\*\*

&#x20; - Ran the full `unittest` suite and confirmed all tests pass.

&#x20; - Reviewed each function line by line to ensure I can explain and modify it

&#x20;   without the tool, in preparation for the live defense.

&#x20; - Checked every documented behavior against the actual code and the contracts.

