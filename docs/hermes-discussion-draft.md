# Hermes Discussion Draft

Title:

```text
Proposal: Shadow-to-live migration path for existing agent gateways
```

Body:

```md
## Background

I recently migrated a long-running personal agent from an OpenClaw-based setup to Hermes while keeping the existing gateway and tool execution layer.

The concrete example is: keep the OpenClaw gateway and existing tool executor, switch the brain runtime to Hermes, run Hermes in shadow mode first, then move it to live mode after basic checks.

The runtime itself worked, but the practical migration path was not obvious for an already-running agent:

- the IM / webhook / CLI gateway already exists
- the tool execution layer already exists
- context documents and current task state already exist outside the runtime
- the new brain should be tested before becoming live
- rollback should be simple

I extracted the generic parts of that migration into a small public repository:

https://github.com/flyingcloudliu-hub/agent-brain-migration-kit

## Problem

For users who already have an agent in production or personal daily use, adopting Hermes is not only a runtime integration problem. It is also a migration problem:

1. How do we preserve the existing gateway?
2. How do we preserve existing tool executors?
3. How do we test Hermes in shadow mode before switching live traffic?
4. How do we avoid letting the brain directly perform side effects?
5. How do we keep identity, rules, tools, and current task state outside the runtime but still available to the brain?
6. How do we debug failures across gateway, router, brain, action contract, executor, and external tools?

## Proposed Shape

I am proposing a lightweight migration pattern rather than a full framework:

- `brain-router`: normalizes input and routes to primary or candidate brain
- `shadow-to-live flow`: run candidate brain in shadow mode, then switch to live after checks
- `action-contract`: brain returns action intents; executor owns side effects
- `context-manifest`: declare which public/project context documents the brain may load
- `troubleshooting checklist`: debug long-chain migration failures layer by layer

## Non-Goals

This proposal does not try to define:

- a full agent platform
- a full IM bot framework
- private tool adapters
- a universal memory system
- deployment-specific patches

## Questions for Hermes maintainers

1. Is this migration pattern within the scope of Hermes documentation or examples?
2. Would this be more useful as a migration guide, an RFC/design note, schemas, or a small example?
3. Does Hermes already have preferred concepts for shadow mode, action intent, or context manifests that this should align with?
4. Which part would be most valuable to contribute first?

My current guess is that the first contribution should be documentation and contracts, not a large implementation PR.
```
