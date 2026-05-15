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
把完成的需求迭代从 `.sdc/changes/active/<change-id>/` 沉淀为稳定项目资产，并移动到 `.sdc/changes/archive/<change-id>/`。它吸收 OpenSpec archive 的核心思想：变更完成后，临时提案要转化成长期规范。

归档不是搬文件，而是把临时变更提升为长期事实。归档后的 `.sdc/specs/<change-id>.md` 必须保留 `SCN-* / REQ-* / AC-*` 和最终验证证据。

---

## 归档前置条件

归档前必须确认：
- `/sdc:validate <change-id>` 已通过
- `/sdc:check <change-id>` 已通过，或有等价的 review/test/security/quality 证据
- `tasks.md` 中关键任务已完成
- `spec.md` 是最终版本
- `SCN-* -> REQ-* -> AC-* -> T### -> 验证证据` 追溯链完整，或明确记录未覆盖原因
- 测试和质量结论已经记录在 `notes.md`、`reports/` 或 change 目录中

---

## 反合理化表

| 偷懒借口 | 必须反驳 |
|---------|---------|
| “代码已经合了，可以归档” | 归档沉淀的是稳定规范，不是代码合并状态；必须有 check 证据 |
| “spec 差不多就行” | specs 是长期资产，模板内容或过期描述会污染后续需求 |
| “历史目录没用了，可以删掉” | change 历史是追溯资产，必须移动到 archive 而不是删除 |
| “任务没全勾也可以归档” | 未完成任务必须关闭、迁移到新 change，或记录明确理由 |

---

## 红旗警告

出现以下情况禁止归档：

- `spec.md` 仍是模板内容
- `tasks.md` 存在未完成关键任务
- spec/tasks/notes 无法形成追溯链
- 没有 `/sdc:check` 或等价检查记录
- 没有测试/质量结论
- `.sdc/specs/<change-id>.md` 已存在但用户没有明确允许覆盖

---

## 必须提供的证据

- change-id
- check 或等价检查记录位置
- 测试/质量结论位置
- 沉淀后的 `.sdc/specs/<change-id>.md`
- 移动后的 `.sdc/changes/archive/<change-id>/`
- `REQ/AC/T###` 最终覆盖摘要

---

## 归档动作

必须执行：
1. 将 `.sdc/changes/active/<change-id>/spec.md` 沉淀到 `.sdc/specs/<change-id>.md`
2. 在 change 目录创建 `archive.md`
3. 记录归档时间、交付结论、验证结果
4. 在 `archive.md` 中记录 `REQ/AC/T###` 覆盖摘要和遗留项
5. 将目录移动到 `.sdc/changes/archive/<change-id>/`

不要删除 change 目录。历史上下文是资产。

---

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
可以作为稳定规范继续引用。

## 下一步
👉 新需求执行 `/sdc:change <short-name>`
```

---

## 质量红线

| 规则 | 违反后果 |
|------|---------|
| 校验未通过不能归档 | 稳定规范污染 |
| 不能删除 change 目录 | 历史丢失 |
| 必须沉淀到 specs | 没有长期规范 |
| 必须记录归档结论 | 以后无法追溯 |
| 已存在 specs 文件不能静默覆盖 | 数据丢失 |
| 追溯链不完整不能归档为稳定规范 | 长期事实污染 |
