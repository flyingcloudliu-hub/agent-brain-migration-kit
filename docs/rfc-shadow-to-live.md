# RFC: Shadow-to-Live Brain Migration

## Problem

Some agents already have a working gateway and tool execution layer. They may receive messages from IM systems, webhooks, CLIs, or internal workflows. Replacing the whole system just to adopt a new brain runtime is risky.

The migration problem is:

- the gateway should remain stable
- existing tools should continue to execute side effects
- the candidate brain should be evaluated before it becomes live
- rollback should be a configuration change, not a rewrite

## Goals

- Decouple gateway, brain runtime, and action execution.
- Support `shadow`, `dry-run`, and `live` modes.
- Make action intent explicit and auditable.
- Provide a small migration path for already-running agents.

## Non-Goals

- Build a full agent framework.
- Replace existing IM integrations.
- Replace existing tool execution systems.
- Define one universal memory format.
- Include private deployment-specific patches.

## Proposed Architecture

```text
Gateway
  -> Brain Router
    -> Primary Brain
    -> Candidate Brain
  -> Action Intent Contract
  -> Executor Adapter
  -> External Tools
```

The gateway handles inbound and outbound transport. The router decides which brain handles the input. The brain produces a user reply and action intents. The executor decides whether and how to perform side effects.

## Modes

### shadow

The primary brain continues to serve users. The candidate brain receives the same input and returns a dry-run result. Its result is logged but does not trigger side effects.

### dry-run

Only validate candidate output shape, action schema, and context loading. No user-facing reply or side effects are produced.

### live

The candidate brain becomes the active brain. Side effects still go through the executor and action policy.

## Router Input

```json
{
  "message": {
    "role": "user",
    "text": "Please summarize this note and save it."
  },
  "context": {
    "channel": "im",
    "thread_id": "thread_123",
    "user_id": "user_123",
    "loaded_docs": []
  },
  "config": {
    "backend": "candidate",
    "mode": "shadow"
  }
}
```

## Brain Output

```json
{
  "reply": "I can stage this note for review before saving it.",
  "actions": [
    {
      "type": "knowledge_stage",
      "payload": {
        "title": "Note summary",
        "content": "..."
      },
      "confidence": 0.86
    }
  ],
  "meta": {
    "backend": "candidate",
    "mode": "shadow"
  }
}
```

## Shadow Log

A shadow log should record enough information to compare safety and compatibility without storing unnecessary private content.

```json
{
  "case_id": "case_001",
  "input_summary": "User asked to stage a note",
  "primary": {
    "reply_summary": "...",
    "actions": []
  },
  "candidate": {
    "reply_summary": "...",
    "actions": [
      {
        "type": "knowledge_stage"
      }
    ]
  },
  "judgement": {
    "task_understanding": "correct",
    "action_safety": "safe",
    "compatibility": "compatible",
    "rollout_recommendation": "observe"
  }
}
```

## Open Questions

- Should shadow logs be a runtime feature or an external adapter?
- Should action schemas live in the runtime, the executor, or a shared package?
- How much context loading should be standardized?
- What minimum examples would be useful for upstream documentation?

