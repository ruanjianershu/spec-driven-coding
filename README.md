# 🔧 SDC - Spec-Driven Coding for AI Agents

> 用少量入口，把 AI 编码从临场发挥收敛成 `spec -> plan -> tasks -> apply -> check -> archive` 的可追溯闭环。

## ✨ 是什么

SDC 是一套**纯声明式 AI 开发技能集**。它不是把 slash command 做得越多越好，而是用少量稳定入口，让 AI 助手在每次需求迭代中做到：

- 📂 先建立标准 `.sdc/` 工作区，长期记录需求迭代
- 🎭 使用英文 shared references 承载角色契约、门禁规则和工件标准，`SKILL.md` 保持短小清晰
- 🧭 存量/遗留项目先建立项目整体认知，再处理具体变更
- 🧾 像 OpenSpec 一样记录 change、validate、archive 的核心生命周期
- 📐 生成项目专属开发规范，让后续开发有章可循
- 📋 先把需求转成 SCN/REQ/AC，再写代码
- 🗓️ 任务拆成可验证的 T### 薄切片
- 🧪 测试驱动，先写测试再写代码
- 🔍 用 `/sdc:check` 合并 validate、review、test、quality
- ✅ 完成后 archive，沉淀为稳定项目规范

v1.1 的核心不是增加更多指令，而是强化内部纪律：

```text
治理优先级：.sdc/constitution.md > AGENTS.md > 对话即时要求
事实优先级：discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code
追溯链：SCN-* -> REQ-* -> AC-* -> T### -> 验证证据
确认门禁：高影响决策必须 Confirmed，不能 Silent Default
探索门禁：不确定需求必须先 discovery，再 spec
遗留门禁：init 做项目整体认知，change 需求确认后做 impact，再 plan/apply
```

**零服务，零遥测，纯文本技能。** SDC 基于 Superpowers 的轻量 skill-pack 思路，吸收 OpenSpec 的核心需求生命周期，并加入 SDD/Karpathy-style 的“先思考、薄切片、TDD、证据链”工程纪律。

v1.1.4 起，SDC 补充了英文 `Role Prompt Contract`。当前结构会把这些标准规则统一维护在共享 reference 中：

```text
Role -> Operating Contract -> Evidence Rules -> Output Contract
```

这让每个 `SKILL.md` 只保留触发条件、核心使命、执行骨架和需要读取的 reference；复杂规则按需加载，避免把所有上下文一次性塞进 skill。

普通模式只需要记住：

```bash
/sdc:init
/sdc:change 支持用户登录
/sdc:plan
/sdc:apply
/sdc:check
/sdc:archive
```

`/sdc:harness` 可选，用于从 `.sdc/standards/` 生成项目级 `AGENTS.md` 执行护栏。

---

## 🧭 实际工作流

一次标准 SDC 迭代会留下完整证据链：

```text
1. init      创建 .sdc/ 工作区、constitution、standards、templates
2. change    先做 Mandatory Change Intake Gate，用户确认后创建 .sdc/changes/active/<change-id>/
3. discovery intake 后仍有不确定项时，继续发散、比较、收敛 MVP 和 Decision Ledger
4. spec      将 Confirmed discovery 收敛为 SCN -> REQ -> AC
5. impact    遗留项目在需求确认后分析当前 change 的影响面
6. plan      生成 design/tasks，并建立 SCN -> REQ -> AC -> T### 追溯
7. apply     按 T### 薄切片执行，记录 notes 和验证证据
8. check     合并 validate/review/test/quality，并支持 bug/impact/repo 分析模式
9. archive   将完成的 change 沉淀到 .sdc/specs/ 和 archive/
```

Claude Code 用户可以直接使用 slash commands：

```text
/sdc:init
/sdc:change login-flow
/sdc:spec
/sdc:plan
/sdc:apply
/sdc:check
/sdc:archive 2026-05-15-login-flow
```

Codex 用户使用自然语言或 `/skills` 触发同名 SDC skills：

```text
用 SDC 初始化这个项目
用 SDC 为登录流程创建 change；先完成 intake 问题并确认，再创建 change 文件
如果这是遗留项目，用 SDC 在需求确认后做当前 change 的影响面分析
用 SDC 基于已确认 discovery 生成 spec 和 plan
用 SDC apply 执行当前任务
用 SDC check 检查是否可以交付
用 SDC archive 归档这个变更
```

---

## 🚀 快速开始

### 方式 1：通用安装 / 更新（推荐 ⭐）

无论是首次安装还是更新老版本，优先使用这一条：

```bash
npx sdc-spec@latest
```

它会自动检测你安装的 AI 工具（Claude Code / Codex / Hermes Agent），一键安装到对应目录。

安装器会为 Claude Code 注册本地 marketplace 并启用 `sdc@sdc-local` 插件；为 Codex 注册本地 marketplace、启用插件并同步 skills。

> Claude Code 安装后需要完全重启应用，`/sdc:*` slash commands 才会刷新到命令列表。
> SDC 会在 Claude 插件缓存中生成标准 `.claude/skills/` 结构，兼容新版 Claude Code 的 skill 扫描规则。
>
> Codex 当前应把 SDC 当作 **skill plugin** 使用，而不是 slash command plugin。Codex CLI 可以加载 SDC plugin/skills，但当前不支持插件自定义 `/sdc:*` slash commands。

后续更新 SDC 也使用同一个命令：
```bash
npx sdc-spec@latest
```

### 更新命令速查

| 安装来源 | 通用更新命令 | 说明 |
| --- | --- | --- |
| npm / npx（推荐） | `npx sdc-spec@latest` | 首次安装和更新都用这一条。 |
| npm 全局安装 | `npm install -g sdc-spec@latest && sdc` | 已经习惯使用全局 `sdc` 命令的机器用这一条。 |
| GitHub 原生安装 | `npx --yes --package github:ruanjianershu/spec-driven-coding#main sdc-spec` | 不走 npm registry，直接使用 GitHub `main` 分支最新版。 |
| 本地 clone 安装 | `git pull && node bin/install.js` | 在本地克隆的 `spec-driven-coding` 目录里执行。 |
| 手动复制安装 | `npx sdc-spec@latest` | 推荐改用安装器同步，避免漏复制插件、skills 或命令文件。 |

### 各客户端更新后生效方式

| 客户端 | 推荐更新命令 | 更新后操作 | 验证方式 |
| --- | --- | --- | --- |
| Claude Code | `npx sdc-spec@latest` | 完全退出并重新打开 Claude Code。 | 输入 `/sdc:init`、`/sdc:change` 或 `/sdc:check`。 |
| Codex CLI | `npx sdc-spec@latest` | 退出当前 CLI 会话后重新进入。 | 在 skill 列表中看到 `sdc` / `sdc-*`，或直接用自然语言调用 SDC。 |
| Codex App | `npx sdc-spec@latest` | 完全退出并重新打开 Codex App。 | 新会话的 skill 列表中出现 `SDC`、`sdc` 或 `sdc:*`。 |
| Hermes Agent | `npx sdc-spec@latest` | 重启或重新加载 Hermes Agent 会话。 | skill 列表中出现 `sdc` / `sdc-*`。 |

如果某台机器必须从 GitHub 更新，把上表里的更新命令统一替换为：

```bash
npx --yes --package github:ruanjianershu/spec-driven-coding#main sdc-spec
```

如果某台机器使用本地 clone 更新，请在克隆目录里执行：

```bash
git pull && node bin/install.js
```

如果更新后仍显示旧版本，先关闭对应客户端，再重新执行一次推荐更新命令即可。

一键卸载：
```bash
npx sdc-spec@latest uninstall
```

如果你已经全局安装，也可以使用：
```bash
sdc uninstall
```

如果你希望在终端里长期保留 `sdc` 命令，需要全局安装：
```bash
npm install -g sdc-spec@latest
sdc
```

如果你想绕过 npm registry，直接从 GitHub 安装最新代码：
```bash
npx --yes --package github:ruanjianershu/spec-driven-coding#main sdc-spec
```

### 方式 2：本地加载
```bash
git clone https://github.com/ruanjianershu/spec-driven-coding.git
cd spec-driven-coding
```

Claude Code 推荐通过 marketplace 安装：

```bash
claude plugin marketplace add "$(pwd)" --scope user
claude plugin install sdc@sdc-local --scope user
```

Codex 可通过 `npx sdc-spec@latest` 完成本地 marketplace 和 skills 同步。

### 方式 3：手动复制技能
直接把 `skills/` 目录复制到你的 AI 工具的 skills 目录。

---

## Codex 使用方式

SDC 在 Codex 中的定位是 **skill plugin**：

- 不依赖 `/sdc:init` 这类 slash command
- 通过 SDC skills 让 Codex 理解并执行规范驱动开发流程
- 安装器会注册本地 Codex marketplace、启用 `sdc@sdc-local` 插件，并同步 skills 到 Codex 可扫描目录

### Codex CLI

安装：

```bash
npx sdc-spec@latest
```

安装后完全重启 Codex CLI。使用时推荐直接用自然语言触发：

```text
用 sdc init 初始化项目
用 SDC 创建一个登录需求变更
用 SDC plan 生成实现计划
用 SDC apply 执行当前任务
用 SDC check 检查是否可以交付
用 SDC archive 归档这个变更
```

如果你的 Codex CLI 支持 `/skills`，也可以在 `/skills` 中选择 SDC 相关 skills，例如：

```text
sdc:sdc-init
sdc:sdc-change
sdc:sdc-plan
sdc:sdc-apply
sdc:sdc-check
sdc:sdc-archive
```

注意：Codex CLI 当前不会把 SDC 插件中的 `commands/*.md` 注册成 `/sdc:init`、`/sdc:plan` 这类 slash commands。看到 skill 存在、但 `/sdc:init` 不存在，是当前 Codex CLI 的预期行为，不代表 SDC 安装失败。

### Codex App

安装：

```bash
npx sdc-spec@latest
```

然后完全退出并重新打开 Codex App。打开项目后，可以这样使用：

```text
用 SDC 初始化这个项目，创建 .sdc 工作区和开发规范
用 SDC 为“支持用户登录”创建一次 change
如果这是遗留项目，用 SDC 在需求确认后先更新 impact.md
用 SDC 基于当前 change 生成 plan
用 SDC 执行 apply
用 SDC 做 check，给出验证、审查、测试和质量结论
```

在 Codex App 中，SDC 的能力来自已安装的 plugin skills，而不是应用内 slash command。只要当前会话的 skills/plugin 列表中能看到 `SDC` 或 `sdc:*` skills，就表示 Codex 已经可以使用 SDC。

---

### 📌 关于 `/plugin add` 命令

目前 `/plugin install sdc@claude-plugins-official` 还不能直接使用，因为这需要 Claude Code 官方 marketplace 收录。

我们正在申请收录，敬请期待！

如果 SDC 被 Claude Code 官方市场接受，用户将可以直接安装：

```text
/plugin install sdc@claude-plugins-official
```

安装后 reload plugins，即可使用 `/sdc:init`、`/sdc:plan`、`/sdc:check` 等 Claude Code slash commands。

### 官方市场提交准备

SDC 已补齐官方市场审核需要的基础材料：

- [安全说明](SECURITY.md)
- [隐私说明](PRIVACY.md)
- [变更记录](CHANGELOG.md)
- [官方提交说明](docs/official-submission.md)
- [Claude Code 市场说明](docs/claude-code-marketplace.md)
- [发布检查清单](docs/release-checklist.md)

---

## 📦 Claude Code 普通模式

下列 slash commands 适用于 Claude Code。Codex 当前请使用 `/skills` 或自然语言调用同名 SDC skills。

| 命令 | 作用 |
|------|------|
| `/sdc:init` | 创建标准 `.sdc/` 工作区；遗留项目先建立项目整体认知 |
| `/sdc:change <name>` | 创建一次需求迭代；创建文件前必须先完成 Mandatory Change Intake Gate，遗留项目需求确认后进入 Change Impact Gate |
| `/sdc:plan` | 基于已确认 spec 和必要的 impact.md 生成或更新 proposal/spec/design/tasks |
| `/sdc:apply` | 按 tasks 执行当前变更 |
| `/sdc:check` | 综合执行校验、审查、测试和质量检查 |
| `/sdc:archive <change-id>` | 归档需求迭代，沉淀稳定规范 |
| `/sdc:harness` | 生成项目级 AI 规则 |

### 高级指令

如果你需要精确控制某一步，也可以直接使用：

`/sdc`、`/sdc:spec`、`/sdc:implement`、`/sdc:review`、`/sdc:test`、`/sdc:quality`、`/sdc:validate`

---

## 📖 使用示例

### 场景：开发一个 Todo 应用

```bash
/sdc:init
/sdc:change todo-app
/sdc:plan
/sdc:apply
/sdc:check
/sdc:archive 2026-05-15-todo-app
```

执行后，项目里会留下：

```text
.sdc/changes/archive/2026-05-15-todo-app/
.sdc/specs/2026-05-15-todo-app.md
```

普通模式只暴露少量公共入口；详细模式保留 `spec`、`validate`、`review`、`test`、`quality` 等细分能力。

日常心智模型：`change` 是入口，`spec` 是 change 内的规格细化。新项目第一版、后续迭代、Bug 修复都先用 `change`；只有当 change 已存在并且需要补清楚 SCN/REQ/AC 时，才直接用 `spec`。

遗留项目心智模型：`init` 只建立项目整体认知，不分析某个还不存在的需求；具体变更的影响面分析发生在 `change` 需求确认后，写入当前 change 的 `impact.md`，再进入 `plan/apply`。

---

## 🗂️ SDC 工作区

`/sdc:init` 会生成项目长期使用的 SDC 工作区：

```text
.sdc/
├── constitution.md  # 最高工程裁决规则
├── project.md       # 项目背景、技术栈、约束和验证命令
├── project-cognition.md # 遗留项目整体认知，基于代码证据维护
├── current/         # 当前需求快捷工作区
├── changes/         # 需求迭代：这次为什么改、怎么改、如何验收
├── specs/           # 稳定业务规范：项目应该做什么
├── standards/       # 开发规范：代码、测试、架构、安全、Git、AI 协作规则
├── decisions/       # 架构/产品/技术关键决策
├── reviews/         # 审查报告
├── reports/         # bug、impact、repo-analysis 等分析报告
└── templates/       # spec、plan、tasks、project-cognition、impact 等模板
```

其中 `standards/` 是项目专属开发规范：

```text
.sdc/standards/
├── README.md
├── coding.md
├── testing.md
├── architecture.md
├── security.md
├── git.md
└── ai.md
```

`.sdc/standards/` 是完整规范，适合长期维护；`AGENTS.md` 是 AI 执行护栏，可以由 `/sdc:harness` 从 standards 中提炼。

更多 v1.1 纪律内核说明见 [docs/sdc-discipline-core.md](docs/sdc-discipline-core.md)。

---

## 🎯 设计理念

### 1. 规范先行
> 任何模糊的需求，最终都会变成 Bug。

先把需求拆成**可验证**的子任务，每个任务都有明确的验收标准。
不要把一句模糊描述直接交给 AI 去自由发挥。

### 2. 测试驱动
> 没有测试的代码，都是遗留代码。

每个功能先写测试，再写代码。
测试不是负担，是你思考的草稿。

### 3. 质量内建
> 质量不是最后检查出来的，是整个过程做出来的。

每一步都有质量检查，不是到最后才来补。

### 4. 纯声明式
> 最好的代码，是不需要写的代码。

SDC 核心是一组纯文本技能文件，**零运行时代码**。
兼容所有主流 AI 编码工具，没有锁定。

### 5. 工程纪律内建
> 没有证据，就不算完成。

SDC 的公共 Skill 内置四类纪律机制：

| 机制 | 作用 |
|------|------|
| 裁决链 | `.sdc/constitution.md > AGENTS.md`，`discovery > spec > design/plan > tasks > code` |
| 追溯链 | `SCN -> REQ -> AC -> T### -> 验证证据` |
| 探索门禁 | 不确定需求先进入 Discovery Gate，确认 MVP 后再生成 spec |
| 确认门禁 | 高影响产品/技术决策必须进入 Decision Ledger，确认后才能 apply |
| 遗留门禁 | init 建项目整体认知；change 需求确认后做 impact，再 plan/apply |
| 角色契约 | `skills/sdc-shared/role-contracts.md` 统一维护英文 Role Prompt Contract，约束角色、工作方式、证据和输出 |
| 禁止静默默认值 | AI 可以提出 Proposed/Assumed，但不能把默认值写成事实 |
| 停线报告 | 文档、代码、任务或验收冲突时先停线，不猜测推进 |
| 反合理化表 | 对抗 AI “这个很简单不用测”“看起来没问题”等偷懒借口 |
| 红旗警告 | 明确出现哪些迹象必须暂停、修正或阻止归档 |
| 证据门槛 | 要求输出测试、审查、文件路径、检查结论等具体证据 |
| 多视角检查 | `/sdc:check` 同时覆盖 delivery、bug、impact、repo 分析模式 |

---

## 🧩 架构

```
┌─────────────────────────────────────────────┐
│              用户输入命令                     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         技能触发匹配（纯文本）                │
│  ┌───────────────────────────────────────┐ │
│  │ 普通模式：init change plan apply       │ │
│  │          check archive harness         │ │
│  │ 详细模式：spec review test quality...  │ │
│  └───────────────────────────────────────┘ │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         AI 执行（不需要代码）                 │
└─────────────────────────────────────────────┘
```

---

## 📋 每个技能的输出保证

### `/sdc:init` 输出包含
- ✅ 标准 `.sdc/` 工作区结构
- ✅ `.sdc/constitution.md` 最高裁决规则
- ✅ 当前迭代目录 `current/`
- ✅ 长期变更目录 `changes/`
- ✅ 项目背景文件 `project.md`
- ✅ 项目开发规范目录 `standards/`
- ✅ 需求、任务、停线、bug、impact、repo-analysis 模板

### `/sdc:change` 输出包含
- ✅ 独立 change 目录
- ✅ proposal/tasks/design/spec/notes 五件套
- ✅ 明确的 change-id
- ✅ 初始 SCN/REQ/AC 或待确认项
- ✅ 下一步校验建议

### `/sdc:spec` 输出包含
- ✅ Glossary / 统一语言
- ✅ 业务场景 `SCN-*`
- ✅ 需求规则 `REQ-*`
- ✅ 验收标准 `AC-*`
- ✅ 验证策略、风险、假设和待确认项
- ✅ 追溯关系矩阵
- ✅ 明确的下一步建议

### `/sdc:plan` 输出包含
- ✅ 设计摘要和影响范围
- ✅ `SCN/REQ/AC -> T###` 追溯矩阵
- ✅ 按依赖排序的任务列表
- ✅ 每个任务不超过 2 小时
- ✅ 每个任务的 `REQ/AC/Phase/Size/Verify/Source`
- ✅ 测试先行策略
- ✅ 明确的交付清单

### `/sdc:apply` 输出包含
- ✅ 当前 change 和任务
- ✅ 当前任务对应的 `REQ-* / AC-*`
- ✅ 任务执行记录
- ✅ 修改文件
- ✅ 测试结果
- ✅ 更新 `tasks.md` 和 `notes.md`
- ✅ 必要时输出 Stop-Line Report

### `/sdc:implement` 输出包含
- ✅ 每个任务的测试代码
- ✅ 每个任务的实现代码
- ✅ 测试运行结果
- ✅ 覆盖率报告
- ✅ 遇到的问题记录

### `/sdc:review` 输出包含
- ✅ 至少 3 个问题发现
- ✅ 问题具体到文件和行号
- ✅ 每个问题的修复建议
- ✅ 做得好的地方
- ✅ 明确的修复优先级

### `/sdc:test` 输出包含
- ✅ 测试通过率
- ✅ 覆盖率报告
- ✅ 失败测试的详细信息
- ✅ 覆盖率不足的文件
- ✅ 测试改进建议

### `/sdc:quality` 输出包含
- ✅ 全维度检查结果
- ✅ 冒烟测试记录
- ✅ 交付清单确认
- ✅ 明确的"可以交付/不可以交付"结论

### `/sdc:check` 输出包含
- ✅ delivery 模式：validate/review/test/quality 结论
- ✅ bug 模式：根因候选、证据链和修复建议（默认只分析）
- ✅ impact 模式：影响范围、回归风险、测试矩阵和回滚建议
- ✅ repo 模式：存量项目结构、事实证据、风险和 SDC 建议
- ✅ 明确的可以交付/需要修复/仅分析结论

### `/sdc:validate` 输出包含
- ✅ 结构完整性检查
- ✅ `.sdc/constitution.md` 检查
- ✅ SCN/REQ/AC 追溯检查
- ✅ 任务强格式检查
- ✅ 模板占位检查
- ✅ 明确的通过/不通过结论

### `/sdc:archive` 输出包含
- ✅ change 归档记录
- ✅ 稳定规范沉淀到 `specs/`
- ✅ `REQ/AC/T###` 最终覆盖摘要
- ✅ 原始变更历史保留
- ✅ 归档结论和下一步建议

---

## 🚦 质量红线（每个技能都严格遵守）

| 规则 | 违反后果 |
|------|---------|
| 输出必须有明确的结构化格式 | 输出无效，重做 |
| 必须包含具体可执行的步骤 | 输出无效，重做 |
| 必须有明确的下一步建议 | 输出无效，重做 |
| 不能有"你懂的"这种废话 | 输出无效，重做 |
| 不能跳过 `spec -> plan -> tasks -> verify` | 变更不可追溯 |
| 发现裁决链冲突必须停线 | 继续执行会污染规范 |

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/xxx`)
3. 提交你的改动 (`git commit -m 'Add xxx'`)
4. 推送到分支 (`git push origin feature/xxx`)
5. 开启一个 Pull Request

---

## 📄 开源协议

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- 灵感来自 [Superpowers](https://github.com/obra/superpowers) - 168k+ stars 的纯声明式 AI 技能框架
- 借鉴 OpenSpec 的 change / validate / archive 生命周期
- 借鉴 Karpathy-style skills 和本地流程实践中的“先思考、薄切片、TDD、证据链”工程纪律
- 感谢所有贡献者的努力

---

## 💬 反馈

有任何问题或建议，欢迎：
- 提交 [Issue](https://github.com/ruanjianershu/spec-driven-coding/issues)
- 或者在思否上 @我

---

> "编程是思考的过程，不是打字的过程。"
> 
> 思考清楚了，代码自然就出来了。
