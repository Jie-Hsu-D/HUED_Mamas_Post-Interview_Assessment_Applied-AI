# Bounded Explanation Input Contract

The explanation layer receives only the following fields:

| Field | Type | Requirement |
|---|---|---|
| `score_version` | string | Must equal an explicitly supported version. |
| `explanation_version` | string | Version of the approved template set. |
| `tier` | enum | `T1`, `T2`, `T3`, or `T4`. |
| `score` | integer/null | Optional, 0–100 when present. |
| `contributors` | array | Ordered objects containing approved `domain`, `signal`, and `rank`. |
| `missing_domains` | array | Approved domain names only. |
| `case_id` | string | Synthetic trace identifier; not a person or profile identifier. |

Allowed contributor domains: `cycle_pattern`, `sleep`, `stress`, `physical_health`.

Allowed signals: `supportive`, `mixed`, `needs_attention`, `not_available`.

Unknown top-level fields, unknown domains, unknown signals, unsupported versions, invalid ranks, and invalid score values must not be silently accepted.

The audience is supplied separately and must be `patient` or `provider`. Audience changes language density and structure, not facts, tier meaning, uncertainty, or contributor ordering.

