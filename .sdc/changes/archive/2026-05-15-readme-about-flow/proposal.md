# 2026-05-15-readme-about-flow Proposal

## 背景

SDC v1.1 已补齐裁决链、追溯链、停线报告和 `/sdc:check` 多模式能力。README 和 GitHub About 仍偏向功能清单，需要调整为“少量入口 + 内部强纪律”的定位，并且用真实 SDC 流程记录本次改动。

## 目标

- 让 README 第一屏直接说明 SDC 是什么、适合谁、为什么比单纯 slash command 更可靠。
- 让快速开始和流程示例体现真实 SDC 链路：init -> change/spec/plan -> apply -> check -> archive。
- 让 Codex 和 Claude Code 的差异说明更清楚。
- 让 GitHub About 与 v1.1 追溯链定位一致。
- 通过本次 change 自举验证 SDC 的完整流程。

## 非目标

- 不新增公开指令。
- 不改变安装器行为，除非验证发现 README/About 必须同步的元信息问题。
- 不发布 npm，不提交 git，除非用户明确要求。

## 初始场景

- SCN-01: 新用户打开 README，希望 1 分钟理解 SDC 的核心价值和安装方式。
- SCN-02: Codex 用户安装后不知道为什么没有 `/sdc:init` slash command，需要明确使用方式。
- SCN-03: Marketplace 审核者或 GitHub 访客查看 About，需要快速理解 v1.1 的定位。

## 初始需求

- REQ-01: README 必须把 SDC 定位为“精简入口、内部强纪律”的 spec-driven coding workflow。
- REQ-02: README 必须包含可执行的端到端流程示例，并覆盖 Claude Code 与 Codex 的使用差异。
- REQ-03: About 描述和 topic 必须与 v1.1 的 traceability、SDD、Claude Code、Codex 定位一致。
- REQ-04: 本次改动必须用 `.sdc/changes` 记录，并通过校验、语法检查、插件校验和打包预检。

## 初始验收标准

- AC-01: README 第一屏包含价值定位、流程链路和 v1.1 discipline core。
- AC-02: README 的使用示例能直接展示完整 SDC lifecycle。
- AC-03: Codex section 明确说明 SDC 是 skill plugin，不依赖自定义 slash command。
- AC-04: GitHub About description 包含 traceability 或 SCN/REQ/AC 相关定位，并增加相关 topics。
- AC-05: `python3 -m py_compile sdc-cli.py`、`node --check bin/install.js`、`claude plugin validate .`、`npm pack --dry-run` 通过。

## 任务清单

见 `tasks.md`。

## 风险和回滚

- 风险：README 过长导致新用户找不到重点。缓解：把核心流程放前面，把细节留在后续章节。
- 风险：About 太长或 topics 不被 GitHub 接受。缓解：使用简洁描述并用 `gh repo view` 验证。
- 回滚：恢复 README/About 元信息到上一版本，并保留 `.sdc/` 记录说明原因。
