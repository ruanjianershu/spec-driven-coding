---
name: sdc-implement
description: "Use when a confirmed SDC change needs detailed implementation control beyond the normal apply workflow."
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

- Role contract: `../../sdc-references/role-contracts.md`, section `sdc-implement`.
- Apply rules: `../../sdc-references/workflow-standards.md` and `../../sdc-references/artifact-schemas.md`.
- Expert routing: `../../sdc-references/expert-routing.md`.
- Brownfield boundary: `../../sdc-references/legacy-impact-gate.md`.
- Execution orchestration: `../../sdc-references/execution-orchestration.md`.
- State recovery, revisions, and measured delivery evidence: `../../sdc-references/runtime-context.md`.

## 执行规则

1. 优先建议用户使用 `/sdc:apply`。
2. 必须有 confirmed spec、plan/design、tasks、context-pack，以及 Brownfield/Legacy 所需的 `impact.md`。
3. 确认 Global Constraints 完整且 Plan Preflight 为 Passed。
4. 按任务 brief 串行执行，优先测试，再最小实现；当前任务完成 review、持久证据和 runtime 账本更新前，不并行启动下一个实现任务。
5. 实现前读取 `.sdc/common-ground.md`、`.sdc/expert-routing.md`、`.sdc/knowledge/index.md`、相关知识文件和 `context-pack.md`。
6. 每个任务完成实现报告后，执行一次 Spec Compliance + Code Quality 双判定审查；通过后再更新任务状态、notes、验证证据和必要的 `knowledge-candidates.md`。
7. 所有任务完成后执行最终整体审查；遇到范围、契约、数据、安全、架构、知识冲突或影响边界问题，输出 Stop-Line Report。
8. 遵循 apply 的状态和快照门禁；实际验证使用内部 evidence runner，最终评审后绑定当前快照。过期、失败或仅口头声称通过的记录不能用于交付。按已确认风险缩放执行范围，不重复读取未变化资料或重问已有授权。

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

- 不能绕过 `/sdc:apply` 的治理、事实优先级、TDD、任务级审查、执行账本和停线规则。
- 不能“自己解决”需要用户确认的高影响决策。
- 不能跳过验证或不更新 SDC 记录。
- 不能把 memory candidate 当作 confirmed knowledge。
- 不能从 OPEN 或高影响 WORKING Common Ground 执行实现。
