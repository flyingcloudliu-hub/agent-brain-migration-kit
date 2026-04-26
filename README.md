# Agent Brain Migration Kit

Utilities and design notes for migrating an existing long-running agent to a new brain runtime without replacing its gateway or tool execution layer.

This project started from a real migration where an existing agent gateway and tool layer needed to adopt Hermes as the brain runtime. The official docs covered the runtime itself, but the practical migration path for an already-running agent was less clear:

- keep the current IM / webhook / CLI gateway
- keep the existing tool execution layer
- route the same input to a candidate brain in shadow mode
- move to live mode only after basic safety checks
- keep rollback simple

The goal is to share the generic method and minimal contracts, not the private deployment details of that migration.

## Scope

This project covers:

- brain router contracts
- shadow-to-live migration flow
- action intent contract
- context manifest convention
- long-chain troubleshooting checklist
- small neutral examples

This project does not cover:

- a full agent platform
- a full IM bot framework
- customer delivery
- private tool integrations
- private prompts, memories, logs, credentials, or deployment paths

## Repository Layout

```text
docs/
  rfc-shadow-to-live.md
  action-contract.md
  context-manifest.md
  troubleshooting.md
  feedback-loop.md
examples/
  manifest-driven-router/
    manifest.example.json
    router.py
    sample-input.json
```

## Core Idea

```text
Existing gateway
  -> brain router
    -> primary brain
    -> candidate brain in shadow mode
  -> action intent contract
  -> existing executor
```

The router owns brain selection. The brain returns intent. The executor owns side effects.

## Suggested Migration Flow

1. Document the current gateway, executor, and rollback path.
2. Define the action intent contract before enabling side effects.
3. Run the candidate brain in shadow mode.
4. Compare primary and candidate outputs.
5. Switch a limited path to live mode.
6. Keep the old brain as fallback until the new path is stable.

## First Public Contribution Shape

If contributing this idea upstream to Hermes or another runtime, start with:

- an RFC / discussion
- a migration guide
- action and shadow log schemas
- a minimal router example

Avoid sending a large implementation PR before the maintainers agree the shape fits the project.
