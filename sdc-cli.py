#!/usr/bin/env python3
"""
SDC CLI - 规范驱动开发 薄运行层
功能：自动管理 SDC 项目文档，不用手动复制粘贴

用法：
  sdc init          # 初始化标准 SDC 工作区
  sdc init --standards <path> # 初始化并导入公司/团队规范包到 .sdc/standards/company/
  sdc standards import <path> # 导入公司/团队规范包
  sdc change <name> # 提出 intake 问题，不写 change 文件
  sdc change <name> --confirmed-intake # intake 确认后创建 Discovery Open 草稿
  sdc validate [target] # 校验 current 或某个 change
  sdc archive <change> # 归档完成的需求迭代，并输出 Knowledge Compact Gate
  sdc spec          # 打开规范文档（你在 AI 助手中写完粘贴进来）
  sdc discovery     # 打开需求探索文档
  sdc plan          # 打开计划文档
  sdc tasks         # 打开任务文档
  sdc apply         # 执行/记录当前需求迭代
  sdc implement     # apply 的兼容别名
  sdc check [target] # 综合检查 current 或某个 change
  sdc review        # 打开审查报告
  sdc test          # 打开测试报告
  sdc quality       # 打开质量检查报告
  sdc harness       # 生成/编辑 AGENTS.md 项目级 AI 规则
  sdc status        # 查看项目进度
"""

import os
import re
import shutil
import sys
import subprocess
from datetime import date, datetime
from pathlib import Path

SDC_DIR = Path(".sdc")
FILES = {
    "discovery": "current/discovery.md",
    "spec": "current/spec.md",
    "plan": "current/plan.md",
    "tasks": "current/tasks.md",
    "apply": "current/apply.md",
    "implement": "current/apply.md",
    "review": "reviews/current-review.md",
    "test": "reports/current-test.md",
    "quality": "reports/current-quality.md",
    "harness": "harness.md",
}

DIRS = [
    "changes",
    "changes/active",
    "changes/archive",
    "current",
    "decisions",
    "knowledge",
    "knowledge/product",
    "knowledge/technical",
    "memory",
    "memory/episodic",
    "reports",
    "reports/bug",
    "reports/impact",
    "reports/repo-analysis",
    "reviews",
    "specs",
    "standards",
    "standards/company",
    "templates",
]

STANDARD_PACK_MARKER = "<!-- SDC-MANAGED-STANDARDS-PACK -->"
STANDARD_PACK_DOC_SUFFIXES = {".md", ".markdown", ".txt", ".rst", ".adoc", ".yaml", ".yml", ".json"}
STANDARD_PACK_IGNORED_NAMES = {
    ".DS_Store",
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "target",
    "coverage",
}

INIT_FILES = {
    "README.md": """# SDC Workspace

这个目录记录项目的规范驱动开发过程。所有需求、计划、实现记录、审查、测试和质量检查都应该沉淀在这里。

## 目录

- `project.md` - 项目长期背景、目标用户、技术约束和验证命令
- `project-cognition.md` - 遗留项目整体认知，基于代码证据建立维护地图
- `constitution.md` - 项目最高工程裁决规则
- `knowledge/` - 项目确认知识库，分为产品知识和技术知识
- `memory/` - 项目记忆与候选知识，默认不高于 confirmed knowledge
- `current/` - 当前正在推进的一次需求迭代，包含 discovery/spec/plan/tasks/apply
- `changes/active/` - 正在推进的需求变更，每个变更一个子目录
- `changes/archive/` - 已完成归档的需求变更
- `specs/` - 已稳定的业务规范和能力说明
- `standards/` - 项目长期开发规范，约束人和 AI 怎么写代码
- `decisions/` - 架构决策记录
- `reviews/` - 代码审查记录
- `reports/` - 测试、质量、bug、impact、repo-analysis 和交付报告
- `templates/` - discovery、需求迭代、项目认知、影响面、停线和分析模板

## 推荐流程

1. `/sdc:change <name>` 创建 `changes/active/<name>/` 的轻量 Discovery Open 草稿
2. 需求不确定时只更新 `discovery.md`、Draft `proposal.md` 和简短 `notes.md`
3. 需求确认后读取 `knowledge/index.md` 和相关产品/技术知识，再生成 spec
4. `sdc-spec` 将已确认 discovery 收敛为 SCN/REQ/AC
5. 遗留项目在需求确认后先更新当前 change 的 `impact.md`
6. `/sdc:plan` 生成 design/tasks/context-pack
7. `/sdc:apply` 执行实现，记录验证证据和 `knowledge-candidates.md`
8. `/sdc:check` 综合校验、审查、测试、质量和知识漂移
9. `/sdc:archive <name>` 归档到 `changes/archive/`，并运行 Knowledge Compact Gate 判断长期知识沉淀

## 三类核心资产

- `specs/` - 业务规范：项目应该做什么
- `changes/` - 需求迭代：这次为什么改、怎么改、如何验收
- `knowledge/` - 项目知识：产品事实、业务规则、技术事实和运行方式
- `standards/` - 开发规范：代码、测试、架构、安全、Git 和 AI 协作规则
- `standards/company/` - 可选公司/团队规范包，通过索引按需读取
- `memory/` - 项目记忆：候选知识、经验、流程和可回顾的工作片段

## SDC v1.2 纪律内核

```text
治理优先级：.sdc/constitution.md > AGENTS.md > 对话即时要求
事实优先级：discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code
追溯链：SCN-* -> REQ-* -> AC-* -> T### -> 验证证据
确认门禁：高影响决策必须 Confirmed，不能 Silent Default
探索门禁：不确定需求必须先 discovery，再 spec
知识门禁：change/plan/apply 前读取 knowledge index；memory 只能辅助召回，不能覆盖 confirmed knowledge
```
""",
    "constitution.md": """# SDC Project Constitution

## 1. Governance Priority

`.sdc/constitution.md > AGENTS.md > conversation instructions`

If these sources conflict, stop and produce a Stop-Line Report.

## 2. Fact Priority

`discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code`

Code is evidence of current behavior, but it does not automatically override the agreed spec.

## 3. Knowledge and Memory Discipline

`.sdc/knowledge/` stores confirmed project knowledge. It is the shared project brain for product facts, domain rules, technical architecture, interfaces, operations, and validation commands.

`.sdc/memory/` stores project memory and knowledge candidates. Memory is useful for recall and continuity, but it cannot override confirmed knowledge, current specs, user confirmation, or code evidence.

Before writing a final spec, plan, task list, or implementation, read `.sdc/knowledge/index.md` and the relevant product/technical knowledge files. If the current change contradicts existing knowledge, record the conflict in the Decision Ledger and stop until it is confirmed.

No Evidence, No Fact. No Confirmation, No Execution. No Impact, No Brownfield Change.

Every durable knowledge item must record Status, Source, Verified At, Verified Against, and Scope. Missing evidence creates a Knowledge Gap; it does not authorize guessing.

Assumptions may be recorded only in discovery, Decision Ledger, or knowledge-candidates. `Assumed`, `Proposed`, `TBD`, `Conflict`, `Stale`, and open Knowledge Gaps must not drive final spec, design, context-pack, tasks, impact, apply, or archive.

For Brownfield/Legacy technical knowledge, code/config/test/build/runtime evidence is required. README files, comments, old docs, and memory are clues only.

## 4. Core Chain

`discovery -> spec -> impact -> plan -> tasks -> code -> verify -> archive`

## 5. Stop-The-Line Rules

Stop and produce a Stop-Line Report when:

- spec, design, or tasks are missing, conflicting, or not verifiable
- implementation requires changing business behavior, public contract, acceptance criteria, or key technical decisions
- current task requires scope expansion
- validation cannot prove the acceptance criteria
- required knowledge sources are missing, stale, or contradict the current change
- final artifacts contain unclosed Knowledge Gaps or unconfirmed assumptions

## 6. Traceability Rules

- specs must define `SCN-*`, `REQ-*`, and `AC-*` identifiers
- tasks must reference `REQ-*` and `AC-*`
- tests or validation notes must reference `AC-*`
- implementation notes must record validation evidence
- specs, designs, plans, and context packs must list the knowledge sources they used

## 7. Human Confirmation Rules

AI may propose options, but humans own high-impact decisions.

High-impact decisions include product rules, permissions, state machines, approval flows, reminder behavior, technology stack, architecture, data model, authentication, locking, deletion, migration, rollout, and security policy.

Before a high-impact decision enters `REQ-*`, `AC-*`, `INV-*`, `design.md`, or `tasks.md`, it must be one of:

- explicitly confirmed by the user
- supported by an authoritative project document
- explicitly delegated by the user with permission to choose

## 8. No Silent Defaults

Do not turn common practice into project truth.

All AI-created defaults must be recorded in a Decision Ledger as `Proposed` or `Assumed` until confirmed. `Proposed`, `Assumed`, `TBD`, and `Conflict` items must not be treated as implementation-ready.

## 9. Discovery Gate

When requirements are uncertain, start with discovery instead of a confirmed spec.

Discovery must record current understanding, candidate directions, tradeoffs, recommended MVP, open questions, and a Decision Ledger. A confirmed spec can only be produced after the current MVP scope and high-impact decisions are confirmed or explicitly deferred.

While Discovery Gate is open, keep artifacts minimal: `discovery.md`, optional Draft `proposal.md`, and brief `notes.md` only. Do not create or update `spec.md`, `design.md`, `tasks.md`, or `impact.md` until the MVP, acceptance direction, and high-impact decisions are confirmed or explicitly deferred.

Interpretation summaries are not consent. Do not write files with "if wrong, tell me" or "如有偏差请告知，我先改". Mark the interpretation as `Proposed` or `Assumed`, ask for explicit yes/no or option confirmation, wait for the user, then write durable artifacts.
""",
    "project.md": """# Project Context

## 项目目标

（这个项目长期要解决什么问题？）

## 目标用户

（谁会使用它？核心使用场景是什么？）

## 技术栈

（语言、框架、构建工具、运行环境）

## 约束条件

（性能、安全、兼容性、部署、合规等限制）

## 验证命令

| 操作 | 命令 |
|------|------|
| 安装依赖 | |
| 运行测试 | |
| 构建 | |
| 本地启动 | |

## AI 工作规则

（项目级偏好、禁忌、容易踩坑的地方）

## 知识库入口

- 产品知识索引：`knowledge/product/`
- 技术知识索引：`knowledge/technical/`
- 当前工作状态：`knowledge/current.md`
- 候选知识与项目记忆：`memory/`
""",
    "project-cognition.md": """# Project Cognition

> 遗留项目整体认知。新项目可以暂时保留为空；存量/遗留项目建议通过 `/sdc:check repo` 基于代码证据补全。

## 0. 分析快照

- 目标仓库/目录：
- 分析时间：
- 分支 / Commit / 子模块状态：
- 技术生态线索：
- 可见配置与依赖范围：
- 本次分析限制：

## 1. 一句话概述

## 2. 系统形态与技术栈

## 3. 核心数据模型与 Schema/DDL

## 4. 关键入口与启动方式

## 5. 目录结构与模块地图

## 6. 核心链路与数据流

## 7. 配置、数据存储与外部集成

## 8. 可观测性与运行诊断线索

## 9. 测试、构建与交付现状

## 10. 已确认风险与复杂区域

## 11. 待确认问题

## 12. 建议阅读顺序

## 13. 证据索引
""",
    "current/spec.md": """# Current Spec

> 当前需求规范。由 `sdc-spec` 生成或维护。

## 0. 文档元信息

- Status: Draft
- Schema: SDC 1.2.0
- Source:

## 1. Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|--------|--------|----------|----------------|

## 1.1 Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|--------|-------------------|----------------|--------|-----------|--------|

## 2. Decision Ledger / 决策台账

| ID | 决策 | 状态 | 依据来源 | 是否允许进入 REQ/AC | 下一步 |
|----|------|------|----------|----------------------|--------|

## 3. Glossary / 统一语言

## 4. 背景与目标

## 5. Business Invariants / 业务不变量

### INV-01

## 6. 场景与需求

### SCN-01

### REQ-01

## 7. Acceptance Criteria / 验收标准

### AC-01

Given ...
When ...
Then ...

## 8. 验证策略

## 9. 风险、假设与待确认项

## 10. 追溯关系矩阵
""",
    "current/discovery.md": """# Current Discovery

> 需求不确定时先在这里探索。Discovery 不是正式 spec，只有 Confirmed 决策才能进入 REQ/AC。
> Open Questions 未闭合时，只维护 discovery、可选 Draft proposal 和简短 notes，不生成完整 spec/design/tasks。

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|--------|--------|----------|----------------|

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|--------|-------------------|----------------|--------|-----------|--------|

## Current Understanding

## Candidate Directions

| Option | Description | Pros | Cons | Status |
|--------|-------------|------|------|--------|

## Tradeoffs

## Recommended MVP

## Decision Ledger

| ID | Decision | Status | Source | Impact | Next Step |
|----|----------|--------|--------|--------|-----------|

## Open Questions

| ID | Question | Why It Matters | Options | Required Before |
|----|----------|----------------|---------|-----------------|

## Exit Criteria

- [ ] MVP scope confirmed
- [ ] high-impact decisions confirmed or explicitly deferred
- [ ] acceptance direction is clear
""",
    "current/plan.md": """# Current Plan

> 当前实现计划。由 `/sdc:plan` 生成或维护。

## 设计摘要

## 影响范围

## 依赖关系

## 测试先行策略

## 交付清单
""",
    "current/tasks.md": """# Current Tasks

> 当前任务清单。任务必须能追溯到 REQ/AC。

## Tasks

- [ ] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] Draft task
  - Depends on: none
  - Verify: TODO
  - Source: current/spec.md#AC-01
""",
    "current/apply.md": """# Current Apply Log

> 当前执行记录。由 `/sdc:apply` 持续更新。

## 已完成任务

## 修改文件

## 测试结果

## 遇到的问题
""",
    "current/context-pack.md": """# Current Context Pack

> 给执行 Agent 的短交接包。只包含本轮需求落地必须知道的知识，不复制整个知识库。

## Goal

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|--------|--------|----------|----------------|

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|--------|-------------------|----------------|--------|-----------|--------|

## Confirmed Product Knowledge

## Confirmed Technical Knowledge

## Execution Boundaries

## Forbidden Assumptions

## Validation Commands

## Knowledge Candidate Routing

- Product knowledge candidates:
- Technical knowledge candidates:
- Memory/procedure candidates:
""",
    "current/knowledge-candidates.md": """# Current Knowledge Candidates

> apply/check/archive 阶段记录候选知识。候选知识不是事实，archive 时确认后才能写入长期知识库。

| Candidate | Type | Scope | Source | Status | Target | Evidence Needed | Promotion Gate |
|-----------|------|-------|--------|--------|--------|-----------------|----------------|
""",
    "changes/README.md": """# Changes

每一次需求迭代一个目录，放在 `active/` 下，推荐命名：

```text
active/YYYY-MM-DD-short-name/
```

每个迭代目录建议包含：

- `proposal.md` - 这次为什么要改、改什么、不改什么
- `discovery.md` - 需求不确定时的探索、候选方向、MVP、问题和决策台账
- `impact.md` - 遗留项目在需求确认后的变更影响面分析
- `tasks.md` - 可执行任务清单
- `design.md` - 关键设计和技术取舍
- `spec.md` - 最终沉淀的需求规范
- `context-pack.md` - 给执行 Agent 的短交接包，引用本次所需知识
- `knowledge-candidates.md` - apply/check 过程中发现的候选知识
- `notes.md` - 实现过程记录和问题

归档后移动到：

```text
archive/YYYY-MM-DD-short-name/
```

归档时会执行 Knowledge Compact Gate：

- `specs/` 和 `changes/archive/` 是必需归档资产
- `decisions/`、`standards/`、`AGENTS.md`、`reports/`、`project.md`、`project-cognition.md` 是条件性长期知识更新
- `knowledge/product/`、`knowledge/technical/` 和 `memory/` 是条件性知识/记忆更新
- 条件项需要明确确认后再写入，不能由 AI 或 CLI 静默更新
""",
    "specs/README.md": """# Specs

这里存放已经稳定下来的业务规范。不要把临时讨论直接放进来，先在 `current/` 或 `changes/` 中完成迭代。
""",
    "knowledge/README.md": """# Knowledge Base

这里存放项目长期知识。它不是聊天记录，也不是所有文档的合集，而是人和 AI 都要复用的项目事实。

## 分层

- `index.md` - 短索引。每次 change/plan/apply 前优先读取。
- `product/` - 产品知识：目标用户、领域概念、业务规则、流程和产品决策。
- `technical/` - 技术知识：技术栈、架构、模块、数据/接口、运行、测试和部署。
- `current.md` - 当前项目状态、最近变化和需要下一次接续的上下文。

## 状态

每条长期知识建议标注状态：

- Confirmed - 已确认事实，可以用于 spec/plan/apply。
- Candidate - 候选知识，等待 archive 确认。
- Assumed - 临时假设，不能进入最终实现依据。
- Stale - 可能过期，需要复核。
- Conflict - 与代码、spec、用户确认或其他知识冲突。
- Deprecated - 已废弃，仅保留历史参考。

Memory 可以帮助召回，但不能覆盖 Confirmed knowledge、当前 spec、用户确认或代码证据。

## Knowledge Evidence Contract

每条长期知识至少要有：

- Status: Confirmed / Candidate / Assumed / Stale / Conflict / Deprecated
- Source: user / spec / code / decision / archive / external-doc
- Verified At: YYYY-MM-DD 或 Commit
- Verified Against: 文件路径、spec、decision、测试命令、代码证据或用户确认
- Scope: personal / project / team / enterprise

没有证据的内容只能进入 Knowledge Gap 或 Candidate，不能进入 final spec/design/tasks/context-pack。

```text
No Evidence, No Fact.
No Confirmation, No Execution.
No Impact, No Brownfield Change.
```
""",
    "knowledge/index.md": """# Knowledge Index

> 每次非平凡 change/plan/apply 前先读这里，再按任务打开相关知识文件。

## Product Knowledge

| Topic | File | Status | When To Read | Evidence Rule |
|-------|------|--------|--------------|---------------|
| Product overview | `product/overview.md` | Candidate | 新需求、范围讨论、产品目标变化 | Source + Verified Against required |
| Roles and permissions | `product/roles.md` | Candidate | 涉及用户、权限、审批或可见性 | Source + Verified Against required |
| Domain concepts | `product/domain.md` | Candidate | 涉及业务术语、对象和状态 | Source + Verified Against required |
| Product flows | `product/flows.md` | Candidate | 涉及流程、状态机、用户路径 | Source + Verified Against required |
| Business rules | `product/rules.md` | Candidate | 涉及业务规则、验收标准、不变量 | Source + Verified Against required |
| Product decisions | `product/decisions.md` | Candidate | 涉及产品取舍、非目标、延期范围 | Source + Verified Against required |

## Technical Knowledge

| Topic | File | Status | When To Read | Evidence Rule |
|-------|------|--------|--------------|---------------|
| Stack | `technical/stack.md` | Candidate | 技术选型、依赖、运行环境 | Code/config evidence required |
| Architecture | `technical/architecture.md` | Candidate | 模块边界、依赖方向、设计变化 | Code/config evidence required |
| Modules | `technical/modules.md` | Candidate | 查找实现位置、影响面 | Code evidence required |
| Data and interfaces | `technical/data-and-interfaces.md` | Candidate | 数据模型、API、事件、集成 | Code/schema/contract evidence required |
| Operations | `technical/operations.md` | Candidate | 启动、部署、回滚、排障 | Script/config evidence required |
| Testing | `technical/testing.md` | Candidate | 验证策略、测试命令、回归风险 | Test/build evidence required |

## Current State

- Current focus: `current.md`
- Project cognition: `../project-cognition.md`
- Standards: `../standards/`
- Decisions: `../decisions/`

## Retrieval Rule

Read only the entries relevant to the current task. If a needed knowledge file is missing or stale, record a Knowledge Gap and ask whether to refresh it.

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|--------|-------------------|----------------|--------|-----------|--------|
""",
    "knowledge/current.md": """# Current Project State

## Current Focus

## Recently Completed

## Active Risks

## Open Knowledge Gaps

## Next Useful Reads
""",
    "knowledge/product/README.md": """# Product Knowledge

产品知识回答：为什么做、给谁做、业务规则是什么、什么不做。

这些内容主要服务 `discovery`、`spec` 和验收标准。技术实现不能偷偷改写产品事实。
""",
    "knowledge/product/overview.md": """# Product Overview

| Item | Content | Status | Source | Verified At | Verified Against | Scope |
|------|---------|--------|--------|-------------|------------------|-------|
| Problem | | Candidate | | | | Project |
| Target users | | Candidate | | | | Project |
| Product goals | | Candidate | | | | Project |
| Non-goals | | Candidate | | | | Project |
""",
    "knowledge/product/roles.md": """# Roles And Permissions

| Role | Capabilities | Restrictions | Status | Source | Verified At | Verified Against | Scope |
|------|--------------|--------------|--------|--------|-------------|------------------|-------|
""",
    "knowledge/product/domain.md": """# Domain Concepts

| Concept | Meaning | Related Rules | Status | Source | Verified At | Verified Against | Scope |
|---------|---------|---------------|--------|--------|-------------|------------------|-------|
""",
    "knowledge/product/flows.md": """# Product Flows

## Flow Index

| Flow | Actors | Status | Source | Verified At | Verified Against | Scope |
|------|--------|--------|--------|-------------|------------------|-------|

## Flow Details
""",
    "knowledge/product/rules.md": """# Business Rules

| Rule ID | Rule | Status | Source | Verified At | Verified Against | Scope | Related Specs |
|---------|------|--------|--------|-------------|------------------|-------|---------------|
""",
    "knowledge/product/decisions.md": """# Product Decisions

| Decision ID | Decision | Status | Source | Verified At | Verified Against | Scope | Impact |
|-------------|----------|--------|--------|-------------|------------------|-------|--------|
""",
    "knowledge/technical/README.md": """# Technical Knowledge

技术知识回答：系统怎么实现、怎么运行、怎么安全地改。

这些内容主要服务 `plan`、`apply`、`check` 和遗留项目影响面分析。技术知识必须接受代码证据复核。
""",
    "knowledge/technical/stack.md": """# Technical Stack

| Area | Choice | Version / Evidence | Status | Source | Verified At | Verified Against | Scope |
|------|--------|--------------------|--------|--------|-------------|------------------|-------|
""",
    "knowledge/technical/architecture.md": """# Architecture Knowledge

## System Shape

## Boundaries

## Dependency Direction

## Architecture Decisions
""",
    "knowledge/technical/modules.md": """# Module Map

| Module | Responsibility | Key Files | Depends On | Status | Source | Verified At | Verified Against | Scope |
|--------|----------------|-----------|------------|--------|--------|-------------|------------------|-------|
""",
    "knowledge/technical/data-and-interfaces.md": """# Data And Interfaces

## Data Models

| Object / Table | Purpose | Key Fields | Status | Source | Verified At | Verified Against | Scope |
|----------------|---------|------------|--------|--------|-------------|------------------|-------|

## APIs / Events / Integrations

| Contract | Purpose | Producer | Consumer | Status | Source | Verified At | Verified Against | Scope |
|----------|---------|----------|----------|--------|--------|-------------|------------------|-------|
""",
    "knowledge/technical/operations.md": """# Operations

## Setup

## Local Run

## Build

## Deploy / Rollback

## Troubleshooting
""",
    "knowledge/technical/testing.md": """# Testing Knowledge

| Scope | Command | What It Proves | Status | Source | Verified At | Verified Against |
|-------|---------|----------------|--------|--------|-------------|------------------|
""",
    "memory/README.md": """# Project Memory

Memory 存放经验、候选知识和过程性记忆。它帮助未来 agent 少重复探索，但不能直接成为产品或技术事实。

## 文件

- `candidates.md` - 本次或历史需求中发现的候选知识，等待 archive 确认。
- `procedures.md` - 可复用流程、排障步骤、容易犯错的操作。
- `episodic/` - 重要工作片段、事故或里程碑的简短记录。

长期稳定事实应进入 `knowledge/`、`standards/` 或 `decisions/`，而不是一直留在 memory。
""",
    "memory/candidates.md": """# Memory Candidates

| Candidate | Type | Scope | Source | Status | Target | Evidence Needed | Promotion Gate |
|-----------|------|-------|--------|--------|--------|-----------------|----------------|
""",
    "memory/procedures.md": """# Procedures And Lessons

| Procedure / Lesson | When To Use | Evidence | Status | Target | Verified At | Scope |
|--------------------|-------------|----------|--------|--------|-------------|-------|
""",
    "memory/episodic/README.md": """# Episodic Memory

这里保存重要需求、事故、迁移或协作事件的短摘要。不要粘贴完整聊天记录。

推荐文件名：

```text
YYYY-MM-DD-short-event.md
```
""",
    "standards/README.md": """# Development Standards

这里存放项目长期开发规范。它回答“这个项目应该怎么写、怎么测、怎么协作”。

建议把这些文件提交到仓库，让人类开发者和 AI 助手共同遵守。

## 文件

- `coding.md` - 代码风格、命名、错误处理、日志、注释规范
- `testing.md` - 测试策略、覆盖率、测试命名、测试数据
- `architecture.md` - 分层、模块边界、依赖方向、扩展方式
- `security.md` - 输入校验、敏感信息、权限、依赖安全
- `git.md` - 分支、提交、PR、变更粒度
- `ai.md` - AI 助手必须遵守的项目规则
- `company/` - 可选公司/团队规范包。放置外部规范时先读 `company/README.md`，再按任务读取相关文件。

## 与 AGENTS.md 的关系

`.sdc/standards/` 是完整开发规范，适合长期维护。
`AGENTS.md` 是 AI 执行护栏，可以由 `/sdc:harness` 从 standards 中提炼。

## Company Standards Packs

如果团队已有现成规范，请放在 `company/` 下，或运行：

```bash
sdc standards import /path/to/spec-rules
```

AI 不应一次性读取整个规范包。先读 `company/README.md`，再按任务加载相关规范文件。
""",
    "standards/company/README.md": """# Company Standards Pack

<!-- SDC-MANAGED-STANDARDS-PACK -->

这里放公司/团队已有开发规范。默认不内置任何公司私有规则；请通过导入命令或手工复制维护。

## Recommended Import

```bash
sdc standards import /path/to/spec-rules
```

## Routing Rule

Agents must read this index first, then load only the relevant rule files for the current task. Do not bulk-load the whole standards pack.

## Imported Files

| File | Title | When To Read |
|------|-------|--------------|
""",
    "standards/coding.md": """# Coding Standard

## 命名

- 使用项目现有命名风格
- 名称必须表达业务含义，避免无意义缩写

## 函数和模块

- 单个函数只做一件事
- 优先复用项目已有工具和抽象
- 不为未来可能性提前设计复杂抽象

## 错误处理

- 不吞异常
- 错误信息必须能指导定位问题
- 用户可见错误和内部错误要区分

## 注释

- 只在复杂业务规则、边界条件或非显然取舍处写注释
- 不写重复代码含义的空注释
""",
    "standards/testing.md": """# Testing Standard

## 测试策略

- 核心业务逻辑必须有单元测试
- 跨模块流程必须有集成测试
- 用户关键路径需要冒烟测试

## 测试要求

- 测试名称表达业务行为
- 覆盖正常路径、异常路径和边界条件
- 不为了覆盖率编写无意义测试

## 运行记录

每次 `/sdc:check` 后，将测试结果记录到 `.sdc/reports/` 或当前 change 的 `notes.md`。
""",
    "standards/architecture.md": """# Architecture Standard

## 模块边界

- 保持现有分层和模块边界
- 不跨层直接访问内部实现
- 新能力优先放在最贴近业务语义的位置

## 依赖方向

- 业务核心不依赖外围适配
- 公共工具不能反向依赖业务模块

## 设计取舍

重要架构决策必须记录到 `.sdc/decisions/`。
""",
    "standards/security.md": """# Security Standard

## 输入和输出

- 所有外部输入必须校验
- 用户可控内容输出前必须按场景转义或过滤

## 敏感信息

- 不硬编码密钥、令牌、密码
- 日志不得输出敏感信息

## 依赖

- 新增依赖前必须说明用途、维护状态和替代方案
""",
    "standards/git.md": """# Git Standard

## 变更粒度

- 一个提交只表达一个清晰意图
- 不混入无关格式化或本地配置

## 提交前

- 运行相关测试
- 更新 `.sdc/changes/active/<change-id>/notes.md`
- 需要时更新 `.sdc/specs/` 或 `.sdc/standards/`

## PR

- 说明需求背景、实现摘要、测试结果和风险
""",
    "standards/ai.md": """# AI Collaboration Standard

## 必须做

- 开始新需求前确认 `.sdc/` 是否存在
- 先读 `.sdc/constitution.md`，再读 `AGENTS.md`
- 非平凡需求先读 `.sdc/knowledge/index.md`，再按任务读取相关产品/技术知识
- 如果 `.sdc/standards/company/README.md` 存在且当前任务涉及代码生成、架构、接口、数据、事务、测试、安全或公司约定，先读该索引，再只读取相关公司规范文件
- 新需求进入 `.sdc/changes/active/`
- 遗留项目先读 `.sdc/project-cognition.md`
- 实现前先看 `discovery.md`、`proposal.md`、`spec.md`、`impact.md`、`design.md`、`tasks.md`、`context-pack.md`
- 保持 `SCN-* -> REQ-* -> AC-* -> T### -> 验证证据` 追溯链
- apply/check 过程中把新发现写入 `knowledge-candidates.md`，不要直接污染长期知识库
- 完成前执行 `/sdc:check`
- 归档时执行 `/sdc:archive`

## 绝对不要做

- 不要跳过需求记录直接改代码
- 不要把模板内容当作有效规范
- 不要在 spec/design/tasks/code 冲突时继续猜测
- 不要在需求不确定时跳过 Discovery Gate
- 不要在遗留项目需求确认后跳过 Change Impact Gate
- 不要覆盖用户编写的 `.sdc/` 文件；SDC 托管模板升级必须保留备份
- 不要删除 change 历史
- 不要忽略 `.sdc/standards/` 中的项目规范
- 不要一次性读取整个 `.sdc/standards/company/`；先读索引，按任务按需加载
- 不要把 `.sdc/memory/` 中的 Candidate/Assumed 当作 confirmed 项目事实
""",
    "decisions/README.md": """# Decisions

记录重要技术/产品决策。推荐文件名：

```text
YYYY-MM-DD-short-title.md
```
""",
    "reviews/README.md": """# Reviews

保存 `sdc-review` 的代码审查结果。
""",
    "reports/README.md": """# Reports

保存 `/sdc:check` 产生的测试、覆盖率、质量检查、bug 分析、impact 分析和 repo-analysis 报告。

## 子目录

- `bug/` - 缺陷分析报告，只分析不直接改代码
- `impact/` - 变更影响面和上线风险分析
- `repo-analysis/` - 存量项目结构、风险和改造建议
""",
    "templates/change.md": """# Change Proposal

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|--------|--------|----------|----------------|

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|--------|-------------------|----------------|--------|-----------|--------|

## 背景

## 目标

## 非目标

## 初始场景

- SCN-01:

## 初始需求

- REQ-01:

## 初始验收标准

- AC-01:

## 任务清单

## 风险和回滚
""",
    "templates/discovery.md": """# Discovery

> 需求不确定时先使用本文件。Discovery 用于发散和收敛，不是 Confirmed spec。
> Open Questions 未闭合时，只维护 discovery、可选 Draft proposal 和简短 notes，不生成完整 spec/design/tasks。

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|--------|--------|----------|----------------|

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|--------|-------------------|----------------|--------|-----------|--------|

## Current Understanding

## Candidate Directions

| Option | Description | Pros | Cons | Status |
|--------|-------------|------|------|--------|

## Tradeoffs

## Recommended MVP

## Decision Ledger

| ID | Decision | Status | Source | Impact | Next Step |
|----|----------|--------|--------|--------|-----------|

## Open Questions

| ID | Question | Why It Matters | Options | Required Before |
|----|----------|----------------|---------|-----------------|

## Exit Criteria

- [ ] MVP scope confirmed
- [ ] high-impact decisions confirmed or explicitly deferred
- [ ] acceptance direction is clear
""",
    "templates/tasks.md": """# Tasks

## 实现任务

- [ ] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] Draft task
  - Depends on: none
  - Verify: TODO
  - Source: spec.md#AC-01

## 验证任务

- [ ] T900 [REQ-01] [AC-01] [Phase Verify] [Size: S] Run validation
  - Depends on: T001
  - Verify: TODO
  - Source: spec.md#AC-01
""",
    "templates/design.md": """# Design

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|--------|--------|----------|----------------|

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|--------|-------------------|----------------|--------|-----------|--------|

## Solution Summary / 方案摘要

## Impact Scope / 影响范围

## Non-Scope / 不改范围

## Key Tradeoffs / 关键取舍

## Data, API, State, or Interaction Changes / 数据、接口、状态或交互变化

## Brownfield Impact Summary / 遗留影响摘要

## REQ/AC to Design Decision Mapping / 追溯映射

## Risks, Rollback, and Migration / 风险、回滚和迁移

## Alternatives / 替代方案
""",
    "templates/spec.md": """# Spec

## 0. 文档元信息

- Status: Draft
- Schema: SDC 1.2.0
- Source:

## 1. Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|--------|--------|----------|----------------|

## 1.1 Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|--------|-------------------|----------------|--------|-----------|--------|

## 2. Decision Ledger / 决策台账

| ID | 决策 | 状态 | 依据来源 | 是否允许进入 REQ/AC | 下一步 |
|----|------|------|----------|----------------------|--------|

## 3. Glossary / 统一语言

## 4. 背景与目标

## 5. Business Invariants / 业务不变量

### INV-01

## 6. 场景与需求

### SCN-01

### REQ-01

## 7. Acceptance Criteria / 验收标准

### AC-01

Given ...
When ...
Then ...

## 8. 验证策略

## 9. 风险、假设与待确认项

## 10. 追溯关系矩阵
""",
    "templates/stop-line-report.md": """# Stop-Line Report

## Trigger

## Evidence

## Conflicting Files

## Affected REQ/AC

## Options

## Recommended Next Step
""",
    "templates/bug-analysis.md": """# Bug Analysis

## Symptom

## Reproduction

## Evidence

## Related Spec / Plan / Tasks

## Root Cause Candidates

## Affected REQ/AC

## Recommended Fix
""",
    "templates/project-cognition.md": """# Project Cognition Template

> 遗留项目整体认知模板。只基于代码、配置、构建、测试和运行脚本等证据填写；文档和注释只能作为线索。

## 0. 分析快照

- 目标仓库/目录：
- 分析时间：
- 分支 / Commit / 子模块状态：
- 技术生态线索：
- 可见配置与依赖范围：
- 本次分析限制：

## 1. 一句话概述

## 2. 系统形态与技术栈

## 3. 核心数据模型与 Schema/DDL

## 4. 关键入口与启动方式

## 5. 目录结构与模块地图

## 6. 核心链路与数据流

## 7. 配置、数据存储与外部集成

## 8. 可观测性与运行诊断线索

## 9. 测试、构建与交付现状

## 10. 已确认风险与复杂区域

## 11. 待确认问题

## 12. 建议阅读顺序

## 13. 证据索引
""",
    "templates/change-impact.md": """# Change Impact

> 遗留项目在需求确认后的变更影响面分析。它发生在 confirmed spec 之后、plan/apply 之前。

## Analysis Snapshot

- 目标仓库/目录：
- 变更目标：
- 分析时间：
- 分支 / Commit / 子模块状态：
- 技术生态线索：
- 可见配置与依赖范围：
- 本次分析限制：

## Entry Points And Call Chain

## Direct Changes Required

| File / Contract | Reason | Evidence | Related REQ/AC |
|-----------------|--------|----------|----------------|

## Cascading Impact

## Contracts / Data / Config / Permissions / Security / Observability

## Tests And Regression Strategy

## Implementation Order And Rollback Boundary

## Open Questions

| Question | Why It Matters | Blocking? |
|----------|----------------|-----------|

## Evidence Index

| Claim | Source |
|-------|--------|
""",
    "templates/context-pack.md": """# Context Pack

> 给执行 Agent 的短交接包。由 plan 阶段从 spec、impact、design、tasks 和知识库压缩生成。

## Goal

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|--------|--------|----------|----------------|

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|--------|-------------------|----------------|--------|-----------|--------|

## Confirmed Product Knowledge

## Confirmed Technical Knowledge

## Execution Boundaries

## Forbidden Assumptions

- Do not invent product rules, roles, permissions, approval flows, notification behavior, database choices, migration strategy, rollout policy, or integration contracts that are not confirmed in spec/knowledge.

## Task And Traceability Summary

## Validation Commands

## Knowledge Candidate Routing

- Product knowledge candidates:
- Technical knowledge candidates:
- Memory/procedure candidates:
""",
    "templates/knowledge-candidates.md": """# Knowledge Candidates

> apply/check 阶段记录候选知识。archive 时确认后再写入长期知识库。

| Candidate | Type | Scope | Source | Status | Target | Evidence Needed | Promotion Gate |
|-----------|------|-------|--------|--------|--------|-----------------|----------------|
""",
    "templates/knowledge-index.md": """# Knowledge Index

## Product Knowledge

| Topic | File | Status | When To Read | Evidence Rule |
|-------|------|--------|--------------|---------------|

## Technical Knowledge

| Topic | File | Status | When To Read | Evidence Rule |
|-------|------|--------|--------------|---------------|

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|--------|-------------------|----------------|--------|-----------|--------|

## Current State

## Retrieval Rule
""",
    "templates/repo-analysis.md": """# Repo Analysis

## Tech Stack

## Entry Points

## Build and Test Commands

## Core Modules

## Business Capability Map

## Risks

## Recommended SDC Assets
""",
    "templates/decision.md": """# Decision Record

## 状态

Proposed / Accepted / Deprecated

## 背景

## 决策

## 影响

## 替代方案
""",
    ".gitignore": """# SDC workspace
# 默认建议提交 .sdc 内容，因为它是项目需求和交付记录。
# 如需忽略本地临时文件，请写在下面。

*.tmp
""",
}

TEMPLATE = """# SDC {name} 文档

> 创建时间：{time}

请在这里粘贴从 AI 助手生成的内容：

---

"""

HEADER = "\033[95m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
ENDC = "\033[0m"


def print_color(color, text):
    print(f"{color}{text}{ENDC}")


def slugify(value):
    """Convert a change name into a filesystem-friendly slug."""
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value.strip().lower())
    slug = slug.strip("-")
    return slug or "change"


def change_path(change_id):
    active = SDC_DIR / "changes" / "active" / change_id
    if active.exists():
        return active

    legacy = SDC_DIR / "changes" / change_id
    if legacy.exists():
        return legacy

    return active


def archive_change_path(change_id):
    return SDC_DIR / "changes" / "archive" / change_id


def read_text(filepath):
    if not filepath.exists():
        return ""
    return filepath.read_text()


def has_real_content(filepath):
    text = read_text(filepath)
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith(">") and not line.strip().startswith("#")
    ]
    placeholders = ("（", "）", "TODO", "todo", "Draft task", "...")
    return any(not any(marker in line for marker in placeholders) for line in lines)


def validate_no_template_placeholders(errors, filepath):
    text = read_text(filepath)
    if not text:
        return

    placeholder_patterns = [
        (r"\bTODO\b", "TODO"),
        (r"Draft task", "Draft task"),
        (r"Given \.\.\.", "Given ..."),
        (r"When \.\.\.", "When ..."),
        (r"Then \.\.\.", "Then ..."),
        (r"^\s*-\s+(SCN|REQ|AC)-0*1:\s*$", "empty SCN/REQ/AC placeholder"),
        (r"^\s*-\s*Source:\s*$", "empty Source"),
        (r"^\s*-\s*Verify:\s*TODO\s*$", "empty Verify"),
        (r"^\s*-\s*目标仓库/目录：\s*$", "empty impact snapshot field"),
        (r"^\s*-\s*变更目标：\s*$", "empty impact snapshot field"),
    ]

    for pattern, label in placeholder_patterns:
        if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
            errors.append(f"{filepath} 仍包含模板占位内容: {label}")
            return


def has_required_heading_set(text, required_headings):
    return all(heading in text for heading in required_headings)


def validate_task_trace(errors, filepath):
    text = read_text(filepath)
    if "- [ ]" not in text and "- [x]" not in text:
        errors.append(f"{filepath} 缺少任务复选框")
        return

    if "TODO" in text or "Draft task" in text:
        errors.append(f"{filepath} 仍包含任务模板占位内容")

    task_lines = [line.strip() for line in text.splitlines() if line.strip().startswith("- [")]
    task_pattern = re.compile(r"- \[[ xX]\] T\d{3} \[REQ-[^\]]+\] \[AC-[^\]]+\] \[Phase [^\]]+\] \[Size: ([SM])\]")
    for line in task_lines:
        match = task_pattern.search(line)
        if not match:
            errors.append(f"{filepath} 任务格式无效: {line}")
        if "[Size: L]" in line:
            errors.append(f"{filepath} 任务不能使用 Size L: {line}")

    for marker in ("Depends on:", "Verify:", "Source:"):
        if marker not in text:
            errors.append(f"{filepath} 缺少任务字段: {marker}")


def validate_no_unconfirmed_execution_inputs(errors, filepath):
    text = read_text(filepath)
    if not text:
        return

    blocking_states = sorted(set(re.findall(r"\b(Proposed|Assumed|TBD|Conflict|Stale)\b", text)))
    if blocking_states:
        errors.append(f"{filepath} 包含未确认/不可执行状态: {', '.join(blocking_states)}")

    if re.search(r"Knowledge Gap", text, re.IGNORECASE):
        open_gap_patterns = [
            r"\|\s*KG-[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|\s*(Open|TBD|Blocking|Unresolved|待确认|未闭合|阻塞)\s*\|",
            r"Knowledge Gap[^\n]*(Open|TBD|Blocking|Unresolved|待确认|未闭合|阻塞)",
        ]
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in open_gap_patterns):
            errors.append(f"{filepath} 存在未闭合 Knowledge Gap，不能进入执行或归档")


def validate_spec_trace(errors, filepath):
    text = read_text(filepath)
    for marker in ("INV-", "SCN-", "REQ-", "AC-"):
        if marker not in text:
            errors.append(f"{filepath} 缺少追溯标识: {marker}")
    if "Decision Ledger" not in text and "决策台账" not in text:
        errors.append(f"{filepath} 缺少 Decision Ledger / 决策台账")


def discovery_gate_open(base):
    """Return True when discovery still contains unresolved exit criteria or blocking states."""
    text = read_text(base / "discovery.md")
    if not text:
        return False

    unchecked_exit = re.search(
        r"- \[ \].*(MVP|scope|decision|acceptance|确认|高影响|验收)",
        text,
        re.IGNORECASE,
    )
    blocking_state = re.search(r"\b(Proposed|Assumed|TBD|Conflict)\b", text)
    return bool(unchecked_exit or blocking_state)


def validate_no_write_ahead(errors, filepath):
    text = read_text(filepath)
    if not text:
        return

    policy_markers = (
        "No Write-Ahead Confirmation",
        "Interpretation summaries are not consent",
        "Forbidden write-ahead patterns",
        "Do not write files with",
    )
    if any(marker in text for marker in policy_markers):
        return

    patterns = [
        r"if (this is )?wrong[,，]? tell me.*(update|adjust|proceed)",
        r"proceed unless you object",
        r"如有偏差请告知.*(先|立即).*(更新|修改|调整|改)",
        r"如果不对告诉我.*(先|立即).*(更新|修改|调整|改)",
        r"若.*有出入.*(先|下面).*更新",
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            errors.append(f"{filepath} 包含 write-ahead 确认话术，必须先获得显式确认")
            return


def validate_discovery_artifact_budget(errors, warnings, base):
    if not discovery_gate_open(base):
        return False

    for filename in ("spec.md", "impact.md", "design.md", "tasks.md", "context-pack.md", "knowledge-candidates.md"):
        filepath = base / filename
        if filepath.exists():
            errors.append(f"Discovery Gate 未退出，但已生成 {filepath}；只允许 discovery.md / Draft proposal.md / notes.md")

    warnings.append("Discovery Gate 仍打开：这是允许的草稿状态，先关闭 Open Questions 再生成 spec/design/tasks")
    return True


def is_stale_managed_template(relative_path, text):
    """Detect SDC-generated old templates that can be upgraded safely."""
    normalized = text.replace("\r\n", "\n")
    template_paths = {
        "README.md",
        "constitution.md",
        "knowledge/index.md",
        "current/discovery.md",
        "current/spec.md",
        "current/context-pack.md",
        "current/knowledge-candidates.md",
        "memory/candidates.md",
        "templates/change.md",
        "templates/discovery.md",
        "templates/design.md",
        "templates/spec.md",
        "templates/context-pack.md",
        "templates/knowledge-candidates.md",
        "templates/knowledge-index.md",
        "standards/README.md",
        "standards/ai.md",
        "standards/company/README.md",
        "current/tasks.md",
        "templates/tasks.md",
    }
    if relative_path not in template_paths:
        return False

    if relative_path == "README.md":
        return "# SDC Workspace" in normalized and (
            "standards/company/" not in normalized
            or "SDC v1.1" in normalized
        )

    if relative_path == "constitution.md":
        return "# SDC Project Constitution" in normalized and (
            "Knowledge and Memory Discipline" not in normalized
            or "No Evidence, No Fact" not in normalized
        )

    if relative_path == "standards/README.md":
        return "# Development Standards" in normalized and "Company Standards Packs" not in normalized

    if relative_path == "standards/ai.md":
        return "# AI Collaboration Standard" in normalized and ".sdc/standards/company/README.md" not in normalized

    if relative_path == "standards/company/README.md":
        return "# Company Standards Pack" in normalized and "Routing Rule" not in normalized

    if relative_path in {"knowledge/index.md", "templates/knowledge-index.md"}:
        return "# Knowledge Index" in normalized and (
            "Evidence Rule" not in normalized
            or "## Knowledge Gaps" not in normalized
        )

    if relative_path in {"current/knowledge-candidates.md", "templates/knowledge-candidates.md", "memory/candidates.md"}:
        return (
            ("# Knowledge Candidates" in normalized or "# Current Knowledge Candidates" in normalized or "# Memory Candidates" in normalized)
            and ("Evidence Needed" not in normalized or "Promotion Gate" not in normalized)
        )

    if relative_path in {"current/context-pack.md", "templates/context-pack.md"}:
        return "# Context Pack" in normalized and (
            "## Knowledge Gaps" not in normalized
            or "## Forbidden Assumptions" not in normalized
            or "| Source | Status | Evidence | Why It Matters |" not in normalized
        )

    if relative_path in {"current/discovery.md", "templates/discovery.md"}:
        return "# Discovery" in normalized and (
            "## Knowledge Gaps" not in normalized
            or "| Source | Status | Evidence | Why It Matters |" not in normalized
        )

    if relative_path == "templates/change.md":
        return "# Change Proposal" in normalized and (
            "## Knowledge Gaps" not in normalized
            or "| Source | Status | Evidence | Why It Matters |" not in normalized
        )

    if relative_path == "templates/design.md":
        return "# Design" in normalized and (
            "## Knowledge Gaps" not in normalized
            or "| Source | Status | Evidence | Why It Matters |" not in normalized
        )

    if relative_path.endswith("spec.md"):
        looks_generated = (
            "Given ..." in normalized
            or "## 场景" in normalized
            or "## Requirements" in normalized
        )
        return looks_generated and "INV-" not in normalized

    if relative_path.endswith("tasks.md"):
        old_task_shape = (
            "### T1" in normalized
            or "Status:" in normalized
            or "AC:" in normalized
            or "Test:" in normalized
            or "[Size: L]" in normalized
        )
        missing_standard_shape = "T001 [REQ-01] [AC-01] [Phase" not in normalized
        looks_generated = "Draft task" in normalized or old_task_shape
        if relative_path == "current/tasks.md":
            looks_generated = looks_generated and (
                "Draft task" in normalized
                or "### T1 — title" in normalized
                or "### T1 - title" in normalized
            )
        return looks_generated and (old_task_shape or missing_standard_shape)

    return False


def write_or_upgrade_managed(relative_path, content):
    """Create missing SDC files or upgrade stale generated templates with backup."""
    filepath = SDC_DIR / relative_path
    if not filepath.exists():
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
        return "created"

    current = read_text(filepath)
    if is_stale_managed_template(relative_path, current):
        backup = filepath.with_name(f"{filepath.name}.bak-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        backup.write_text(current)
        filepath.write_text(content)
        return f"upgraded (backup: {backup.relative_to(SDC_DIR)})"

    return None


def standards_pack_slug(name):
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", (name or "").strip().lower()).strip("-")
    return slug or "company"


def is_standard_pack_source_file(path, source_root):
    if not path.is_file():
        return False
    try:
        relative_parts = path.relative_to(source_root).parts
    except ValueError:
        relative_parts = path.parts

    if any(part.startswith(".") or part in STANDARD_PACK_IGNORED_NAMES for part in relative_parts):
        return False

    return path.suffix.lower() in STANDARD_PACK_DOC_SUFFIXES


def iter_standard_pack_files(source):
    if source.is_file():
        return [source] if is_standard_pack_source_file(source, source.parent) else []
    return [
        path
        for path in sorted(source.rglob("*"))
        if is_standard_pack_source_file(path, source)
    ]


def file_bytes_equal(left, right):
    if not left.exists() or not right.exists():
        return False
    return left.read_bytes() == right.read_bytes()


def standards_title(path):
    try:
        for line in path.read_text(errors="ignore").splitlines()[:80]:
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or path.stem.replace("-", " ").title()
    except UnicodeDecodeError:
        pass
    return path.stem.replace("-", " ").replace("_", " ").title()


def standards_routing_hint(relative_path):
    lower = str(relative_path).lower()
    rules = [
        (("code-generation", "scaffold", "generator"), "Read when creating new code scaffolds, entities, services, or generated files."),
        (("surgical", "refactor", "edit"), "Read before making focused changes to existing code."),
        (("aggregate", "valueobject", "domain"), "Read when touching aggregates, value objects, domain models, or domain invariants."),
        (("application-service", "controller", "facade", "orchestration"), "Read when touching application services, controllers, facades, or orchestration logic."),
        (("repository", "client", "acl", "infrastructure"), "Read when touching repositories, external clients, ACLs, or infrastructure adapters."),
        (("data-objects", "dto", "request", "response", "money", "time"), "Read when defining DTOs, request/response objects, money/time fields, or data conversion."),
        (("enum", "schema"), "Read when adding or changing enums, schemas, or value constraints."),
        (("transaction", "tx"), "Read when changing transaction boundaries, consistency rules, or rollback behavior."),
        (("logging", "log"), "Read when adding logs, diagnostic fields, trace IDs, or operational messages."),
        (("exception", "monitoring", "error"), "Read when changing exceptions, monitoring, alarms, or error-code behavior."),
        (("middleware", "redis", "mq", "lock", "job"), "Read when touching Redis, MQ, locks, jobs, cache, or middleware integration."),
        (("loop", "query", "performance", "single-record"), "Read when changing queries, loops, N+1 risks, or performance-sensitive reads."),
        (("naming", "name"), "Read when naming packages, classes, methods, fields, constants, or files."),
        (("comment", "javadoc"), "Read when writing comments, JavaDoc, or documentation inside code."),
        (("configuration", "properties", "config"), "Read when adding configuration properties, feature flags, or environment settings."),
        (("testing", "test"), "Read when writing or changing tests, fixtures, mocks, or validation commands."),
    ]
    for needles, hint in rules:
        if any(needle in lower for needle in needles):
            return hint
    return "Read when the current task touches this topic."


def standards_pack_index_content(pack_name, entries):
    lines = [
        "# Company Standards Pack" if pack_name == "company" else f"# {pack_name} Standards Pack",
        "",
        STANDARD_PACK_MARKER,
        "",
        "This index routes company or team engineering standards. The SDC package does not ship private rules; imported rules live in the project workspace.",
        "",
        "## Routing Rule",
        "",
        "Agents must read this index first, then load only the relevant rule files for the current task. Do not bulk-load the whole standards pack.",
        "",
        "## Imported Files",
        "",
        "| File | Title | When To Read |",
        "|------|-------|--------------|",
    ]
    for relative_file, title, hint in entries:
        safe_file = str(relative_file).replace("\\", "/")
        lines.append(f"| `{safe_file}` | {title} | {hint} |")
    if not entries:
        lines.append("| _none yet_ |  |  |")
    lines.extend([
        "",
        "## Maintenance",
        "",
        "- Re-run `sdc standards import <path>` when the external standards pack changes.",
        "- If a file conflicts with an existing project rule, record the decision in `.sdc/decisions/` before using it as execution guidance.",
        "- Keep private company standards inside the target project workspace or private repositories; do not publish them with SDC itself.",
        "",
    ])
    return "\n".join(lines)


def write_standards_pack_index(target_dir, pack_name, entries):
    readme = target_dir / "README.md"
    index_path = readme
    if readme.exists() and STANDARD_PACK_MARKER not in read_text(readme):
        index_path = target_dir / "IMPORT-INDEX.md"
    index_path.write_text(standards_pack_index_content(pack_name, entries))
    return index_path


def cmd_import_standards(source_path, pack_name="company"):
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
        return False

    source = Path(source_path).expanduser()
    if not source.exists():
        print_color(RED, f"❌ 规范目录不存在: {source_path}")
        return False

    pack_slug = standards_pack_slug(pack_name)
    target_dir = SDC_DIR / "standards" / pack_slug
    target_dir.mkdir(parents=True, exist_ok=True)

    source_root = source.parent if source.is_file() else source
    source_files = iter_standard_pack_files(source)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    imported_entries = []
    copied = []
    skipped = []
    conflicts = []

    for source_file in source_files:
        relative = source_file.relative_to(source_root)
        destination = target_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)

        actual_destination = destination
        if destination.exists():
            if file_bytes_equal(source_file, destination):
                skipped.append(str(destination.relative_to(target_dir)))
            else:
                actual_destination = destination.with_name(f"{destination.stem}.import-{timestamp}{destination.suffix}")
                conflicts.append(f"{destination.relative_to(target_dir)} -> {actual_destination.name}")

        if not actual_destination.exists():
            shutil.copy2(source_file, actual_destination)
            copied.append(str(actual_destination.relative_to(target_dir)))

        entry_relative = actual_destination.relative_to(target_dir)
        imported_entries.append((entry_relative, standards_title(actual_destination), standards_routing_hint(entry_relative)))

    index_path = write_standards_pack_index(target_dir, pack_slug, imported_entries)

    print_color(GREEN, "✅ Standards pack 已导入")
    print(f"   Pack: {pack_slug}")
    print(f"   Target: {target_dir}")
    print(f"   Index: {index_path.relative_to(SDC_DIR)}")
    print(f"   Files: {len(imported_entries)} indexed, {len(copied)} copied, {len(skipped)} unchanged")
    if conflicts:
        print("   Conflicts saved as timestamped imports:")
        for item in conflicts[:10]:
            print(f"  - {item}")
        if len(conflicts) > 10:
            print(f"  - ... {len(conflicts) - 10} more")
    if not imported_entries:
        print_color(YELLOW, "⚠️  未发现可导入的规范文档；支持 .md/.txt/.rst/.adoc/.yaml/.yml/.json")
    return True


def detect_project_kind():
    """Best-effort hint for whether init is running in a new or existing project."""
    marker_names = {
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "go.mod",
        "Cargo.toml",
        "composer.json",
        "Gemfile",
        "Makefile",
        "CMakeLists.txt",
        "docker-compose.yml",
        "compose.yaml",
    }
    ignored_dirs = {".git", ".sdc", ".idea", "node_modules", "dist", "build", "target", "coverage", "vendor"}
    source_suffixes = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".kt", ".go", ".rs", ".cs", ".php", ".rb", ".cpp", ".c", ".h"}

    markers = []
    source_count = 0

    for path in Path(".").iterdir():
        if path.name in ignored_dirs:
            continue
        if path.is_file() and path.name in marker_names:
            markers.append(path.name)
        elif path.is_dir() and path.name in {"src", "app", "lib", "cmd", "internal", "server", "client", "frontend", "backend", "tests"}:
            markers.append(f"{path.name}/")

    for path in Path(".").rglob("*"):
        if any(part in ignored_dirs for part in path.parts):
            continue
        if path.is_file() and path.suffix in source_suffixes:
            source_count += 1
            if source_count >= 5:
                break

    if markers or source_count >= 5:
        return "brownfield", markers[:8], source_count
    return "greenfield", markers, source_count


def cmd_init(standards_source=None, standards_name="company"):
    """初始化标准 SDC 工作区"""
    created = []
    upgraded = []
    project_kind, project_markers, source_count = detect_project_kind()

    SDC_DIR.mkdir(exist_ok=True)

    for dirname in DIRS:
        directory = SDC_DIR / dirname
        if not directory.exists():
            directory.mkdir(parents=True)
            created.append(f"{dirname}/")

    for relative_path, content in INIT_FILES.items():
        result = write_or_upgrade_managed(relative_path, content)
        if result == "created":
            created.append(relative_path)
        elif result and result.startswith("upgraded"):
            upgraded.append(f"{relative_path} {result}")

    if created or upgraded:
        print_color(GREEN, "✅ SDC 标准工作区已初始化")
        print(f"   目录: {SDC_DIR.absolute()}")
        print()
        if created:
            print("已创建:")
            for item in created:
                print(f"  - {item}")
        if upgraded:
            print("已安全升级的 SDC 托管模板:")
            for item in upgraded:
                print(f"  - {item}")
    else:
        print_color(YELLOW, "⚠️  SDC 工作区已存在，未覆盖任何文件")

    print()
    if project_kind == "brownfield":
        print_color(YELLOW, "🧭 检测到存量/遗留项目线索")
        if project_markers:
            print(f"   线索: {', '.join(project_markers)}")
        print(f"   源码文件线索: {source_count}+")
        print("   建议先用 /sdc:check repo 补全 .sdc/project-cognition.md。")
        print("   具体需求的影响面分析会在 change 需求确认后写入该 change 的 impact.md。")
        print()
    else:
        print_color(GREEN, "🧭 当前更像新项目 / Greenfield")
        print("   可以直接从 /sdc:change 开始记录第一版需求。")
        print()

    print("下一步:")
    print(f"  {BLUE}.sdc/knowledge/index.md{ENDC} - 先补最小产品/技术知识索引")
    print(f"  {BLUE}sdc discovery{ENDC} - 需求不确定时先探索和收敛 MVP")
    print(f"  {BLUE}sdc spec{ENDC}    - 编辑当前需求规范")
    print(f"  {BLUE}sdc plan{ENDC}    - 生成/编辑规范和实现计划")
    print(f"  {BLUE}sdc apply{ENDC}   - 执行当前需求迭代")
    print(f"  {BLUE}sdc change login-flow{ENDC} - 创建一次需求迭代")
    print(f"  {BLUE}sdc status{ENDC}  - 查看工作区状态")

    if standards_source:
        print()
        cmd_import_standards(standards_source, standards_name)


def print_change_intake(name):
    change_id = f"{date.today().isoformat()}-{slugify(name)}"
    print_color(YELLOW, "⚠️  Change Intake Gate：尚未创建任何 change 文件")
    print()
    print("在 SDC 中，创建 `.sdc/changes/active/*` 前必须先确认 4 类 intake 信息。")
    print("请先回答并确认下面问题；确认后再运行：")
    print(f"  {BLUE}sdc change {name} --confirmed-intake{ENDC}")
    print()
    print("## Change Intake")
    print(f"- Current request: {name}")
    print(f"- Recommended change id: {change_id}")
    print()
    print("## Required Questions")
    print("1. Project context: 这是新项目还是存量项目？目标用户是谁？个人还是团队使用？")
    print("2. Core scope: 当前 MVP 必须包含什么？哪些明确不做？")
    print("3. Technical preferences: 语言、框架、数据库、部署方式或集成偏好是什么？")
    print("4. Constraints and acceptance: 截止时间、预算、安全/合规约束，以及怎么证明完成？")
    print()
    print("SDC 不会在这些信息确认前写入 change 文件。")


def cmd_change(name, confirmed_intake=False):
    """创建一次需求迭代目录；未确认 intake 时只提出问题，不写文件。"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
        return

    if not confirmed_intake:
        print_change_intake(name)
        return

    change_id = f"{date.today().isoformat()}-{slugify(name)}"
    directory = SDC_DIR / "changes" / "active" / change_id

    if directory.exists():
        print_color(YELLOW, f"⚠️  需求迭代已存在: {directory}")
        return

    directory.mkdir(parents=True)
    files = {
        "discovery.md": INIT_FILES["templates/discovery.md"],
        "proposal.md": INIT_FILES["templates/change.md"].replace("# Change Proposal", f"# {change_id} Proposal")
        .replace("## 目标", "## Status\n\nDraft - Discovery Open\n\n## 目标"),
        "notes.md": f"""# Notes

> Change: {change_id}
> Created: {datetime.now().isoformat()}
> Status: Draft - Discovery Open

## Discovery Notes

## Confirmed Decisions

## Pending Questions
""",
    }

    for filename, content in files.items():
        (directory / filename).write_text(content)

    print_color(GREEN, "✅ SDC 需求迭代草稿已创建")
    print(f"   ID: {change_id}")
    print(f"   目录: {directory.absolute()}")
    print("   状态: Discovery Open（仅创建 discovery/proposal/notes）")
    print()
    print("下一步:")
    print(f"  {BLUE}.sdc/knowledge/index.md{ENDC} - 读取相关产品/技术知识后继续 discovery/spec")
    print(f"  {BLUE}sdc discovery{ENDC}         - 继续确认 MVP、Open Questions 和 Decision Ledger")
    print(f"  {BLUE}sdc spec{ENDC}              - Discovery 退出后再生成 SCN/REQ/AC")
    print(f"  {BLUE}impact.md{ENDC}             - 遗留项目需求确认后再做变更影响面分析")
    print(f"  {BLUE}sdc plan {change_id}{ENDC}   - spec/impact 确认后再生成计划")
    print(f"  {BLUE}sdc check {change_id}{ENDC}  - 综合检查")


def validate_file(errors, warnings, filepath, required_headings, require_content=True):
    if not filepath.exists():
        errors.append(f"缺少文件: {filepath}")
        return

    text = read_text(filepath)
    validate_no_write_ahead(errors, filepath)
    if require_content and not has_real_content(filepath):
        errors.append(f"内容仍是模板或缺少有效内容: {filepath}")
    if require_content:
        validate_no_template_placeholders(errors, filepath)

    for heading in required_headings:
        if heading not in text:
            errors.append(f"{filepath} 缺少章节: {heading}")


def validate_knowledge_workspace(errors, warnings):
    """Validate that the project knowledge/memory skeleton exists."""
    required = [
        (SDC_DIR / "knowledge" / "index.md", ["# Knowledge Index", "## Product Knowledge", "## Technical Knowledge"]),
        (SDC_DIR / "knowledge" / "product" / "README.md", ["# Product Knowledge"]),
        (SDC_DIR / "knowledge" / "technical" / "README.md", ["# Technical Knowledge"]),
        (SDC_DIR / "memory" / "candidates.md", ["# Memory Candidates"]),
    ]

    for filepath, headings in required:
        validate_file(errors, warnings, filepath, headings, require_content=False)


def validate_context_pack(errors, warnings, filepath):
    validate_file(
        errors,
        warnings,
        filepath,
        ["## Goal", "## Knowledge Sources Used", "## Knowledge Gaps", "## Execution Boundaries", "## Forbidden Assumptions", "## Validation Commands", "## Knowledge Candidate Routing"],
    )
    validate_no_unconfirmed_execution_inputs(errors, filepath)


def validate_spec_file(errors, warnings, filepath):
    validate_file(
        errors,
        warnings,
        filepath,
        ["Knowledge Sources Used", "Decision Ledger", "Business Invariants / 业务不变量", "Acceptance Criteria / 验收标准", "追溯关系矩阵"],
    )
    if not filepath.exists():
        return
    text = read_text(filepath)
    if re.search(r"Status:\s*Draft", text, re.IGNORECASE):
        errors.append(f"{filepath} 仍是 Draft，进入 plan/apply 前必须明确 Confirmed")
    validate_no_unconfirmed_execution_inputs(errors, filepath)
    validate_spec_trace(errors, filepath)


def validate_design_file(errors, warnings, filepath):
    validate_file(
        errors,
        warnings,
        filepath,
        ["## Knowledge Sources Used", "## Knowledge Gaps", "## Solution Summary", "## Impact Scope", "## REQ/AC to Design Decision Mapping", "## Risks, Rollback, and Migration"],
    )
    validate_no_unconfirmed_execution_inputs(errors, filepath)


def validate_impact_file(errors, warnings, filepath):
    if not filepath.exists():
        errors.append(f"缺少文件: {filepath}")
        return

    text = read_text(filepath)
    validate_no_write_ahead(errors, filepath)
    validate_no_template_placeholders(errors, filepath)
    validate_no_unconfirmed_execution_inputs(errors, filepath)

    english_headings = [
        "## Analysis Snapshot",
        "## Direct Changes Required",
        "## Tests And Regression Strategy",
        "## Evidence Index",
    ]
    legacy_headings = [
        "## 0. 分析快照",
        "## 4. 必须修改的文件清单",
        "## 8. 测试与回归策略建议",
        "## 10. 待确认业务规则与问题清单",
    ]
    if not (
        has_required_heading_set(text, english_headings)
        or has_required_heading_set(text, legacy_headings)
    ):
        errors.append(f"{filepath} 缺少 Change Impact Gate 必需章节")


def validate_impact_gate(errors, warnings, base):
    impact = base / "impact.md"
    if impact.exists():
        validate_impact_file(errors, warnings, impact)
        return

    project_kind, project_markers, source_count = detect_project_kind()
    if project_kind == "greenfield":
        warnings.append("Greenfield N/A：当前项目没有存量代码线索，impact.md 不作为进入 plan/apply 的必需文件")
        return

    evidence = ", ".join(project_markers) if project_markers else f"source files: {source_count}+"
    errors.append(f"缺少文件: {impact}（{project_kind} 项目需要 impact.md；证据: {evidence}）")


def validate_knowledge_candidates_file(errors, warnings, filepath):
    validate_file(errors, warnings, filepath, ["Knowledge Candidates"], require_content=False)
    if not filepath.exists():
        return

    text = read_text(filepath)
    if "Evidence Needed" not in text or "Promotion Gate" not in text:
        errors.append(f"{filepath} 缺少候选知识证据字段: Evidence Needed / Promotion Gate")

    for line in text.splitlines():
        stripped = line.strip()
        if (
            not stripped.startswith("|")
            or stripped.startswith("|---")
            or stripped.lower().startswith("| candidate |")
        ):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 8:
            errors.append(f"{filepath} 候选知识行缺少字段: {stripped}")
            continue
        candidate, item_type, scope, source, status, target, evidence_needed, promotion_gate = cells[:8]
        required = {
            "Candidate": candidate,
            "Type": item_type,
            "Scope": scope,
            "Source": source,
            "Status": status,
            "Target": target,
            "Evidence Needed": evidence_needed,
            "Promotion Gate": promotion_gate,
        }
        missing = [name for name, value in required.items() if not value or value in {"-", "TBD", "TODO"}]
        if missing:
            errors.append(f"{filepath} 候选知识缺少必填字段 {', '.join(missing)}: {candidate or stripped}")


def cmd_validate(target="current"):
    """校验 current 或某个 change"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
        return

    errors = []
    warnings = []

    validate_file(errors, warnings, SDC_DIR / "constitution.md", [
        "## 1. Governance Priority",
        "## 2. Fact Priority",
        "## 3. Knowledge and Memory Discipline",
        "## 6. Traceability Rules",
        "## 7. Human Confirmation Rules",
        "## 8. No Silent Defaults",
        "## 9. Discovery Gate",
    ])
    validate_knowledge_workspace(errors, warnings)

    if target == "current":
        base = SDC_DIR / "current"
        validate_spec_file(errors, warnings, base / "spec.md")
        validate_file(errors, warnings, base / "plan.md", ["## 设计摘要", "## 测试先行策略", "## 交付清单"])
        validate_file(errors, warnings, base / "tasks.md", ["## Tasks"])
        validate_file(errors, warnings, base / "apply.md", ["## 已完成任务", "## 修改文件", "## 测试结果"])
        validate_context_pack(errors, warnings, base / "context-pack.md")
        validate_knowledge_candidates_file(errors, warnings, base / "knowledge-candidates.md")
        validate_task_trace(errors, base / "tasks.md")
        validate_no_unconfirmed_execution_inputs(errors, base / "tasks.md")
        validate_no_unconfirmed_execution_inputs(errors, base / "apply.md")
    else:
        base = change_path(target)
        if not base.exists():
            errors.append(f"需求迭代不存在: {base}")
        else:
            validate_file(
                errors,
                warnings,
                base / "discovery.md",
                ["## Current Understanding", "## Decision Ledger", "## Open Questions", "## Exit Criteria"],
                require_content=False,
            )
            if validate_discovery_artifact_budget(errors, warnings, base):
                validate_file(errors, warnings, base / "proposal.md", ["## 背景", "## 目标"], require_content=False)
                validate_file(errors, warnings, base / "notes.md", ["# Notes"], require_content=False)
            else:
                validate_impact_gate(errors, warnings, base)
                validate_file(errors, warnings, base / "proposal.md", ["## 背景", "## 目标", "## 初始验收标准"])
                validate_design_file(errors, warnings, base / "design.md")
                validate_file(errors, warnings, base / "tasks.md", ["## 实现任务", "## 验证任务"])
                validate_spec_file(errors, warnings, base / "spec.md")
                validate_context_pack(errors, warnings, base / "context-pack.md")
                validate_knowledge_candidates_file(errors, warnings, base / "knowledge-candidates.md")
                validate_task_trace(errors, base / "tasks.md")
                validate_no_unconfirmed_execution_inputs(errors, base / "tasks.md")
                validate_no_unconfirmed_execution_inputs(errors, base / "notes.md")

    print()
    print_color(HEADER, f"🔍 SDC 校验结果: {target}")
    print("=" * 50)

    if errors:
        print_color(RED, "❌ 必须修复")
        for item in errors:
            print(f"  - {item}")
    else:
        print_color(GREEN, "✅ 必须项通过")

    if warnings:
        print()
        print_color(YELLOW, "⚠️  建议完善")
        for item in warnings:
            print(f"  - {item}")

    print("=" * 50)
    if errors:
        print_color(RED, "结论: 不可归档 / 不建议进入实现")
    elif any("Discovery Gate 仍打开" in item for item in warnings):
        print_color(YELLOW, "结论: Discovery 草稿有效；关闭 Open Questions 后再进入 spec/plan/apply")
    else:
        print_color(GREEN, "结论: 校验通过")
    print()
    return not errors


def collect_change_text(source):
    """Collect change artifact text for lightweight archive heuristics."""
    parts = []
    for name in (
        "discovery.md",
        "proposal.md",
        "spec.md",
        "design.md",
        "impact.md",
        "tasks.md",
        "context-pack.md",
        "knowledge-candidates.md",
        "notes.md",
    ):
        path = source / name
        if path.exists():
            parts.append(read_text(path))
    return "\n".join(parts)


def has_any_pattern(text, patterns):
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def knowledge_compact_rows(source, change_id, spec_status):
    """Build the archive Knowledge Compact Gate table without writing conditional assets."""
    text = collect_change_text(source)
    rows = [
        ("Required", f".sdc/specs/{change_id}.md", "Final confirmed spec", spec_status),
        ("Required", f".sdc/changes/archive/{change_id}/archive.md", "Completed change history and evidence", "Done"),
    ]

    optional_rows = []
    if has_any_pattern(text, [r"Knowledge Gap", r"No Evidence, No Fact", r"No Confirmation, No Execution", r"No Impact, No Brownfield Change", r"禁止假设", r"Forbidden Assumptions"]):
        optional_rows.append((
            "Recommended",
            ".sdc/knowledge/current.md or Stop-Line Report",
            "Change artifacts mention knowledge gaps, evidence rules, or forbidden assumptions; confirm whether durable knowledge gaps remain",
            "Needs confirmation",
        ))

    if has_any_pattern(text, [r"product knowledge", r"business rule", r"\brole\b", r"permission", r"approval", r"workflow", r"user flow", r"non-?goal", r"MVP", r"产品知识", r"业务规则", r"用户角色", r"权限", r"审批", r"流程", r"非目标"]):
        optional_rows.append((
            "Recommended",
            ".sdc/knowledge/product/",
            "Change artifacts contain durable product facts, roles, flows, rules, or product decisions",
            "Needs confirmation",
        ))

    if has_any_pattern(text, [r"technical knowledge", r"\bstack\b", r"framework", r"architecture", r"\bmodule\b", r"data model", r"\bAPI\b", r"integration", r"validation command", r"deploy", r"rollback", r"技术知识", r"技术栈", r"架构", r"模块", r"数据模型", r"接口", r"集成", r"验证命令", r"部署", r"回滚"]):
        optional_rows.append((
            "Recommended",
            ".sdc/knowledge/technical/",
            "Change artifacts contain durable technical facts, architecture, interfaces, operations, or validation knowledge",
            "Needs confirmation",
        ))

    if (source / "knowledge-candidates.md").exists() or has_any_pattern(text, [r"knowledge candidate", r"memory candidate", r"procedure candidate", r"候选知识", r"项目记忆"]):
        optional_rows.append((
            "Recommended",
            ".sdc/memory/ or .sdc/knowledge/",
            "Knowledge candidates exist; confirm which ones become durable knowledge, procedures, or memory",
            "Needs confirmation",
        ))

    if has_any_pattern(text, [r"Decision Ledger", r"决策台账", r"\bConfirmed\b", r"ADR", r"architecture decision"]):
        optional_rows.append((
            "Recommended",
            ".sdc/decisions/",
            "Change artifacts contain decision evidence; confirm whether any decision is long-lived",
            "Needs confirmation",
        ))

    if has_any_pattern(text, [r"\bstandard\b", r"coding rule", r"testing rule", r"architecture rule", r"security rule", r"git rule", r"AI collaboration rule", r"开发规范", r"测试规范", r"架构边界", r"安全规则", r"Git 规则", r"AI 协作规则"]):
        optional_rows.append((
            "Recommended",
            ".sdc/standards/",
            "Change artifacts may contain reusable engineering rules",
            "Needs confirmation",
        ))

    if has_any_pattern(text, [r"\bAGENTS\.md\b", r"\bagent\b", r"\bAI\b", r"guardrail", r"harness", r"护栏"]):
        optional_rows.append((
            "Recommended",
            "AGENTS.md",
            "Change artifacts mention AI execution guardrails or harness rules",
            "Needs confirmation",
        ))

    if has_any_pattern(text, [r"\bbug\b", r"\bdefect\b", r"root cause", r"regression", r"缺陷", r"根因", r"回归"]):
        optional_rows.append((
            "Recommended",
            ".sdc/reports/bug/",
            "Bug or regression evidence may deserve durable root-cause record",
            "Needs confirmation",
        ))

    if (source / "impact.md").exists():
        optional_rows.append((
            "Recommended",
            ".sdc/reports/impact/",
            "impact.md exists; preserve final Brownfield/Legacy impact evidence if applicable",
            "Needs confirmation",
        ))

    if has_any_pattern(text, [r"stack", r"framework", r"validation command", r"deploy", r"constraint", r"技术栈", r"验证命令", r"部署", r"长期约束"]):
        optional_rows.append((
            "Recommended",
            ".sdc/project.md",
            "Project context, stack, validation, deployment, or constraints may have changed",
            "Needs confirmation",
        ))

    if has_any_pattern(text, [r"entry ?point", r"module", r"data model", r"public contract", r"integration", r"仓库结构", r"核心模块", r"数据模型", r"公共契约", r"集成"]):
        optional_rows.append((
            "Recommended",
            ".sdc/project-cognition.md",
            "Repository-level cognition may need refresh if structural contracts changed",
            "Needs confirmation",
        ))

    if optional_rows:
        rows.extend(optional_rows)
    else:
        rows.append((
            "N/A",
            "Conditional memory updates",
            "CLI did not detect durable product knowledge, technical knowledge, memory, decision, standard, report, project, or cognition evidence",
            "N/A",
        ))

    return rows


def format_knowledge_compact_table(rows):
    lines = [
        "| Action | Target | Reason | Status |",
        "| --- | --- | --- | --- |",
    ]
    for action, target, reason, status in rows:
        lines.append(f"| {action} | `{target}` | {reason} | {status} |")
    return "\n".join(lines)


def cmd_archive(change_id):
    """归档完成的需求迭代"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
        return False

    source = change_path(change_id)
    if not source.exists():
        print_color(RED, f"❌ 需求迭代不存在: {source}")
        return False

    if not cmd_validate(change_id):
        print_color(RED, "❌ 归档前校验未通过，已停止归档")
        return False

    spec = source / "spec.md"
    if not spec.exists():
        print_color(RED, f"❌ 缺少 spec.md，不能归档: {spec}")
        return False
    if not has_real_content(spec):
        print_color(RED, f"❌ spec.md 仍是模板或缺少有效内容，不能归档: {spec}")
        return False

    trace_errors = []
    validate_spec_trace(trace_errors, spec)
    if trace_errors:
        print_color(RED, "❌ spec.md 追溯链不完整，不能归档")
        for item in trace_errors:
            print(f"  - {item}")
        return False

    tasks = source / "tasks.md"
    if not tasks.exists():
        print_color(RED, f"❌ 缺少 tasks.md，不能归档: {tasks}")
        return False

    tasks_text = read_text(tasks)
    if re.search(r"^\s*-\s+\[\s\]", tasks_text, re.MULTILINE):
        print_color(RED, f"❌ tasks.md 仍有未完成任务，不能归档: {tasks}")
        return False
    if "- [x]" not in tasks_text and "- [X]" not in tasks_text:
        print_color(RED, f"❌ tasks.md 中没有已完成任务，不能归档: {tasks}")
        return False
    trace_errors = []
    validate_task_trace(trace_errors, tasks)
    if trace_errors:
        print_color(RED, "❌ tasks.md 追溯链不完整，不能归档")
        for item in trace_errors:
            print(f"  - {item}")
        return False

    specs_dir = SDC_DIR / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    target = specs_dir / f"{change_id}.md"
    archived_dir = archive_change_path(change_id)

    if target.exists():
        print_color(RED, f"❌ 稳定规范已存在，未覆盖也不归档: {target}")
        return False
    if archived_dir.exists():
        print_color(RED, f"❌ 归档目录已存在，不能重复归档: {archived_dir}")
        return False

    target.write_text(f"# Archived Spec: {change_id}\n\n" + spec.read_text())
    spec_status = "Done"
    compact_table = format_knowledge_compact_table(knowledge_compact_rows(source, change_id, spec_status))

    archive_file = source / "archive.md"
    if not archive_file.exists():
        archive_file.write_text(f"""# Archive

> Change: {change_id}
> Archived: {datetime.now().isoformat()}

## 归档结果

- 稳定规范: `../../../specs/{change_id}.md`
- 归档目录: `.sdc/changes/archive/{change_id}/`
- 原 active 目录: `.sdc/changes/active/{change_id}/`

## 交付结论

（填写可以交付 / 已上线 / 已废弃）

## 追溯摘要

- REQ/AC/T### 覆盖：
- 验证证据：
- 遗留项：

## Knowledge Compact Gate

{compact_table}

> CLI will not write conditional durable knowledge or memory updates. Confirm optional updates in an AI client or edit the target files intentionally.
""")
    elif "Knowledge Compact Gate" not in read_text(archive_file):
        with archive_file.open("a") as file:
            file.write(f"""

## Knowledge Compact Gate

{compact_table}

> CLI will not write conditional durable knowledge or memory updates. Confirm optional updates in an AI client or edit the target files intentionally.
""")

    final_archive_file = archive_file
    moved_to = None
    if source != archived_dir and source.exists() and not archived_dir.exists():
        archived_dir.parent.mkdir(parents=True, exist_ok=True)
        source.rename(archived_dir)
        final_archive_file = archived_dir / "archive.md"
        moved_to = archived_dir

    print_color(GREEN, "✅ SDC 需求迭代已归档")
    print(f"   Change: {change_id}")
    print(f"   Spec: {target.absolute()}")
    print(f"   Archive: {final_archive_file.absolute()}")
    print("   Knowledge Compact Gate: see archive.md; optional durable knowledge/memory updates need confirmation")
    if moved_to:
        print(f"   Moved: {moved_to.absolute()}")
    return True


def cmd_check(target="current"):
    """综合检查入口：CLI 层先执行结构校验，并提示后续人工/AI 检查。"""
    ok = cmd_validate(target)
    print_color(HEADER, "🔎 后续检查")
    print("  - delivery: validate + review + test + quality")
    print("  - bug: 只分析根因和证据，不直接改代码")
    print("  - impact: 分析影响范围、测试矩阵和回滚方案")
    print("  - repo: 分析存量项目结构、风险和 SDC 资产建议")
    print("  - AI 中可直接使用: /sdc:check")
    print()
    return ok


def cmd_edit(name):
    """编辑某个文档"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
        return

    filepath = SDC_DIR / FILES[name]
    if not filepath.exists():
        from datetime import datetime
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(TEMPLATE.format(name=name.capitalize(), time=datetime.now().isoformat()))
    
    # 用系统默认编辑器打开
    editor = os.environ.get("EDITOR", "nano")
    subprocess.run([editor, str(filepath)])
    
    print_color(GREEN, f"✅ {name}.md 已更新")


def cmd_status():
    """查看项目状态"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 未初始化，请先运行: sdc init")
        return

    print()
    print_color(HEADER, "📋 SDC 项目状态")
    print("=" * 50)
    
    done_count = 0
    for name, filename in FILES.items():
        filepath = SDC_DIR / filename
        status = GREEN + "✅" if filepath.exists() and filepath.stat().st_size > 100 else YELLOW + "⬜"
        size = filepath.stat().st_size if filepath.exists() else 0
        if size > 100:
            done_count += 1
        print(f"  {status} {name:<12} {ENDC} {size:>5} 字节")
    
    print("=" * 50)
    progress = int(done_count / len(FILES) * 100)
    print(f"  进度: {progress}% ({done_count}/{len(FILES)})")
    print()

    print_color(HEADER, "📂 标准目录")
    for dirname in DIRS:
        directory = SDC_DIR / dirname
        status = GREEN + "✅" if directory.exists() else RED + "❌"
        print(f"  {status} {dirname}/ {ENDC}")
    print()


def option_value(args, option_name):
    if option_name not in args:
        return None
    index = args.index(option_name)
    if index + 1 >= len(args) or args[index + 1].startswith("--"):
        print_color(RED, f"❌ {option_name} 需要一个参数")
        sys.exit(1)
    return args[index + 1]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "init":
        args = sys.argv[2:]
        standards_source = option_value(args, "--standards")
        standards_name = option_value(args, "--standards-name") or "company"
        cmd_init(standards_source=standards_source, standards_name=standards_name)
    elif cmd == "standards":
        if len(sys.argv) < 4 or sys.argv[2] != "import":
            print_color(RED, "❌ 用法: sdc standards import <path> [--name company]")
            return
        args = sys.argv[3:]
        source_path = args[0]
        pack_name = option_value(args[1:], "--name") or "company"
        if not cmd_import_standards(source_path, pack_name):
            sys.exit(1)
    elif cmd == "change":
        if len(sys.argv) < 3:
            print_color(RED, "❌ 用法: sdc change <short-name> [--confirmed-intake]")
            return
        cmd_change(sys.argv[2], confirmed_intake="--confirmed-intake" in sys.argv[3:])
    elif cmd == "validate":
        target = sys.argv[2] if len(sys.argv) >= 3 else "current"
        if not cmd_validate(target):
            sys.exit(1)
    elif cmd == "archive":
        if len(sys.argv) < 3:
            print_color(RED, "❌ 用法: sdc archive <change-id>")
            return
        if not cmd_archive(sys.argv[2]):
            sys.exit(1)
    elif cmd == "apply":
        cmd_edit("apply")
    elif cmd == "check":
        target = sys.argv[2] if len(sys.argv) >= 3 else "current"
        if not cmd_check(target):
            sys.exit(1)
    elif cmd == "spec":
        cmd_edit("spec")
    elif cmd == "discovery":
        cmd_edit("discovery")
    elif cmd == "plan":
        cmd_edit("plan")
    elif cmd == "tasks":
        cmd_edit("tasks")
    elif cmd == "implement":
        cmd_edit("implement")
    elif cmd == "review":
        cmd_edit("review")
    elif cmd == "test":
        cmd_edit("test")
    elif cmd == "quality":
        cmd_edit("quality")
    elif cmd == "harness":
        # 特殊处理：在项目根目录生成 AGENTS.md
        if not SDC_DIR.exists():
            print_color(RED, "❌ 请先运行: sdc init")
            return
        
        agents_file = Path("AGENTS.md")
        if not agents_file.exists():
            from datetime import datetime
            with open(agents_file, "w") as f:
                f.write(f"""# 🤖 AGENTS.md - 本项目 AI 助手必须遵守的规则

> 本文件是项目级执行护栏。最高治理文件是 `.sdc/constitution.md`。
> 所有 AI 助手必须阅读并严格遵守。
> 创建时间：{datetime.now().isoformat()}

---

## 0. 裁决链

| 类型 | 优先级 |
|------|--------|
| 治理规则 | `.sdc/constitution.md` > `AGENTS.md` > 对话即时要求 |
| 事实来源 | `discovery.md` > `spec.md` > `impact.md` > `design.md/plan.md` > `tasks.md` > code |
| 知识来源 | `.sdc/knowledge/` confirmed facts > `.sdc/memory/` candidates |

如果发现冲突，必须停止执行并输出 Stop-Line Report。

---

## 1. 人类确认规则

- AI 可以提出候选方案，但不得自主决定高影响事项
- 高影响事项包括产品规则、权限、状态机、审批、提醒、技术栈、架构、数据模型、认证、安全策略
- 未经用户确认、权威文档支持或显式授权，不得把候选方案写成 REQ/AC/INV/design/tasks
- 所有 AI 默认值必须进入 Decision Ledger，状态为 Proposed 或 Assumed
- Proposed、Assumed、TBD、Conflict 不可进入 apply
- 需求不确定时必须先进入 Discovery Gate，Open Questions 未闭合时只维护 discovery / Draft proposal / notes
- 禁止“如果不对告诉我，我先改”；必须先 ask yes/no 或选项确认，再写入持久文件
- 非平凡需求必须先读 `.sdc/knowledge/index.md`，并在 spec/design/context-pack 记录用到的知识来源
- `.sdc/memory/` 只能帮助召回，不能把 Candidate/Assumed 当作 Confirmed fact
- 遗留项目必须先维护 `.sdc/project-cognition.md`
- 遗留项目在需求确认后、plan/apply 前必须读取当前 change 的 `impact.md`

---

## ✅ 这个项目必须做

| 规则 | 验证方式 |
|------|---------|
| (请在 AI 助手中运行 /sdc:harness 自动生成) | |

---

## ❌ 这个项目绝对不要做

| 禁止事项 | 原因 |
|---------|------|
| (请在 AI 助手中运行 /sdc:harness 自动生成) | |

---

## 🔍 验证命令

| 操作 | 命令 |
|------|------|
| (请在 AI 助手中运行 /sdc:harness 自动生成) | |

---

## 💀 历史上犯过的错误（不要再踩）

| 错误 | 发生时间 | 正确做法 |
|------|---------|---------|
| | | |

---

## 📝 更新记录

每次 AI 犯了一个新类型的错误，就立即追加到上面。
目标：同一个错误，永远不发生第二次。
""")
            print_color(GREEN, "✅ AGENTS.md 已创建")
        else:
            print_color(YELLOW, "⚠️  AGENTS.md 已存在")
        
        # 打开文件编辑
        editor = os.environ.get("EDITOR", "nano")
        subprocess.run([editor, str(agents_file)])
        
        print_color(GREEN, "✅ Harness 已更新")
    elif cmd == "status":
        cmd_status()
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
