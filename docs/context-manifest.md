# Context Manifest

A context manifest declares which public or project-level documents a brain may load.

The goal is to keep identity, rules, tool descriptions, and current task state outside the brain runtime while preserving continuity during migration.

## Example

```json
{
  "max_total_chars": 24000,
  "docs": [
    {
      "path": "context/identity.md",
      "priority": "P0",
      "max_chars": 4000,
      "required": true
    },
    {
      "path": "context/tools.md",
      "priority": "P0",
      "max_chars": 6000,
      "required": true
    },
    {
      "path": "context/session-brief.md",
      "priority": "P1",
      "max_chars": 4000,
      "required": false
    }
  ]
}
```

## Loading Rules

- Load P0 documents first.
- Missing required documents should fail fast.
- Missing optional documents should be recorded but should not block.
- Apply per-document and total character limits.
- Avoid loading secrets or raw private logs.

## Suggested Document Types

- identity
- user or project preferences
- tool descriptions
- action contract
- current task state
- session brief
- migration notes

