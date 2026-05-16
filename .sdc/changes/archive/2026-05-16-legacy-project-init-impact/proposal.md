# 2026-05-16-legacy-project-init-impact Proposal

## 背景

SDC 当前已经有 repo/brownfield 和 impact 模式，但遗留项目流程边界还不够自然。用户修正了关键时机：遗留项目变更影响面分析不应该在 init 时执行，因为 init 还没有具体需求；它应该在 change 中需求已经确定之后、进入 plan/apply 之前执行。

## 目标

- `init` 能区分新项目和存量/遗留项目；对遗留项目，生成项目整体认知资产和 repo-analysis 提示，而不是生成具体需求影响分析。
- `change` 在需求确定后，如果项目是遗留项目，必须触发 change impact gate，产出当前 change 的影响面分析。
- `plan/apply/check/review` 对遗留项目必须读取并复核该影响分析，最终给出老系统改造点与影响点。
- 吸收 SDDInAction 中 repo-analysis 和 change-impact-analysis 的提示词原则：证据优先、先找入口、沿调用链收敛、区分已确认事实/合理推断/待确认问题。

## 非目标

- 不新增公开 slash command。
- 不在 init 阶段为不存在的具体需求生成影响分析。
- 不要求新项目填写遗留影响分析。

## 初始场景

- SCN-01: 用户在遗留项目中执行 init，需要得到项目整体认知入口。
- SCN-02: 用户在遗留项目中创建并确认一个 change，需要在 plan 前做变更影响面分析。
- SCN-03: 用户在遗留项目中完成实现并进入 review/check，需要看到本次需求对老系统的实际改造点和影响点。

## 初始需求

- REQ-01: init legacy cognition
- REQ-02: change impact gate after confirmed requirement
- REQ-03: final legacy impact review

## 初始验收标准

- AC-01: init 生成项目整体认知模板，并说明遗留项目先做 repo/brownfield 认知。
- AC-02: change 需求确认后，遗留项目必须在 plan/apply 前产出 `impact.md`。
- AC-03: review/check 遗留项目时必须输出老系统改造点与影响点分析。

## 任务清单

见 `tasks.md`。

## 风险和回滚

- 风险：新增模板可能让流程看起来变重。
- 缓解：保持公共指令不变，所有 legacy 能力都作为 init/change/check/review 的内部门禁。
- 回滚：恢复模板与技能文档即可，不涉及运行时服务。
