---
name: sdc-archive
description: "Archive a completed SDC change, preserve history, and promote final spec into .sdc/specs."
---

# Skill: SDC 需求归档 /sdc:archive

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `/sdc:archive`
- "归档这个需求"
- "完成这个 change"
- "沉淀到 specs"
- "结束这次迭代"

## 核心使命

把完成的需求迭代从 `.sdc/changes/active/<change-id>/` 沉淀为稳定项目资产，并移动到 `.sdc/changes/archive/<change-id>/`。

归档后的 `.sdc/specs/<change-id>.md` 必须保留 SCN/REQ/AC 和最终验证证据。

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-archive`.
- Archive schema: `../sdc-shared/artifact-schemas.md`.
- Archive gate: `../sdc-shared/delivery-gates.md`.
- Traceability and evidence rules: `../sdc-shared/workflow-standards.md`.

## 归档前置条件

必须确认：

- `/sdc:validate` 已通过或有等价证据。
- `/sdc:check` 已通过或有等价 review/test/security/quality 证据。
- 关键 tasks 已完成。
- `spec.md` 是最终 confirmed 版本。
- SCN/REQ/AC/T###/验证证据可追溯。
- 测试和质量结论记录在 `notes.md`、`reports/` 或 change 目录中。

## 归档动作

1. 将 active change 的最终 `spec.md` 复制或提升为 `.sdc/specs/<change-id>.md`。
2. 在 change 目录创建 `archive.md`。
3. 记录归档时间、交付结论、验证结果、残余风险。
4. 记录 REQ/AC/T### 覆盖摘要和遗留项。
5. 将目录移动到 `.sdc/changes/archive/<change-id>/`。

不要删除 change 目录。历史上下文是资产。

## 输出格式

```text
✅ SDC 需求迭代已归档
==================================================

## Change
<change-id>

## 沉淀文件
- .sdc/specs/<change-id>.md
- .sdc/changes/archive/<change-id>/archive.md

## 归档结论
- ...

## 下一步
👉 新需求执行 `/sdc:change <short-name>`
```

## 质量红线

- 校验未通过不能归档。
- 不能删除 change 历史。
- 不能静默覆盖已有 specs 文件。
- 追溯链不完整不能归档为稳定规范。
- 未完成任务必须关闭、迁移到新 change，或记录明确理由。
