# Reflection Proposal Schema

Use a compact proposal that supports a decision and a later patch. Do not recount the full session.

```markdown
## Reflection proposal

### Outcome

<One sentence describing what the session completed.>

### Candidate improvements

| Lesson | Existing coverage | Route | Confidence |
|---|---|---|---|
| <durable lesson> | missing / partial / sufficient | local_project / public_empiricalops / no_change | high / medium / low |

### Proposed changes

#### <Route>: <component>

- Evidence: <specific correction, rework, or confirmed preference>
- Root cause: <missing rule, poor discovery, ambiguous default, or execution failure>
- Target: `<file, skill, template, or setup question>`
- Change: <minimal patch-level description>
- Scope rationale: <why this belongs here and not elsewhere>
- Privacy treatment: <none needed or what must be abstracted>
- Validation: <observable future behavior or deterministic check>

### No-change dispositions

- <Candidate>: <why no durable modification is warranted>

### Decision requested

<Ask which proposals, if any, the user wants implemented.>
```

## Confidence

- `high`: the user explicitly stated the preference or the workflow requirement is directly evidenced.
- `medium`: evidence is strong but the intended durability or scope has not been confirmed.
- `low`: plausible lesson inferred from one event; normally keep as `no_change` or request clarification.

## Root Cause Discipline

If an existing instruction already states the desired behavior, do not automatically propose another copy. Consider whether the real improvement is better routing, setup discovery, a validation gate, or no change.
