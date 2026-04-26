# Long-Chain Troubleshooting

Brain migration failures often happen outside the brain itself. A useful checklist should inspect each layer from transport to side effects.

## Layers

1. Gateway receives the message.
2. Router builds normalized input.
3. Context loader loads expected documents.
4. Primary or candidate brain returns valid output.
5. Action contract validates.
6. Executor policy allows or blocks side effects.
7. External tool succeeds.
8. Gateway sends final reply.

## Minimal Checks

### Gateway

- Is the inbound message visible in logs?
- Does it have a trace id or message id?
- Is the correct user or thread mapped?

### Router

- Which backend is active?
- Which mode is active?
- Is fallback configured?
- Is the router input serializable?

### Context

- Which manifest was used?
- Which required docs were loaded?
- Were any docs truncated?
- Were secrets excluded?

### Brain

- Did the brain return JSON?
- Does the result contain `reply`, `actions`, and `meta`?
- Did it claim side effects in shadow mode?

### Action

- Are all action types allowlisted?
- Do payloads pass schema validation?
- Are high-impact actions gated?
- Were executor results recorded?

### Rollback

- Can active backend be changed by config?
- Can mode be changed back to `shadow`?
- Is the previous brain still available?

## Recommended Trace Fields

- `trace_id`
- `channel`
- `thread_id`
- `backend`
- `mode`
- `action_id`
- `executor_status`

