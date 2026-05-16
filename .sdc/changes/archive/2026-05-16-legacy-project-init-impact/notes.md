# Notes

> Change: 2026-05-16-legacy-project-init-impact
> Created: 2026-05-16T11:37:09.397235

## 实现记录

- 已按用户修正重新调整设计：init 只做项目整体认知，具体遗留项目变更影响面分析在 change 需求确认后触发。
- 已新增 `.sdc/project-cognition.md` 和 `.sdc/templates/project-cognition.md`。
- 已更新 `sdc-cli.py`：init 会提示 Greenfield/Brownfield 路径，change 会生成 `impact.md`。
- 已更新 `skills/sdc-init`、`sdc-change`、`sdc-plan`、`sdc-apply`、`sdc-review`、`sdc-check`、`sdc-validate`、`sdc-core`、`sdc-harness`。
- 已更新 README、docs、changelog、package/plugin metadata，版本提升到 1.1.3。

## 问题记录

- 中途根据用户反馈修正了方案：不再将具体需求影响分析放在 init 阶段。
- 无阻塞问题。

## 验证记录

- PASS `python3 -m py_compile sdc-cli.py`
- PASS `python3 sdc-cli.py validate 2026-05-16-legacy-project-init-impact`
- PASS JSON parse: `package.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`
- PASS `node --check bin/install.js`
- PASS 临时目录流程：`sdc init` 生成 `project-cognition.md` 和 `templates/project-cognition.md`，`sdc change demo` 生成 `impact.md`
- PASS `python3 sdc-cli.py check 2026-05-16-legacy-project-init-impact`
- PASS `claude plugin validate .`
- PASS `npm pack --dry-run`
