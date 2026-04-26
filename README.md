# Agent Brain Migration Kit

Utilities and design notes for migrating an existing long-running agent to a new brain runtime without replacing its gateway or tool execution layer.

## 中文说明

这个项目来自一次真实的个人 Agent 迁移：我已经有一个长期运行的 Agent，有自己的 IM 入口、工具执行层、文档/任务上下文和回滚方式。迁移到 Hermes 这类新 brain runtime 时，我发现官方文档更偏 runtime 本身，对“已有系统如何平滑换脑”这类场景说明不够具体。

所以这个仓库沉淀的是一套通用方法，而不是我的私人部署：

- 保留现有入口，例如 IM、webhook、CLI
- 保留现有工具执行层
- 通过 brain router 切换或旁路验证新 brain
- 用 shadow mode 先观察候选 brain 的输出
- 用 action contract 把“动作意图”和“真实执行”分开
- 用 context manifest 外置身份、规则、工具说明和当前任务状态
- 保留简单明确的回滚路径

这个项目的目标是帮助类似场景的人少踩坑，也方便把成熟部分反馈给 Hermes 社区。它不是一个完整 Agent 平台，也不包含任何私人提示词、记忆、日志、账号、路径或工具配置。

## English Summary

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
