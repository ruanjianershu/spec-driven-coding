# Design

## 背景

Discovery Gate 是 change 内部阶段，不是新公开命令。它解决“需求不确定怎么推进”的问题，让 SDC 能先发散再收敛，再进入 confirmed spec。

## 方案

1. 更新 `sdc-change`：加入需求确定性判定和 Discovery Gate 输出。
2. 更新 `sdc-spec`：读取 `discovery.md`，未确认 discovery 不能生成 Confirmed spec。
3. 更新 `sdc-cli.py`：init 模板和 change 目录创建 `discovery.md`。
4. 更新 `.sdc/templates/discovery.md`。
5. 更新 README/docs/changelog/package/plugin metadata 到 v1.1.2。

## 影响范围

- `skills/sdc-change/SKILL.md`
- `skills/sdc-spec/SKILL.md`
- `skills/sdc-core/SKILL.md`
- `sdc-cli.py`
- `.sdc/templates/discovery.md`
- `README.md`
- `docs/sdc-discipline-core.md`
- package/plugin manifests/changelog

## 不改范围

- 不新增公开指令。
- 不接入外部 Superpowers skill。
- 不改变 installer 路径。

## REQ/AC 到设计决策的映射

| REQ | AC | 设计决策 |
|-----|----|----------|
| REQ-01 | AC-01 | change 增加需求确定性判定 |
| REQ-02 | AC-01, AC-02 | change/spec 增加 Discovery Gate 和 discovery.md 消费规则 |
| REQ-03 | AC-03 | CLI 和模板创建 discovery.md |
| REQ-04 | AC-04 | README/docs 解释 change/spec 心智模型 |

## 风险

- Discovery Gate 可能和 Decision Ledger 重叠。处理：Discovery 是阶段，Decision Ledger 是该阶段和 spec 共用的决策表。

## 回滚方案

恢复本次修改，保留 v1.1.1 consent gates。
