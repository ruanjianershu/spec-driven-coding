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

---

## 归档前置条件

归档前必须确认：
- `/sdc:validate <change-id>` 已通过
- `tasks.md` 中关键任务已完成
- `spec.md` 是最终版本
- 测试和质量结论已经记录在 `notes.md`、`reports/` 或 change 目录中

---

## 归档动作

必须执行：
1. 将 `.sdc/changes/active/<change-id>/spec.md` 沉淀到 `.sdc/specs/<change-id>.md`
2. 在 change 目录创建 `archive.md`
3. 记录归档时间、交付结论、验证结果
4. 将目录移动到 `.sdc/changes/archive/<change-id>/`

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
