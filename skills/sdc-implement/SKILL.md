---
name: sdc-implement
description: "Compatibility detailed command for implementation. Prefer sdc-apply in normal mode."
---

# Skill: SDC 自动开发 sdc-implement

> 兼容说明：普通模式请优先使用 `/sdc:apply`。`sdc-implement` 作为详细/兼容 skill 保留。

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `sdc-implement`
- "开始实现"
- "写代码"
- "开发"

## 核心使命

兼容旧版或详细指令入口。实际执行规则与 `/sdc:apply` 一致：按 confirmed artifacts 和 tasks 逐步实现，不做大范围自主改写。

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-implement`.
- Apply rules: `../sdc-shared/workflow-standards.md` and `../sdc-shared/artifact-schemas.md`.
- Brownfield boundary: `../sdc-shared/legacy-impact-gate.md`.

## 执行规则

1. 优先建议用户使用 `/sdc:apply`。
2. 必须有 confirmed spec、plan/design、tasks、context-pack，以及 Brownfield/Legacy 所需的 `impact.md`。
3. 按任务顺序执行，优先测试，再最小实现。
4. 实现前读取 `.sdc/knowledge/index.md`、相关知识文件和 `context-pack.md`。
5. 每完成一个任务，更新任务状态、notes、验证证据和必要的 `knowledge-candidates.md`。
6. 遇到范围、契约、数据、安全、架构、知识冲突或影响边界问题，输出 Stop-Line Report。

## 输出格式

```text
🚀 SDC Implement
==================================================

## 兼容提示
普通模式建议改用 `/sdc:apply`

## 当前任务
- ...

## 修改文件
- ...

## 验证结果
- ...

## 下一步
👉 ...
```

## 质量红线

- 不能绕过 `/sdc:apply` 的治理、事实优先级、TDD、停线规则。
- 不能“自己解决”需要用户确认的高影响决策。
- 不能跳过验证或不更新 SDC 记录。
- 不能把 memory candidate 当作 confirmed knowledge。
