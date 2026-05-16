# Notes

> Change: 2026-05-16-discovery-gate
> Created: 2026-05-16

## 实现记录

- 已创建 Discovery Gate change。
- 已将 `/sdc:change` 升级为新需求入口：先判断需求确定性，不确定时进入 Discovery Gate。
- 已将 `/sdc:spec` 升级为消费 `discovery.md`：存在未确认高影响决策时不能生成 Confirmed spec。
- 已更新 `sdc-cli.py`，`init` 会创建 `.sdc/current/discovery.md` 和 `.sdc/templates/discovery.md`，`change` 会为每个 change 创建 `discovery.md`。
- 已修正 CLI 校验边界：`discovery.md` 必须存在并具备结构，但清晰需求的 change 不会因为空 discovery 模板而被阻塞。
- 已更新 README、docs、changelog、package/plugin metadata，版本提升到 1.1.2。

## 问题记录

- 无停线问题。

## 验证记录

- PASS `python3 sdc-cli.py validate 2026-05-16-discovery-gate`
- PASS `python3 sdc-cli.py check 2026-05-16-discovery-gate`
- PASS `python3 -m py_compile sdc-cli.py`
- PASS `node --check bin/install.js`
- PASS JSON parse: `package.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`
- PASS 临时目录流程: `sdc init` 后 `sdc change demo` 可生成 `.sdc/templates/discovery.md` 和 change `discovery.md`
- PASS 临时目录验证边界: `sdc validate 2026-05-16-demo` 不再把空 discovery 模板列为阻塞错误，仅阻塞未完成 tasks 模板
- PASS `claude plugin validate .`
- PASS `npm pack --dry-run`
