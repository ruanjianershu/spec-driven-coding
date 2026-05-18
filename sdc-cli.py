#!/usr/bin/env python3
"""
SDC CLI - 规范驱动开发 薄运行层
功能：自动管理 SDC 项目文档，不用手动复制粘贴

用法：
  sdc init          # 初始化标准 SDC 工作区
  sdc change <name> # 创建一次需求迭代
  sdc validate [target] # 校验 current 或某个 change
  sdc archive <change> # 归档完成的需求迭代
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
    "reports",
    "reports/bug",
    "reports/impact",
    "reports/repo-analysis",
    "reviews",
    "specs",
    "standards",
    "templates",
]

INIT_FILES = {
    "README.md": """# SDC Workspace

这个目录记录项目的规范驱动开发过程。所有需求、计划、实现记录、审查、测试和质量检查都应该沉淀在这里。

## 目录

- `project.md` - 项目长期背景、目标用户、技术约束和验证命令
- `project-cognition.md` - 遗留项目整体认知，基于代码证据建立维护地图
- `constitution.md` - 项目最高工程裁决规则
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
3. `/sdc:spec` 将已确认 discovery 收敛为 SCN/REQ/AC
4. 遗留项目在需求确认后先更新当前 change 的 `impact.md`
5. `/sdc:plan` 生成 design/tasks
6. `/sdc:apply` 执行实现并记录过程
7. `/sdc:check` 综合校验、审查、测试和质量检查
8. `/sdc:archive <name>` 归档到 `changes/archive/`

## 三类核心资产

- `specs/` - 业务规范：项目应该做什么
- `changes/` - 需求迭代：这次为什么改、怎么改、如何验收
- `standards/` - 开发规范：代码、测试、架构、安全、Git 和 AI 协作规则

## SDC v1.1 纪律内核

```text
治理优先级：.sdc/constitution.md > AGENTS.md > 对话即时要求
事实优先级：discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code
追溯链：SCN-* -> REQ-* -> AC-* -> T### -> 验证证据
确认门禁：高影响决策必须 Confirmed，不能 Silent Default
探索门禁：不确定需求必须先 discovery，再 spec
```
""",
    "constitution.md": """# SDC Project Constitution

## 1. Governance Priority

`.sdc/constitution.md > AGENTS.md > conversation instructions`

If these sources conflict, stop and produce a Stop-Line Report.

## 2. Fact Priority

`discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code`

Code is evidence of current behavior, but it does not automatically override the agreed spec.

## 3. Core Chain

`discovery -> spec -> impact -> plan -> tasks -> code -> verify -> archive`

## 4. Stop-The-Line Rules

Stop and produce a Stop-Line Report when:

- spec, design, or tasks are missing, conflicting, or not verifiable
- implementation requires changing business behavior, public contract, acceptance criteria, or key technical decisions
- current task requires scope expansion
- validation cannot prove the acceptance criteria

## 5. Traceability Rules

- specs must define `SCN-*`, `REQ-*`, and `AC-*` identifiers
- tasks must reference `REQ-*` and `AC-*`
- tests or validation notes must reference `AC-*`
- implementation notes must record validation evidence

## 6. Human Confirmation Rules

AI may propose options, but humans own high-impact decisions.

High-impact decisions include product rules, permissions, state machines, approval flows, reminder behavior, technology stack, architecture, data model, authentication, locking, deletion, migration, rollout, and security policy.

Before a high-impact decision enters `REQ-*`, `AC-*`, `INV-*`, `design.md`, or `tasks.md`, it must be one of:

- explicitly confirmed by the user
- supported by an authoritative project document
- explicitly delegated by the user with permission to choose

## 7. No Silent Defaults

Do not turn common practice into project truth.

All AI-created defaults must be recorded in a Decision Ledger as `Proposed` or `Assumed` until confirmed. `Proposed`, `Assumed`, `TBD`, and `Conflict` items must not be treated as implementation-ready.

## 8. Discovery Gate

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

> 当前需求规范。由 `/sdc:spec` 生成或维护。

## 0. 文档元信息

## 1. Decision Ledger / 决策台账

| ID | 决策 | 状态 | 依据来源 | 是否允许进入 REQ/AC | 下一步 |
|----|------|------|----------|----------------------|--------|

## 2. Glossary / 统一语言

## 3. 背景与目标

## 4. 场景与需求

### SCN-01

### REQ-01

## 5. Acceptance Criteria / 验收标准

### AC-01

Given ...
When ...
Then ...

## 6. 验证策略

## 7. 风险、假设与待确认项

## 8. 追溯关系矩阵
""",
    "current/discovery.md": """# Current Discovery

> 需求不确定时先在这里探索。Discovery 不是正式 spec，只有 Confirmed 决策才能进入 REQ/AC。
> Open Questions 未闭合时，只维护 discovery、可选 Draft proposal 和简短 notes，不生成完整 spec/design/tasks。

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
- `notes.md` - 实现过程记录和问题

归档后移动到：

```text
archive/YYYY-MM-DD-short-name/
```
""",
    "specs/README.md": """# Specs

这里存放已经稳定下来的业务规范。不要把临时讨论直接放进来，先在 `current/` 或 `changes/` 中完成迭代。
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

## 与 AGENTS.md 的关系

`.sdc/standards/` 是完整开发规范，适合长期维护。
`AGENTS.md` 是 AI 执行护栏，可以由 `/sdc:harness` 从 standards 中提炼。
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
- 新需求进入 `.sdc/changes/active/`
- 遗留项目先读 `.sdc/project-cognition.md`
- 实现前先看 `discovery.md`、`proposal.md`、`spec.md`、`impact.md`、`design.md`、`tasks.md`
- 保持 `SCN-* -> REQ-* -> AC-* -> T### -> 验证证据` 追溯链
- 完成前执行 `/sdc:check`
- 归档时执行 `/sdc:archive`

## 绝对不要做

- 不要跳过需求记录直接改代码
- 不要把模板内容当作有效规范
- 不要在 spec/design/tasks/code 冲突时继续猜测
- 不要在需求不确定时跳过 Discovery Gate
- 不要在遗留项目需求确认后跳过 Change Impact Gate
- 不要覆盖已有 `.sdc/` 文件
- 不要删除 change 历史
- 不要忽略 `.sdc/standards/` 中的项目规范
""",
    "decisions/README.md": """# Decisions

记录重要技术/产品决策。推荐文件名：

```text
YYYY-MM-DD-short-title.md
```
""",
    "reviews/README.md": """# Reviews

保存 `/sdc:review` 的代码审查结果。
""",
    "reports/README.md": """# Reports

保存 `/sdc:check` 产生的测试、覆盖率、质量检查、bug 分析、impact 分析和 repo-analysis 报告。

## 子目录

- `bug/` - 缺陷分析报告，只分析不直接改代码
- `impact/` - 变更影响面和上线风险分析
- `repo-analysis/` - 存量项目结构、风险和改造建议
""",
    "templates/change.md": """# Change Proposal

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

## 背景

## 方案

## 影响范围

## 不改范围

## 数据和接口变化

## REQ/AC 到设计决策的映射

## 风险

## 回滚方案

## 替代方案
""",
    "templates/spec.md": """# Spec

## 0. 文档元信息

## 1. Decision Ledger / 决策台账

| ID | 决策 | 状态 | 依据来源 | 是否允许进入 REQ/AC | 下一步 |
|----|------|------|----------|----------------------|--------|

## 2. Glossary / 统一语言

## 3. 背景与目标

## 4. 场景与需求

### SCN-01

### REQ-01

## 5. Acceptance Criteria / 验收标准

### AC-01

Given ...
When ...
Then ...

## 6. 验证策略

## 7. 风险、假设与待确认项

## 8. 追溯关系矩阵
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
    "templates/change-impact.md": """# Change Impact Analysis

> 遗留项目在需求确认后的变更影响面分析。它发生在 confirmed spec 之后、plan/apply 之前。

## 0. 分析快照

- 目标仓库/目录：
- 变更目标：
- 分析时间：
- 分支 / Commit / 子模块状态：
- 技术生态线索：
- 可见配置与依赖范围：
- 本次分析限制：

## 1. 变更意图与范围概述

## 2. 受影响系统形态与技术栈

## 3. 核心调用链路图谱

## 4. 必须修改的文件清单

| 类别 | 文件/模块/契约 | 为什么需要关注 | 证据 | 关联 REQ/AC |
|------|----------------|----------------|------|-------------|

## 5. 级联影响与风险雷达

| 风险点 | 影响范围 | 触发原因 | 证据 | 初步应对 |
|--------|----------|----------|------|----------|

## 6. 契约、数据与配置影响

## 7. 安全、权限、中间件与可观测性影响

## 8. 测试与回归策略建议

## 9. 已确认风险与复杂区域

## 10. 待确认业务规则与问题清单

| 问题 | 为什么重要 | 影响哪类修改 | 缺少什么信息 |
|------|------------|--------------|--------------|

## 11. 推荐的实施顺序

## 12. 证据索引
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


def validate_spec_trace(errors, filepath):
    text = read_text(filepath)
    for marker in ("SCN-", "REQ-", "AC-"):
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

    for filename in ("spec.md", "impact.md", "design.md", "tasks.md"):
        filepath = base / filename
        if filepath.exists():
            errors.append(f"Discovery Gate 未退出，但已生成 {filepath}；只允许 discovery.md / Draft proposal.md / notes.md")

    warnings.append("Discovery Gate 仍打开：这是允许的草稿状态，先关闭 Open Questions 再生成 spec/design/tasks")
    return True


def write_if_missing(relative_path, content):
    """Create a workspace file without overwriting user content."""
    filepath = SDC_DIR / relative_path
    if filepath.exists():
        return False

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)
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


def cmd_init():
    """初始化标准 SDC 工作区"""
    created = []
    project_kind, project_markers, source_count = detect_project_kind()

    SDC_DIR.mkdir(exist_ok=True)

    for dirname in DIRS:
        directory = SDC_DIR / dirname
        if not directory.exists():
            directory.mkdir(parents=True)
            created.append(f"{dirname}/")

    for relative_path, content in INIT_FILES.items():
        if write_if_missing(relative_path, content):
            created.append(relative_path)

    if created:
        print_color(GREEN, "✅ SDC 标准工作区已初始化")
        print(f"   目录: {SDC_DIR.absolute()}")
        print()
        print("已创建:")
        for item in created:
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
    print(f"  {BLUE}sdc discovery{ENDC} - 需求不确定时先探索和收敛 MVP")
    print(f"  {BLUE}sdc spec{ENDC}    - 编辑当前需求规范")
    print(f"  {BLUE}sdc plan{ENDC}    - 生成/编辑规范和实现计划")
    print(f"  {BLUE}sdc apply{ENDC}   - 执行当前需求迭代")
    print(f"  {BLUE}sdc change login-flow{ENDC} - 创建一次需求迭代")
    print(f"  {BLUE}sdc status{ENDC}  - 查看工作区状态")


def cmd_change(name):
    """创建一次需求迭代目录，默认只生成轻量 discovery 草稿。"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
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

    for heading in required_headings:
        if heading not in text:
            errors.append(f"{filepath} 缺少章节: {heading}")


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
        "## 5. Traceability Rules",
        "## 6. Human Confirmation Rules",
        "## 7. No Silent Defaults",
        "## 8. Discovery Gate",
    ])

    if target == "current":
        base = SDC_DIR / "current"
        validate_file(errors, warnings, base / "spec.md", ["Decision Ledger", "Acceptance Criteria / 验收标准", "追溯关系矩阵"])
        validate_file(errors, warnings, base / "plan.md", ["## 设计摘要", "## 测试先行策略", "## 交付清单"])
        validate_file(errors, warnings, base / "tasks.md", ["## Tasks"])
        validate_file(errors, warnings, base / "apply.md", ["## 已完成任务", "## 修改文件", "## 测试结果"])
        validate_spec_trace(errors, base / "spec.md")
        validate_task_trace(errors, base / "tasks.md")
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
                validate_file(
                    errors,
                    warnings,
                    base / "impact.md",
                    ["## 0. 分析快照", "## 4. 必须修改的文件清单", "## 8. 测试与回归策略建议", "## 10. 待确认业务规则与问题清单"],
                    require_content=False,
                )
                validate_file(errors, warnings, base / "proposal.md", ["## 背景", "## 目标", "## 初始验收标准"])
                validate_file(errors, warnings, base / "tasks.md", ["## 实现任务", "## 验证任务"])
                validate_file(errors, warnings, base / "spec.md", ["Decision Ledger", "Acceptance Criteria / 验收标准", "追溯关系矩阵"])
                validate_spec_trace(errors, base / "spec.md")
                validate_task_trace(errors, base / "tasks.md")

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


def cmd_archive(change_id):
    """归档完成的需求迭代"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
        return

    source = change_path(change_id)
    if not source.exists():
        print_color(RED, f"❌ 需求迭代不存在: {source}")
        return

    spec = source / "spec.md"
    if not spec.exists():
        print_color(RED, f"❌ 缺少 spec.md，不能归档: {spec}")
        return
    if not has_real_content(spec):
        print_color(RED, f"❌ spec.md 仍是模板或缺少有效内容，不能归档: {spec}")
        return

    trace_errors = []
    validate_spec_trace(trace_errors, spec)
    if trace_errors:
        print_color(RED, "❌ spec.md 追溯链不完整，不能归档")
        for item in trace_errors:
            print(f"  - {item}")
        return

    tasks = source / "tasks.md"
    if tasks.exists():
        tasks_text = read_text(tasks)
        if "- [ ]" in tasks_text and "- [x]" not in tasks_text:
            print_color(RED, f"❌ tasks.md 中没有已完成任务，不能归档: {tasks}")
            return
        trace_errors = []
        validate_task_trace(trace_errors, tasks)
        if trace_errors:
            print_color(RED, "❌ tasks.md 追溯链不完整，不能归档")
            for item in trace_errors:
                print(f"  - {item}")
            return

    specs_dir = SDC_DIR / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    target = specs_dir / f"{change_id}.md"

    if target.exists():
        print_color(YELLOW, f"⚠️  稳定规范已存在，未覆盖: {target}")
    else:
        target.write_text(f"# Archived Spec: {change_id}\n\n" + spec.read_text())

    archive_file = source / "archive.md"
    if not archive_file.exists():
        archive_file.write_text(f"""# Archive

> Change: {change_id}
> Archived: {datetime.now().isoformat()}

## 归档结果

- 稳定规范: `../../specs/{change_id}.md`
- 原始变更目录: `{source}`

## 交付结论

（填写可以交付 / 已上线 / 已废弃）

## 追溯摘要

- REQ/AC/T### 覆盖：
- 验证证据：
- 遗留项：
""")

    print_color(GREEN, "✅ SDC 需求迭代已归档")
    print(f"   Change: {change_id}")
    print(f"   Spec: {target.absolute()}")
    print(f"   Archive: {archive_file.absolute()}")

    archived_dir = archive_change_path(change_id)
    if source != archived_dir and source.exists() and not archived_dir.exists():
        archived_dir.parent.mkdir(parents=True, exist_ok=True)
        source.rename(archived_dir)
        print(f"   Moved: {archived_dir.absolute()}")


def cmd_check(target="current"):
    """综合检查入口：CLI 层先执行结构校验，并提示后续人工/AI 检查。"""
    cmd_validate(target)
    print_color(HEADER, "🔎 后续检查")
    print("  - delivery: validate + review + test + quality")
    print("  - bug: 只分析根因和证据，不直接改代码")
    print("  - impact: 分析影响范围、测试矩阵和回滚方案")
    print("  - repo: 分析存量项目结构、风险和 SDC 资产建议")
    print("  - AI 中可直接使用: /sdc:check")
    print()


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


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
    elif cmd == "change":
        if len(sys.argv) < 3:
            print_color(RED, "❌ 用法: sdc change <short-name>")
            return
        cmd_change(sys.argv[2])
    elif cmd == "validate":
        target = sys.argv[2] if len(sys.argv) >= 3 else "current"
        cmd_validate(target)
    elif cmd == "archive":
        if len(sys.argv) < 3:
            print_color(RED, "❌ 用法: sdc archive <change-id>")
            return
        cmd_archive(sys.argv[2])
    elif cmd == "apply":
        cmd_edit("apply")
    elif cmd == "check":
        target = sys.argv[2] if len(sys.argv) >= 3 else "current"
        cmd_check(target)
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
