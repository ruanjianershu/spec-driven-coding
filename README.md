# SDC - Spec-Driven Coding

SDC 是一套本地优先的 AI 编码工作流技能集，用少量入口把需求落地收敛成：

```text
init -> change -> plan -> apply -> check -> archive
```

它的目标不是增加更多命令，而是让 AI 在写代码前先确认需求、读取项目知识、保留追溯链、执行检查，并在完成后沉淀长期知识。

## 核心能力

- 标准 `.sdc/` 工作区：记录需求、规范、任务、决策、知识库和交付证据。
- Mandatory Change Intake Gate：创建 change 前必须先问清项目背景、范围、技术偏好和验收约束。
- Discovery Gate：需求没确认时只保留轻量草稿，不生成完整 spec/design/tasks。
- 知识库与 memory：区分产品知识、技术知识、候选知识和过程记忆。
- Brownfield impact gate：存量项目在需求确认后做当前变更影响面分析。
- 追溯链：`SCN-* -> REQ-* -> AC-* -> T### -> validation evidence`。
- 反乱猜门禁：`No Evidence, No Fact; No Confirmation, No Execution; No Impact, No Brownfield Change`。
- `check` 合并 validate、review、test、quality。
- `archive` 归档完成变更，并通过 Knowledge Compact Gate 判断哪些知识需要沉淀。

## 安装 / 更新

推荐所有机器统一使用：

```bash
npx sdc-spec@latest
```

卸载：

```bash
npx sdc-spec@latest uninstall
```

本地 clone 调试：

```bash
git clone https://github.com/ruanjianershu/spec-driven-coding.git
cd spec-driven-coding
node bin/install.js
```

从 GitHub main 直接安装：

```bash
npx --yes --package github:ruanjianershu/spec-driven-coding#main sdc-spec
```

更新后请重启对应客户端，让 skills / plugins 重新加载。

## 客户端使用

### Claude Code

Claude Code 使用 slash commands：

```text
/sdc:init
/sdc:change login-flow
/sdc:plan
/sdc:apply
/sdc:check
/sdc:archive 2026-06-03-login-flow
/sdc:harness
```

Claude 插件只把公共工作流暴露为 slash commands；高级能力如 `sdc-spec`、`sdc-review`、`sdc-test`、`sdc-quality`、`sdc-validate` 仍作为 skills 存在，避免重复入口。

### Codex

Codex 当前应把 SDC 当作 skill plugin 使用，不依赖 `/sdc:*` slash commands。

安装后重启 Codex CLI / Codex App，可通过自然语言触发：

```text
用 SDC 初始化这个项目
用 SDC 创建一个登录需求变更
用 SDC plan 生成实现计划
用 SDC apply 执行当前任务
用 SDC check 检查是否可以交付
用 SDC archive 归档这个变更
```

如果支持 `/skills`，可以选择：

```text
sdc:sdc-init
sdc:sdc-change
sdc:sdc-plan
sdc:sdc-apply
sdc:sdc-check
sdc:sdc-archive
sdc:sdc-harness
```

旧版 Codex 如果只能扫描直装 skills，可临时使用：

```bash
SDC_CODEX_DIRECT_SKILLS=1 npx sdc-spec@latest
```

新版 Codex 不建议这样做，避免 plugin skills 和直装 skills 重复。

### Hermes Agent

安装器会同步 `sdc` / `sdc-*` skills 到 Hermes skills 目录。重启或重新加载 Hermes 后使用。

## 工作流

```text
1. init
   创建 .sdc/ 工作区、constitution、standards、knowledge、memory、templates。

2. change
   先完成 intake 问题并等待确认；未确认时只保留 discovery/proposal/notes 草稿。

3. plan
   基于 confirmed spec、必要的 impact.md 和相关知识库生成 design/tasks/context-pack。

4. apply
   按 T### 薄切片执行，记录 notes、验证证据和 knowledge-candidates。

5. check
   综合 validate/review/test/quality，判断是否可以交付或归档。

6. archive
   归档到 .sdc/specs 和 .sdc/changes/archive，并建议需要沉淀的长期知识。
```

## `.sdc/` 工作区

`/sdc:init` 会创建：

```text
.sdc/
├── constitution.md
├── project.md
├── project-cognition.md
├── knowledge/
│   ├── index.md
│   ├── current.md
│   ├── product/
│   └── technical/
├── memory/
│   ├── candidates.md
│   ├── procedures.md
│   └── episodic/
├── current/
├── changes/
│   ├── active/
│   └── archive/
├── specs/
├── standards/
├── decisions/
├── reports/
├── reviews/
└── templates/
```

### Knowledge vs Memory

- `knowledge/` 是 confirmed 项目事实，分为产品知识和技术知识。
- `memory/` 是候选知识、经验和过程记忆，不能直接覆盖 confirmed knowledge。
- 常用入口是 `.sdc/knowledge/product/`、`.sdc/knowledge/technical/` 和每次 plan 生成的 `context-pack.md`。
- 每条长期知识应记录 `Status / Source / Verified At / Verified Against / Scope`。
- 缺证据时写 Knowledge Gap，不允许把推断写成事实。

## 关键规则

- Open Questions 未闭合时，只能生成 Draft，不允许生成 Confirmed spec/design/tasks。
- 禁止“如果不对告诉我，我先改”。必须先问 yes/no 或选项确认。
- 高影响推断必须进入 Decision Ledger，状态为 `Proposed` 或 `Assumed`，不能直接写成事实。
- `Assumed / Proposed / TBD / Conflict / Stale` 不能进入 final spec/design/tasks/context-pack/apply/archive。
- 存量项目的技术事实必须有代码、配置、测试、构建或运行证据。
- `archive` 可以写必需归档资产；更新 knowledge、memory、standards、decisions、AGENTS.md 等长期资产前必须等待用户确认。

## 公开命令

| 命令 | 用途 |
| --- | --- |
| `init` | 创建或修复 `.sdc/` 工作区 |
| `change` | 创建需求迭代并执行 intake/discovery |
| `plan` | 生成 design、tasks、context-pack |
| `apply` | 按任务执行实现并记录证据 |
| `check` | validate + review + test + quality |
| `archive` | 归档完成变更并触发知识沉淀建议 |
| `harness` | 生成或更新项目级 `AGENTS.md` 护栏 |

高级 skills：`sdc-spec`、`sdc-implement`、`sdc-review`、`sdc-test`、`sdc-quality`、`sdc-validate`。

## 开发与发布检查

```bash
npm run audit
npm run eval:sdc
node --check bin/install.js
npm pack --dry-run
```

可选：

```bash
claude plugin validate .
```

## 项目材料

- [CHANGELOG.md](CHANGELOG.md)
- [SECURITY.md](SECURITY.md)
- [PRIVACY.md](PRIVACY.md)
- [docs/sdc-discipline-core.md](docs/sdc-discipline-core.md)
- [docs/release-checklist.md](docs/release-checklist.md)
- [docs/claude-code-marketplace.md](docs/claude-code-marketplace.md)
- [docs/official-submission.md](docs/official-submission.md)

## License

MIT
