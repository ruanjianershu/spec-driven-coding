# Design

## 背景

SDC v1.1 的核心价值已经从“指令集”升级为“精简入口 + 纪律内核”。README 和 About 应该围绕这个心智组织，而不是继续堆功能点。

## 方案

1. README 第一屏保留一句话定位，但改成更具体的 lifecycle 表达。
2. 增加“实际工作流”小节，作为用户照着跑的主路径。
3. 优化 Codex section，强调 skill plugin 和自然语言触发。
4. 调整设计理念里的过度口语表达，使其更适合 GitHub/marketplace 读者。
5. 用 `gh repo edit` 更新 GitHub About description 和 topics。

## 影响范围

- `README.md`
- `package.json`
- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- GitHub repository About
- `.sdc/changes/active/2026-05-15-readme-about-flow/`

## 不改范围

- 不新增或删除公开命令。
- 不修改安装路径和插件扫描逻辑。
- 不发布 npm 包。

## 数据和接口变化

- 无代码接口变化。
- GitHub repository metadata 会通过 GitHub API 更新。

## REQ/AC 到设计决策的映射

| REQ | AC | 设计决策 |
|-----|----|----------|
| REQ-01 | AC-01 | README 开头增加 workflow/discipline core 定位 |
| REQ-02 | AC-02, AC-03 | 增加实际工作流，整理 Claude/Codex 差异 |
| REQ-03 | AC-04 | 更新 About description/topics |
| REQ-04 | AC-05 | 使用 `.sdc` 记录并执行验证 |

## 风险

- README 改动范围可能与当前未提交 v1.1 变更交织。处理：只顺着 v1.1 已有内容压缩和重排，不回滚既有改动。
- About 更新是外部可见操作。处理：执行后立即查询验证。

## 回滚方案

- GitHub About 可用 `gh repo edit` 恢复上一版 description/topics。
- README 和 metadata 可通过 git diff 定位并回退本次片段。

## 替代方案

- 只改 README 不改 About：会导致 GitHub 第一印象滞后。
- 新增专门 docs 解释流程：信息会被藏太深，不适合新用户。
