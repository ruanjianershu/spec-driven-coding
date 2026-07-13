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
- Common Ground：把 AI 的共同认知拆成 `ESTABLISHED / WORKING / OPEN`，OPEN 不能驱动最终方案。
- Expert Routing：吸收专家库思路，但不增加公开命令，由 AI 在 plan/check/archive 内部选择产品、架构、数据、测试、安全等专家视角。
- 知识库与 memory：区分产品知识、技术知识、候选知识和过程记忆。
- Artifact Output Contract：按触发条件强制标准产物，比如流程图、API/数据契约、测试矩阵和上线清单。
- Execution Orchestration：Plan Preflight、任务接口、文件化交接、执行账本、任务级双判定审查和最终整体审查。
- Brownfield impact gate：存量项目在需求确认后做当前变更影响面分析。
- 追溯链：`SCN-* -> REQ-* -> AC-* -> T### -> validation evidence`。
- 反乱猜门禁：`No Evidence, No Fact; No Confirmation, No Execution; No Impact, No Brownfield Change`。
- `check` 合并 validate、review、test、quality。
- `archive` 归档完成变更，并通过 Knowledge Compact Gate 判断哪些知识需要沉淀。

## 安装

推荐使用 npm 安装：

```bash
npx --yes sdc-spec@latest
```

也可以直接安装 GitHub `main`：

```bash
npx --yes --package github:ruanjianershu/spec-driven-coding#main sdc-spec
```

首次从源码安装：

```bash
git clone https://github.com/ruanjianershu/spec-driven-coding.git
cd spec-driven-coding
node bin/install.js
```

卸载：

```bash
npx --yes sdc-spec@latest uninstall
```

## 更新已有 SDC

优先沿用原来的安装来源：

| 原安装方式 | 更新命令 |
|---|---|
| npm | `npx --yes sdc-spec@latest` |
| GitHub `main` | `npx --yes --package github:ruanjianershu/spec-driven-coding#main sdc-spec` |

### 源码安装的版本

如果源码目录跟踪 GitHub 或其他 Git 远程，进入当初 clone 的目录更新。若 `git status --short` 有本地改动，请先自行提交或处理：

```bash
cd /path/to/spec-driven-coding
git status --short
git pull --ff-only
node bin/install.js
```

不同 Git 远程的源码 clone 都使用这组命令，区别只是该目录配置的远程仓库地址。

如果安装来源是正在修改的本地开发分支，不要执行 `git pull`；每次源码变化后重新安装即可：

```bash
cd /path/to/spec-driven-coding
node bin/install.js
```

安装器会替换旧插件 cache、清理旧版重复 skills，并重新生成 Claude Code 与 Codex 各自需要的目录结构；正常更新不需要先卸载。

### 更新客户端和已有项目

1. 完全退出并重新打开 Claude Code、Codex CLI、Codex App 或 Hermes，让新的 plugins / skills 重新加载。
2. 进入每个已有业务项目，执行一次 SDC init，升级该项目的 `.sdc` 托管结构：

Claude Code：

```text
/sdc:init
```

Codex：

```text
选择 sdc:sdc-init，或输入“使用 SDC 升级当前项目”
```

终端或其他客户端：

```bash
sdc-init
```

只更新插件不会自动升级已有项目中的 `.sdc`。再次 init 是幂等操作：只升级未被用户修改的 SDC 托管模板，检测到项目自定义内容时会保留原文件。

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
   创建 .sdc/ 工作区、constitution、common-ground、expert-routing、standards、knowledge、memory、templates。
   如已有团队规范，可同时导入：`sdc init --standards /path/to/spec-rules`。

2. change
   先读 common-ground 和 knowledge，再完成 intake 问题并等待确认；同时识别输入证据和可能需要的标准产物。未确认时只保留 discovery/proposal/notes 草稿。

3. plan
   基于 confirmed spec、必要的 impact.md、相关知识库、expert-routing 和 Artifact Output Contract 生成 design/tasks/context-pack；记录 Global Constraints 并通过 Plan Preflight。

4. apply
   按 T### 薄切片执行。每个任务使用独立 brief、实现报告和 Spec Compliance + Code Quality 审查，并用 runtime 账本支持中断恢复。

5. check
   综合 validate/review/test/quality，检查任务审查证据和最终整体审查，并验证 Common Ground、专家视角、标准产物和知识漂移。

6. archive
   归档到 .sdc/specs 和 .sdc/changes/archive，并建议需要沉淀的长期知识、共同认知和专家路由。
```

## `.sdc/` 工作区

`/sdc:init` 会创建：

```text
.sdc/
├── constitution.md
├── project.md
├── project-cognition.md
├── common-ground.md
├── expert-routing.md
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
│   └── company/      # 可选：公司/团队规范包索引与规则文件
├── decisions/
├── reports/
├── reviews/
├── runtime/          # git-ignored 执行 brief/report/diff/ledger
└── templates/
```

### Knowledge vs Memory

- `common-ground.md` 是共同认知层：`ESTABLISHED` 可作为依据，`WORKING` 只能辅助探索，`OPEN` 必须先问。
- `expert-routing.md` 是内部专家路由：用户不需要选择专家命令，SDC 会按任务选择产品、领域、架构、API、数据、测试、安全、运维等视角。
- `knowledge/` 是 confirmed 项目事实，分为产品知识和技术知识。
- `memory/` 是候选知识、经验和过程记忆，不能直接覆盖 confirmed knowledge。
- 常用入口是 `.sdc/knowledge/product/`、`.sdc/knowledge/technical/` 和每次 plan 生成的 `context-pack.md`。
- 每条长期知识应记录 `Status / Source / Verified At / Verified Against / Scope`。
- 缺证据时写 Knowledge Gap，不允许把推断写成事实。

### Artifact Output Contract

SDC 不新增一堆命令，但会要求每个阶段有清晰输入输出。

- `change` 记录输入证据：PRD、会议纪要、issue、日志、截图、代码证据或用户口述。
- `plan` 按触发条件生成标准产物：流程/状态图、时序/集成图、API 契约、数据/迁移契约、UX 状态、测试矩阵、上线检查清单、AI 参与说明。
- `check` 反向检查：如果实际 diff 触发了 API、数据、部署、流程、UX、测试等风险，但设计或上下文包没有对应产物，会阻断交付。
- 小需求可以写 `N/A + 证据原因`，但 final plan/check 必须有 AC 测试矩阵。

### Execution Orchestration

SDC 1.3 不增加命令，但强化 plan 之后的执行纪律：

- `plan` 写入精确的 Global Constraints，并在执行前完成 Plan Preflight。
- 每个任务必须声明 `Files / Consumes / Produces / Verify / Expected / Review / Evidence / Source`。
- `apply` 把任务 brief、实现报告和 review package 放进 `.sdc/runtime/<change-id>/`，避免重复向主上下文粘贴完整计划和 diff。
- 客户端支持 subagent 时使用独立 implementer/reviewer，但实现任务仍按任务串行；当前任务未完成 review、持久证据和账本更新前不启动下一个实现。
- 每个任务必须分别通过 `Spec Compliance` 和 `Code Quality`，并引用存在的持久 Evidence；`Cannot verify from diff` 必须由协调 agent 用证据闭合。
- 所有任务完成后还要做一次 Final Whole-Change Review，才能通过 check/archive。

### Company Standards Pack

SDC 不内置任何公司私有规范。已有团队规范建议放进业务项目的 `.sdc/standards/company/`，由索引按需读取：

```bash
sdc standards import /path/to/spec-rules
```

AI 应先读 `.sdc/standards/company/README.md`，再按当前任务读取相关规则文件，避免一次性吞掉整包规范。

## 关键规则

- Open Questions 未闭合时，只能生成 Draft，不允许生成 Confirmed spec/design/tasks。
- OPEN Common Ground 不能进入 final spec/design/tasks/context-pack/apply/archive。
- 专家路由只能提出问题、检查和 investigation task，不能替用户确认产品规则、架构、数据模型、权限或发布策略。
- 触发式交付物缺失不能进入交付：流程/状态、集成、API、数据、UX、测试、部署、AI 参与说明必须有对应产物或 `N/A + 证据原因`。
- final plan/check 必须包含 Test Matrix，并能追溯到 AC。
- Global Constraints 必须有有效 `GC-*` 行，并在 design/plan、tasks、context-pack 中保持同一约束和来源。
- Plan Preflight 未同时满足 `Passed + Reviewed Against + closed Findings`，不能进入 apply。
- 已完成任务必须 `Review: Approved`，且 Task Review Evidence 分别记录已批准的 Spec Compliance、Code Quality 和项目内、非 gitignored 的可解析 Evidence；reviewer 必须只读且不能被提示忽略 finding。
- `.sdc/runtime/` 只保存本地执行交接和恢复账本，长期证据仍写入 tasks、notes、reports 和 archive。
- `WORKTREE` review 遇到未跟踪文件必须先停下并 stage/commit，不能生成漏文件的 diff 包。
- `init` 只自动升级指纹未变化或精确匹配已知旧模板的托管文件；检测到用户修改时原样保留。
- 禁止“如果不对告诉我，我先改”。必须先问 yes/no 或选项确认。
- 高影响推断必须进入 Decision Ledger，状态为 `Proposed` 或 `Assumed`，不能直接写成事实。
- `Assumed / Proposed / TBD / Conflict / Stale` 不能进入 final spec/design/tasks/context-pack/apply/archive。
- 存量项目的技术事实必须有代码、配置、测试、构建或运行证据。
- `archive` 可以写必需归档资产；更新 common-ground、expert-routing、knowledge、memory、standards、decisions、AGENTS.md 等长期资产前必须等待用户确认。

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
npm run sync:skills
npm run audit
npm run eval:sdc
npm run package:codex -- --allow-dirty --output /tmp/sdc-codex-plugin.zip
node --check bin/install.js
npm pack --dry-run
```

`package:codex` 生成 rootless、最小化、固定时间戳的 Codex Portal zip 和 SHA-256 文件；正式构建默认拒绝脏工作区，`--allow-dirty` 仅用于本地验证。

可选：

```bash
claude plugin validate "$HOME/.claude/plugins/marketplaces/sdc-local"
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
