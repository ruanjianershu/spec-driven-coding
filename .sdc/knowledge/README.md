# Knowledge Base

这里存放项目长期知识。它不是聊天记录，也不是所有文档的合集，而是人和 AI 都要复用的项目事实。

## 分层

- `index.md` - 短索引。每次 change/plan/apply 前优先读取。
- `product/` - 产品知识：目标用户、领域概念、业务规则、流程和产品决策。
- `technical/` - 技术知识：技术栈、架构、模块、数据/接口、运行、测试和部署。
- `current.md` - 当前项目状态、最近变化和需要下一次接续的上下文。

## 状态

每条长期知识建议标注状态：

- Confirmed - 已确认事实，可以用于 spec/plan/apply。
- Candidate - 候选知识，等待 archive 确认。
- Assumed - 临时假设，不能进入最终实现依据。
- Stale - 可能过期，需要复核。
- Conflict - 与代码、spec、用户确认或其他知识冲突。
- Deprecated - 已废弃，仅保留历史参考。

Memory 可以帮助召回，但不能覆盖 Confirmed knowledge、当前 spec、用户确认或代码证据。

## Knowledge Evidence Contract

每条长期知识至少要有：

- Status: Confirmed / Candidate / Assumed / Stale / Conflict / Deprecated
- Source: user / spec / code / decision / archive / external-doc
- Verified At: YYYY-MM-DD 或 Commit
- Verified Against: 文件路径、spec、decision、测试命令、代码证据或用户确认
- Scope: personal / project / team / enterprise

没有证据的内容只能进入 Knowledge Gap 或 Candidate，不能进入 final spec/design/tasks/context-pack。

```text
No Evidence, No Fact.
No Confirmation, No Execution.
No Impact, No Brownfield Change.
```
