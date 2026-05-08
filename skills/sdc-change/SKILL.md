---
name: sdc-change
description: "Create a focused requirement change under .sdc/changes/active with proposal, spec, design, tasks, and notes."
---

# Skill: SDC 需求变更创建 /sdc:change

## 触发条件
当用户输入以下任一内容时，自动触发本技能：
- `/sdc:change`
- "创建需求变更"
- "新建一次迭代"
- "开始一个 change"
- "记录这次需求"

## 核心使命
创建一次独立、可追踪、可验证的需求迭代。它吸收 OpenSpec 的核心 change 思路，但只保留 SDC 需要的最小闭环：为什么改、改什么、怎么做、怎么验收、最后如何归档。

---

## 标准输出/落盘结构

每次变更必须在 `.sdc/changes/active/` 下创建一个目录：

```text
.sdc/changes/active/YYYY-MM-DD-short-name/
├── proposal.md
├── tasks.md
├── design.md
├── spec.md
└── notes.md
```

## 文件职责

| 文件 | 作用 |
|------|------|
| `proposal.md` | 背景、目标、非目标、验收标准、风险 |
| `tasks.md` | 可执行任务清单，每项必须可验收 |
| `design.md` | 关键技术设计、数据变化、替代方案 |
| `spec.md` | 最终需求规范，完成后可沉淀到 `.sdc/specs/` |
| `notes.md` | 实现过程、问题、验证记录 |

---

## 执行规则

1. 如果 `.sdc/` 不存在，先执行 `/sdc:init`
2. short-name 必须简短、稳定，推荐英文小写和连字符
3. 一个 change 只表达一次独立需求迭代
4. 不要把多个互相独立的需求塞进同一个 change
5. 创建后必须给出下一步：`/sdc:spec` 或 `/sdc:validate`

---

## 输出格式

```text
✅ SDC 需求变更已创建
==================================================

## Change ID
YYYY-MM-DD-short-name

## 创建文件
- .sdc/changes/active/YYYY-MM-DD-short-name/proposal.md
- .sdc/changes/active/YYYY-MM-DD-short-name/tasks.md
- .sdc/changes/active/YYYY-MM-DD-short-name/design.md
- .sdc/changes/active/YYYY-MM-DD-short-name/spec.md
- .sdc/changes/active/YYYY-MM-DD-short-name/notes.md

## 下一步
👉 完善 proposal.md 和 spec.md，然后执行 `/sdc:validate`
```

---

## 质量红线

| 规则 | 违反后果 |
|------|---------|
| 必须创建独立 change 目录 | 变更不可追踪 |
| 必须包含 proposal/tasks/spec | 输出无效 |
| 不能覆盖已有 change | 数据丢失 |
| 必须有验收标准 | 无法验证 |
| 必须给出下一步 | 输出无效 |
