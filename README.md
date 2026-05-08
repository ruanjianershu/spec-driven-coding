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

### 方式 1：npx 一键安装（推荐 ⭐）
```bash
npx sdc-spec
```

自动检测你安装的 AI 工具（Claude Code / CodeX / Hermes Agent），一键安装到对应目录。

### 方式 2：本地加载
```bash
git clone https://github.com/ruanjianershu/spec-driven-coding.git
cd spec-driven-coding
```

然后在 Claude Code / CodeX 中选择"加载本地插件"，选择这个目录。

### 方式 3：手动复制技能
直接把 `skills/` 目录复制到你的 AI 工具的 skills 目录。

---

### 📌 关于 `/plugin add` 命令

目前 `/plugin add ruanjianershu/spec-driven-coding` 还不能直接使用，因为这需要平台官方 marketplace 收录。

我们正在申请收录，敬请期待！

---

## 📦 普通模式

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
