"""Deterministic explanation layer for synthetic FRS inputs.



Render patient-facing and provider-facing explanations from the same 

approved score-level facts. Facts are audience-independent; audience 

only changes wording. No raw health information is added or inferred.

"""



import hashlib

import json



\# Part 1



\# allowed values: Sources from the Bounded Explanation Input Contract

ALLOWED\_FIELDS = {

&#x20;   "score\_version", "explanation\_version", "tier",

&#x20;   "score", "contributors", "missing\_domains", "case\_id"

}

ALLOWED\_TIERS = {"T1", "T2", "T3", "T4"}

SCORE\_MIN = 0

SCORE\_MAX = 100

ALLOWED\_CONTRIBUTOR\_DOMAINS = {"cycle\_pattern", "sleep", "stress", "physical\_health"}

ALLOWED\_SIGNALS = { "supportive", "mixed", "needs\_attention", "not\_available"}

SUPPORTED\_SCORE\_VERSION = {"SYNTHETIC-1.0"}

SUPPORTED\_EXPLANATION\_VERSION = {"TEMPLATE-1.0"}

ALLOWED\_AUDIENCES = {"patient", "provider"}



\#Neutral, non-advice phrasing per domain. No forbidden words appear here.

DOMAIN\_LABELS = {

&#x20;   "cycle\_pattern": "cycle pattern",

&#x20;   "sleep": "sleep", 

&#x20;   "stress": "stress",

&#x20;   "physical\_health": "physical health"

}

TIER\_MEANING = {

&#x20;   "T1": "a strongly supportive readiness pattern",

&#x20;   "T2": "a broadly supportive pattern with some areas to watch",

&#x20;   "T3": "a mixed pattern across several areas", 

&#x20;   "T4": "several areas flagged for attention"

}

SIGNAL\_LABELS = {

&#x20;   "supportive": "appeared supportive",

&#x20;   "mixed": "showed a mixed picture",

&#x20;   "needs\_attention": "showed less support", 

&#x20;   "not\_available": "had no data available"

}



\# Aligned with docs/SAFETY\_CONTRACT.md.

FORBIDDEN\_PHRASES = {

&#x20;   "you should", "we recommend", "consult", "seek care",

&#x20;   "treatment", "diagnosis", "will become pregnant", "caused by",

}



class ExplanationError(ValueError):

&#x20;   pass

