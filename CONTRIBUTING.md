# Contributing

This project is intentionally small. It is a public extraction of a real brain migration workflow, not a full agent platform.

## Good Contributions

Good contributions usually improve one of these areas:

- clearer migration docs
- better action intent schemas
- better shadow log schemas
- safer side-effect boundaries
- simpler examples
- troubleshooting checklists

## Out of Scope

The project does not aim to include:

- private deployment instructions
- credentials or account-specific logs
- full IM bot implementations
- full workflow orchestration
- deep adapters for private tools
- prompt or memory content from a specific personal agent

## Feedback Loop

Useful feedback may be applied in two places:

1. this public kit, if it improves the generic method
2. the original private agent setup, if it improves real-world stability

Changes should not flow the other way unless private details are removed first.

## Review Principles

- Prefer small docs or schema changes before large implementations.
- Keep examples neutral and runnable.
- Make side-effect behavior explicit.
- Avoid storing raw private content in examples or logs.
- Explain why a migration step is needed, not only how to run it.

