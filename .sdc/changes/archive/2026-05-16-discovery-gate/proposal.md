# 2026-05-16 Discovery Gate Proposal

## 背景

用户指出“轻量头脑风暴”不足以处理不确定需求。SDC 不应该依赖 Superpowers 的 brainstorm，但应内置自己的需求探索阶段：当需求不确定时，不能直接进入 spec/plan，而应先发散、收敛、记录决策，再进入 confirmed spec。

## 目标

- 将 `/sdc:change` 升级为需求入口和 Discovery Gate 入口。
- 当需求不确定时，产出 `discovery.md`、Decision Ledger、候选方向、推荐 MVP、open questions，而不是直接写正式 `REQ/AC`。
- 让 `/sdc:spec` 只消费已确认 discovery 结果。
- 更新 CLI 模板、README、docs、版本信息到 v1.1.2。

## 非目标

- 不新增 `/sdc:brainstorm` 公开指令。
- 不依赖外部 Superpowers skill。
- 不要求所有需求都进入 discovery；需求清楚时可以直接进入 spec。

## 初始场景

- SCN-01: 用户只有模糊想法，需要先探索方向。
- SCN-02: 用户不知道该用 change 还是 spec，SDC 应自动判断。
- SCN-03: 用户说“按你的判断”，SDC 可以提出推荐 MVP，但必须等待确认。

## 初始需求

- REQ-01: `/sdc:change` 必须判断需求确定性，确定时进入 spec，不确定时进入 Discovery Gate。
- REQ-02: Discovery Gate 必须产出结构化探索结果，包括当前理解、候选方向、取舍、Decision Ledger、推荐 MVP、open questions。
- REQ-03: `sdc-cli.py` 和 `.sdc/templates` 必须提供 `discovery.md` 模板，change 目录默认包含该文件。
- REQ-04: README/docs 必须说明 change/spec 的选择：日常用 change，spec 是 change 内的规格细化。

## 初始验收标准

- AC-01: `skills/sdc-change/SKILL.md` 明确包含 Discovery Gate 判定、输出和阻塞规则。
- AC-02: `skills/sdc-spec/SKILL.md` 明确要求读取并消费 `discovery.md`，未完成 discovery 不生成 confirmed spec。
- AC-03: `sdc-cli.py` 的 init/change 模板包含 `templates/discovery.md` 和 change 目录的 `discovery.md`。
- AC-04: README/docs/changelog/package/plugin metadata 更新到 v1.1.2。
- AC-05: 基础验证通过。

## 风险和回滚

- 风险：流程显得更重。缓解：Discovery Gate 只在需求不确定时触发。
- 风险：用户误以为必须先 discovery。缓解：README 明确“确定需求可直接 spec/plan”。
