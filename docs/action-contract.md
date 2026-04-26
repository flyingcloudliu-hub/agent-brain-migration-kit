# Action Intent Contract

The action intent contract separates what the brain wants to do from what the executor actually does.

The brain should not directly perform side effects. It should return an intent. The executor validates and performs the action based on local policy.

## Brain Result

```json
{
  "reply": "I will stage this note for review.",
  "actions": [
    {
      "type": "knowledge_stage",
      "payload": {
        "title": "Example note",
        "content": "Example content"
      },
      "confidence": 0.86
    }
  ],
  "meta": {
    "backend": "hermes",
    "mode": "live"
  }
}
```

## Fields

### reply

User-facing natural language response. In `shadow` or `dry-run` mode, this should not claim that a side effect has already happened.

### actions

List of action intents. Each action should include:

- `type`: stable action name
- `payload`: structured input for the executor
- `confidence`: optional model confidence or routing confidence

### meta

Runtime metadata. Suggested fields:

- `backend`
- `mode`
- `model`
- `trace_id`

## Recommended Action Types

Use neutral action names in public examples:

- `knowledge_stage`
- `record_create`
- `record_update`
- `webhook_call`
- `research_request`
- `progress_update`

Avoid names tied to a private deployment.

## Executor Result

```json
{
  "action_id": "act_001",
  "type": "record_create",
  "status": "success",
  "artifact": {
    "type": "record",
    "id": "rec_123",
    "url": "https://example.com/records/rec_123"
  },
  "summary": "Created one record.",
  "error": null
}
```

## Policy Recommendations

- Maintain an action allowlist.
- Validate payloads before execution.
- Treat `shadow` and `dry-run` as no-side-effect modes.
- Require confirmation for high-impact actions.
- Log executor results with a trace id.

