# Change Impact Analysis

## 0. 分析快照

- 目标仓库/目录：`<repo-root>`
- 变更目标：升级 SDC 遗留项目流程，将项目整体认知放在 init/repo 阶段，将具体变更影响分析放在 change 需求确认后。
- 分析时间：2026-05-16
- 分支 / Commit / 子模块状态：`main`，本地有当前 active change，未发现子模块需求。
- 技术生态线索：Python CLI、Node installer、Claude/Codex plugin manifests、Markdown skills/docs。
- 可见配置与依赖范围：仓库内可见 package/plugin manifest、CLI、skills、docs、`.sdc`。
- 本次分析限制：本次是 SDC 自身流程升级，不涉及业务运行系统和数据库。

## 1. 变更意图与范围概述

- [已确认事实] 本次变更修正 legacy 分析时机：init 做项目整体认知，change 需求确认后做具体影响面分析。
- [已确认事实] 不新增公开命令，避免 SDC 指令复杂化。

## 2. 受影响系统形态与技术栈

- [已确认事实] 受影响的是 SDC CLI、skills、docs、plugin metadata 和 `.sdc` 模板。

## 3. 核心调用链路图谱

- [已确认事实] `sdc init` -> 创建 `.sdc` 模板 -> 提示 project cognition。
- [已确认事实] `sdc change <name>` -> 创建 change 文件 -> 包含 `impact.md`。
- [已确认事实] AI skill `/sdc:change` -> 需求确认 -> legacy Change Impact Gate -> `/sdc:plan`。

## 4. 必须修改的文件清单

- 必须修改：`sdc-cli.py`，新增 project cognition 和 per-change impact 模板。
- 必须修改：`skills/sdc-init/SKILL.md`，定义 Greenfield/Brownfield init 行为。
- 必须修改：`skills/sdc-change/SKILL.md`、`skills/sdc-plan/SKILL.md`、`skills/sdc-apply/SKILL.md`，定义 Change Impact Gate。
- 必须修改：`skills/sdc-review/SKILL.md`、`skills/sdc-check/SKILL.md`，定义最终 legacy impact review。
- 必须修改：README、docs、metadata、changelog。

## 5. 级联影响与风险雷达

- 风险点 / 影响范围 / 触发原因 / 证据 / 初步应对思路：模板增加可能显得更重 / SDC 用户流程 / 新增 project cognition 和 impact 文件 / `sdc-cli.py` 与 README / 不新增公开命令，仅作为 legacy 内部门禁。

## 6. 契约、数据与配置影响

- [已确认事实] npm bin 和插件入口不变。
- [已确认事实] package/plugin 版本需要提升。

## 7. 安全、权限、中间件与可观测性影响

- [已确认事实] 不涉及网络服务、权限系统或后台进程。

## 8. 测试与回归策略建议

- 运行 `python3 -m py_compile sdc-cli.py`。
- 运行 `node --check bin/install.js`。
- 运行临时目录 `sdc init` 和 `sdc change demo`，确认模板生成。
- 运行 `claude plugin validate .` 和 `npm pack --dry-run`。

## 9. 已确认风险与复杂区域

- 风险点 / 影响范围 / 触发原因 / 证据 / 初步应对思路：legacy 时机定义混乱 / init/change/plan/review 流程 / 用户刚修正需求 / 本 change spec / 明确 init 与 change 职责分离。

## 10. 待确认业务规则与问题清单

- 无阻塞待确认问题。

## 11. 推荐的实施顺序

1. 更新 CLI 模板和 change 文件结构。
2. 更新 init/change/plan/apply/review/check skills。
3. 更新 README/docs/metadata/changelog。
4. 运行验证并归档。

## 12. 证据索引

- `sdc-cli.py`
- `skills/sdc-init/SKILL.md`
- `skills/sdc-change/SKILL.md`
- `skills/sdc-plan/SKILL.md`
- `skills/sdc-review/SKILL.md`
- `skills/sdc-check/SKILL.md`
- `<local-reference>/legacy-repo-analysis.md`
- `<local-reference>/legacy-change-impact-analysis.md`
