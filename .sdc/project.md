# Project Context

## 项目目标

SDC 是一个面向 Claude Code 和 Codex 的轻量 Spec-Driven-Coding skill/plugin 集。项目目标是用少量稳定入口覆盖需求澄清、计划、执行、检查和归档，同时用 `.sdc/` 保留长期需求资产和工程纪律。

## 目标用户

- 使用 Claude Code 的开发者：通过 `/sdc:*` slash commands 执行规范驱动开发。
- 使用 Codex CLI/App 的开发者：通过 SDC skills 或自然语言触发同样流程。
- 想要 OpenSpec 核心生命周期但不想引入复杂指令集的团队。
- 想让 AI 编码过程留下可审查证据链的维护者。

## 技术栈

- Node.js installer: `bin/install.js`
- Python thin CLI: `sdc-cli.py`
- Prompt-only skills: `skills/*/SKILL.md`
- Claude plugin manifest: `.claude-plugin/`
- Codex plugin manifest: `.codex-plugin/`
- Documentation: `README.md`, `docs/`

## 约束条件

- 保持 prompt-only、local-first，不引入 MCP server、遥测、后台服务或外部依赖。
- 普通模式保持少量公共入口：init/change/plan/apply/check/archive/harness。
- Codex 中按 skill plugin 使用；不要承诺 Codex 自定义 `/sdc:*` slash commands。
- Claude Code 中使用 namespaced slash commands。
- 所有 SDC 流程资产应保留 `SCN -> REQ -> AC -> T### -> 验证证据` 追溯链。

## 验证命令

| 操作 | 命令 |
|------|------|
| Python 语法检查 | `python3 -m py_compile sdc-cli.py` |
| Node 语法检查 | `node --check bin/install.js` |
| JSON manifest 检查 | `node -e 'for (const f of ["package.json",".claude-plugin/plugin.json",".claude-plugin/marketplace.json",".codex-plugin/plugin.json"]) JSON.parse(require("fs").readFileSync(f,"utf8"))'` |
| Claude 插件校验 | `claude plugin validate .` |
| npm 打包预检 | `npm pack --dry-run` |
| SDC change 校验 | `python3 sdc-cli.py validate <change-id>` |

## AI 工作规则

- 修改功能前先检查 `.sdc/constitution.md` 和相关 change。
- README、plugin metadata、installer 行为必须同步更新，避免用户安装后感知不一致。
- 不提交 `.idea/`、本地缓存、临时打包产物。
- 涉及 GitHub About、npm、marketplace 等外部可见信息时，修改后必须查询验证。
