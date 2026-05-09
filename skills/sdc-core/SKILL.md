---
name: sdc
description: "SDC main entry. Route natural language requests across init, change, plan, apply, check, archive, and harness for spec-driven coding."
---

# Skill: SDC 主入口 sdc

## 触发条件
当用户输入以下任一内容时，自动触发本技能：
- `sdc`
- `sdc 初始化`
- `sdc 新需求`
- `sdc 开始实现`
- `sdc 检查`
- `sdc 完成`
- "用 SDC 做"

## 核心使命
提供一个统一、简单的 SDC 入口。用户不需要记住所有细分命令，只要描述当前想做什么，本技能负责路由到合适的 SDC 阶段。

SDC 的设计目标是整合和简化：
- OpenSpec 的核心：change、validate、archive
- Superpowers 的核心：轻量 skill-pack 和命令触发
- SDC 自己的核心：spec、plan、implement、review、test、quality、harness

但用户界面只保留一个主入口：`sdc`。

---

## 路由规则

| 用户意图 | 应执行的 SDC 能力 |
|---------|------------------|
| 初始化、第一次使用、建立目录 | `sdc:init` |
| 新需求、新功能、需求变更 | `sdc:change` + `sdc:spec` + `sdc:plan` |
| 开始写代码、执行计划 | `sdc:apply` |
| 检查、验收、能不能交付 | `sdc:validate` + `sdc:review` + `sdc:test` + `sdc:quality` |
| 完成、归档、沉淀规范 | `sdc:archive` |
| 记录项目规则、避免重复踩坑 | `sdc:harness` |

---

## 推荐用户用法

```text
sdc 初始化
sdc 新需求：支持用户登录
sdc:apply
sdc 检查
sdc 完成
```

---

## 执行原则

1. 优先自动判断阶段，不要求用户记细分命令
2. 如果 `.sdc/` 不存在，先建议或执行初始化
3. 新需求必须进入 `.sdc/changes/` 或 `.sdc/current/`
4. apply 前必须有 spec、design 和 tasks
5. 完成前必须 validate/check 通过
6. 归档时必须沉淀到 `.sdc/specs/`

---

## 输出格式

```text
🔧 SDC
==================================================

## 识别到的阶段
初始化 / 新需求 / 实现 / 检查 / 完成 / 规则沉淀

## 我会执行
- ...

## 当前结果
- ...

## 下一步
👉 ...
```

---

## 质量红线

| 规则 | 违反后果 |
|------|---------|
| 不能要求用户记住所有细分命令 | 违背 SDC 初衷 |
| 不能跳过需求记录直接实现 | 流程失效 |
| 不能绕过校验直接归档 | 规范污染 |
| 必须给出下一步 | 用户不知道怎么继续 |
