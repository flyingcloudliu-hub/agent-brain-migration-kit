# Hermes Issue Draft

Title:

```text
Docs proposal: shadow-to-live migration supplement for OpenClaw -> Hermes
```

Body:

```md
## Summary

This is a docs / migration supplement proposal for users coming from OpenClaw via `hermes claw migrate`, especially users who already have a working external gateway such as Feishu/Lark and an existing tool execution layer.

I am not proposing a full framework or a large implementation PR. I wanted to share a concrete migration pattern from a real OpenClaw -> Hermes setup where the existing gateway and tool executor were kept in place.

The public extraction is here:

https://github.com/flyingcloudliu-hub/agent-brain-migration-kit

## Background

The concrete scenario is:

- an OpenClaw gateway is already serving real messages
- Feishu/Lark or another IM entry point is already connected
- tool execution already exists outside the brain runtime
- project context, rules, tool docs, and current task state already live outside the runtime
- Hermes should first be tested in shadow mode
- live switching should be limited and reversible

The runtime itself worked, but the practical migration path was not obvious for an already-running agent.

## Problem this supplement tries to cover

For users who already have an OpenClaw-based agent in production or personal daily use, adopting Hermes is not only a runtime integration problem. It is also a migration problem:

1. How do we preserve the existing gateway?
2. How do we preserve existing tool executors?
3. How do we test Hermes in shadow mode before switching live traffic?
4. How do we avoid letting the brain directly perform side effects?
5. How do we keep identity, rules, tools, and current task state outside the runtime but still available to the brain?
6. How do we debug failures across gateway, router, brain, action contract, executor, and external tools?

## Proposed supplement shape

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
2. Would this be useful as a supplement to `hermes claw migrate`?
3. Does Hermes already have preferred concepts for shadow mode, action intent, or context manifests that this should align with?
4. Which part would be most valuable to contribute first?

My current guess is that the first contribution should be documentation and contracts, not a large implementation PR.

---

## 中文说明

这是一个面向 `hermes claw migrate` 的文档 / 迁移补充提案，尤其适合已经从 OpenClaw 接入了飞书/Lark，且已有外部工具执行层的用户。

我不是想提交一个完整框架或大型功能 PR。这个提案来自一次真实的 OpenClaw -> Hermes 迁移：保留已有 OpenClaw gateway 和工具执行层，只把 brain runtime 逐步切到 Hermes。

具体场景是：

- OpenClaw gateway 已经在线处理真实消息
- 飞书/Lark 或其他 IM 入口已经打通
- 工具写入、检索、同步等 side effects 已经由外部执行层处理
- 身份、规则、工具说明、当前任务状态等公共上下文已经在 runtime 外部维护
- Hermes 需要先以 shadow mode 跑同一批输入
- 通过基础检查后再有限切到 live
- 如果表现不稳定，可以快速回滚到旧 backend

我整理了一个独立的小仓库，用来沉淀这套通用方法和最小契约：

https://github.com/flyingcloudliu-hub/agent-brain-migration-kit

我希望确认这类迁移补充是否适合进入 Hermes 文档或 examples。如果适合，我倾向于先贡献文档、契约和最小示例，而不是直接提交大规模实现。
```
