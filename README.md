# 🔧 SDC - 规范驱动开发 (Spec-Driven-Coding)

> 一个 `/sdc`，覆盖从需求到交付的完整闭环。

## ✨ 是什么

SDC 是一套**纯声明式 AI 开发技能集**，用一个主入口 `/sdc` 让你的 AI 助手：
- 📂 先建立标准 `.sdc/` 工作区，长期记录需求迭代
- 🧾 像 OpenSpec 一样记录 change、validate、archive 的核心生命周期
- 📐 生成项目专属开发规范，让后续开发有章可循
- 📋 先把需求理清楚，再写代码
- 🗓️ 任务拆到不超过 2 小时，可独立验收
- 🧪 测试驱动，先写测试再写代码
- 🔍 像资深工程师一样审查代码
- ✅ 交付前全维度质量检查

**零代码，零配置，纯文本技能。** 基于 Superpowers 的轻量 skill-pack 思路，吸收 OpenSpec 的核心需求生命周期，但不复制它们的全部技能。

普通模式只需要记住：

```bash
/sdc:init
/sdc:change 支持用户登录
/sdc:plan
/sdc:apply
/sdc:check
/sdc:archive
```

---

## 🚀 快速开始

### 方式 1：npx 一键安装 / 更新（推荐 ⭐）
```bash
npx sdc-spec@latest
```

自动检测你安装的 AI 工具（Claude Code / CodeX / Hermes Agent），一键安装到对应目录。

安装器会为 Claude Code 注册本地 marketplace 并启用 `sdc@sdc-local` 插件；为 Codex 注册本地 marketplace、启用插件并同步 skills。

> Claude Code 安装后需要完全重启应用，`/sdc:*` slash commands 才会刷新到命令列表。
> SDC 会在 Claude 插件缓存中生成标准 `.claude/skills/` 结构，兼容新版 Claude Code 的 skill 扫描规则。
>
> Codex 当前应把 SDC 当作 **skill plugin** 使用，而不是 slash command plugin。Codex CLI 可以加载 SDC plugin/skills，但当前不支持插件自定义 `/sdc:*` slash commands。

后续更新 SDC 也使用同一个命令：
```bash
npx sdc-spec@latest
```

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
npx --package github:ruanjianershu/spec-driven-coding sdc-spec
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
| `/sdc:init` | 创建标准 `.sdc/` 工作区 |
| `/sdc:change <name>` | 创建一次需求迭代 |
| `/sdc:plan` | 生成或更新 proposal/spec/design/tasks |
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
/sdc:plan 做一个 Todo 应用，支持增删改查，有用户登录
/sdc:apply
/sdc:check
/sdc:archive 2026-05-08-todo-app
```

就这么简单。**普通模式 6-7 个公共指令，详细模式保留完整能力。**

---

## 🗂️ SDC 工作区

`/sdc:init` 会生成三类核心资产：

```text
.sdc/
├── specs/       # 业务规范：项目应该做什么
├── changes/     # 需求迭代：这次为什么改、怎么改、如何验收
└── standards/   # 开发规范：代码、测试、架构、安全、Git、AI 协作规则
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

---

## 🎯 设计理念

### 1. 规范先行
> 任何模糊的需求，最终都会变成 Bug。

先把需求拆成**可验证**的子任务，每个任务都有明确的验收标准。
不要相信"我要一个类似微信的东西"这种鬼话。

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
| 反合理化表 | 对抗 AI “这个很简单不用测”“看起来没问题”等偷懒借口 |
| 红旗警告 | 明确出现哪些迹象必须暂停、修正或阻止归档 |
| 证据门槛 | 要求输出测试、审查、文件路径、检查结论等具体证据 |
| 多视角检查 | `/sdc:check` 同时从 reviewer、tester、security 三个视角检查 |

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
- ✅ 当前迭代目录 `current/`
- ✅ 长期变更目录 `changes/`
- ✅ 项目背景文件 `project.md`
- ✅ 项目开发规范目录 `standards/`
- ✅ 需求和决策模板

### `/sdc:change` 输出包含
- ✅ 独立 change 目录
- ✅ proposal/tasks/design/spec/notes 五件套
- ✅ 明确的 change-id
- ✅ 下一步校验建议

### `/sdc:spec` 输出包含
- ✅ 5-10 个可独立验收的子任务
- ✅ 技术选型建议和理由
- ✅ 可量化的验收标准
- ✅ 完整的测试计划
- ✅ 至少 3 个风险评估
- ✅ 明确的下一步建议

### `/sdc:plan` 输出包含
- ✅ 按依赖排序的任务列表
- ✅ 每个任务不超过 2 小时
- ✅ 每个任务的验收标准
- ✅ 测试先行策略
- ✅ 明确的交付清单

### `/sdc:apply` 输出包含
- ✅ 当前 change 和任务
- ✅ 任务执行记录
- ✅ 修改文件
- ✅ 测试结果
- ✅ 更新 `tasks.md` 和 `notes.md`

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
- ✅ `/sdc:validate` 校验结果
- ✅ `/sdc:review` 代码审查结果
- ✅ `/sdc:test` 测试结果
- ✅ `/sdc:quality` 交付质量结论

### `/sdc:validate` 输出包含
- ✅ 结构完整性检查
- ✅ 验收标准检查
- ✅ 任务复选框检查
- ✅ 模板占位检查
- ✅ 明确的通过/不通过结论

### `/sdc:archive` 输出包含
- ✅ change 归档记录
- ✅ 稳定规范沉淀到 `specs/`
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
