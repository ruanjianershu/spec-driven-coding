---
name: sdc-init
description: "Initialize the standard .sdc workspace with specs, changes, standards, decisions, reports, templates, and project context."
---

# Skill: SDC 工作区初始化 /sdc:init

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `/sdc:init`
- "初始化 SDC"
- "创建 SDC 工作区"
- "生成需求迭代目录"
- "像 openspec 一样初始化"

## 核心使命

在当前项目中创建或修复标准 `.sdc/` 工作区，让需求、计划、实现、审查、测试、质量检查、架构决策和历史迭代成为长期项目资产。

`/sdc:init` 必须区分：

- Greenfield：直接创建标准 `.sdc/`，下一步进入 `/sdc:change`。
- Brownfield/Legacy：创建标准 `.sdc/`，额外维护 `project-cognition.md`，并建议 `/sdc:check repo`。
- Unknown：保守处理为可能存在历史系统，记录不确定性。

注意：具体需求的变更影响面分析不在 init 阶段做，必须在 `/sdc:change` 需求确认后写入当前 change 的 `impact.md`。

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-init`.
- Workspace and templates: `../sdc-shared/artifact-schemas.md`.
- Governance and stop-line rules: `../sdc-shared/workflow-standards.md`.
- Brownfield classification and project cognition: `../sdc-shared/legacy-impact-gate.md`.

## 执行步骤

1. 检查当前目录是否已有 `.sdc/`。
2. 用仓库证据判断 Greenfield / Brownfield-Legacy / Unknown。
3. 创建缺失目录和模板；不得覆盖用户编写的 `.sdc/` 文件。
4. 创建或补齐 `constitution.md`、`project.md`、`project-cognition.md`、`standards/`、`templates/`。
5. 对 SDC 早期版本生成的托管模板，如果明显与当前 schema 漂移，可以安全升级并保留 `.bak-*` 备份。
6. 如果项目已有 `AGENTS.md`，不得覆盖；提醒后续可执行 `/sdc:harness` 同步规则。
7. Brownfield/Legacy 项目只做整体认知，不做具体 change 的 impact。
8. 输出创建/保留/安全升级的文件、项目类型判断证据和下一步建议。

## 必须创建或补齐

参考 `../sdc-shared/artifact-schemas.md` 中的 workspace schema。最低要求：

- `.sdc/constitution.md`
- `.sdc/project.md`
- `.sdc/project-cognition.md`
- `.sdc/current/`
- `.sdc/changes/active/`
- `.sdc/changes/archive/`
- `.sdc/specs/`
- `.sdc/standards/`
- `.sdc/decisions/`
- `.sdc/reviews/`
- `.sdc/reports/`
- `.sdc/templates/`
- `.sdc/.gitignore`

## Brownfield / Legacy 规则

- 使用代码、构建、配置、测试、CI、数据库脚本、运行脚本、接口定义作为主要证据。
- README、注释和历史文档只能作为线索。
- `project-cognition.md` 记录项目整体认知：运行形态、入口、模块、数据、集成、测试、风险、阅读顺序。
- 关键结论尽量标记 `[Confirmed Fact]`、`[Reasoned Inference]`、`[Open Question]`。
- 下一步建议 `/sdc:check repo` 补全代码证据。
- `project-cognition.md` 是长期可复用基座；后续 change 默认读取它并做局部 impact，不应每次重跑完整项目分析。

## 输出格式

```text
✅ SDC 工作区初始化完成
==================================================

## 项目类型判断
- 类型：Greenfield / Brownfield-Legacy / Unknown
- 证据：

## 创建/补齐的目录
- ...

## 创建/保留的文件
- ...

## 注意事项
- ...

## 下一步
👉 ...
```

## 质量红线

- 不能覆盖用户编写的 `.sdc/` 文件。
- SDC 托管模板升级必须保留备份，并只修复明显的历史 schema 漂移。
- 必须创建 `constitution.md`、`project.md`、`project-cognition.md` 和 `standards/`。
- 必须创建 `current/`、`changes/`、`specs/` 和 `templates/`。
- 必须区分项目整体认知和具体需求影响面分析。
- 必须给出下一步命令。
