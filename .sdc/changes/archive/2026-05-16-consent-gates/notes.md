# Notes

> Change: 2026-05-16-consent-gates
> Created: 2026-05-16

## 实现记录

- 已读取 2026-05-15 SDC 实验日志。
- 已识别主要失效模式：缺少真实头脑风暴、假设进入事实、plan 自主选技术栈、任务过大、constitution 未形成门禁。
- 已创建本次 SDC change。
- 已升级 `sdc-spec`：新增 Brainstorm-first、Decision Ledger、Confirmed-only、Silent Defaults 禁止规则。
- 已升级 `sdc-plan`：新增 Technical Consent Gate、MVP Slice Gate 和 Stop-Line Report 示例。
- 已升级 `sdc-validate` / `sdc-check` / `sdc-apply`：未确认高影响决策不能进入 apply/archive。
- 已升级 `sdc-init` / `sdc-harness` / `sdc-cli.py` / `.sdc/constitution.md`：新增 Human Confirmation 和 No Silent Defaults。
- 已更新 README、discipline docs、marketplace docs、package/plugin metadata，版本提升到 `1.1.1`。

## 问题记录

- 无停线问题。

## 验证记录

- `python3 sdc-cli.py validate 2026-05-16-consent-gates` 通过。
- `python3 sdc-cli.py check 2026-05-16-consent-gates` 通过结构校验。
- `python3 -m py_compile sdc-cli.py` 通过。
- `node --check bin/install.js` 通过。
- JSON manifest 解析检查通过。
- `claude plugin validate .` 通过。
- `npm pack --dry-run` 通过，包版本为 `sdc-spec@1.1.1`。
