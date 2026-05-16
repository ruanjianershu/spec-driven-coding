# Change Impact Analysis

## 0. 分析快照

- 目标仓库/目录：`<repo-root>`
- 变更目标：为所有 SDC skills 增加英文 Role Prompt Contract。
- 分析时间：2026-05-16
- 分支 / Commit / 子模块状态：`main`，存在未提交 legacy 1.1.3 变更。
- 技术生态线索：Markdown skills、Python CLI、Node installer、plugin manifests。
- 可见配置与依赖范围：本次只影响 prompt assets 和 package metadata。
- 本次分析限制：不涉及真实业务运行系统。

## 1. 变更意图与范围概述

- [已确认事实] 强化每个 skill 的角色化 prompt，提升调用时行为稳定性。
- [已确认事实] 不新增运行时功能或外部服务。

## 2. 受影响系统形态与技术栈

- [已确认事实] 受影响文件主要是 `skills/*/SKILL.md` 和 Markdown/docs/JSON metadata。

## 3. 核心调用链路图谱

- [已确认事实] Codex/Claude 加载 skill -> 读取 `SKILL.md` -> Role Prompt Contract 参与行为约束。

## 4. 必须修改的文件清单

| 类别 | 文件/模块/契约 | 为什么需要关注 | 证据 | 关联 REQ/AC |
|------|----------------|----------------|------|-------------|
| 必须修改 | `skills/*/SKILL.md` | 每个 skill 调用都需要 contract | 用户要求 | REQ-01/AC-01 |
| 必须修改 | `README.md`, `CHANGELOG.md`, manifests | 发布说明和版本一致 | package metadata | REQ-03/AC-03 |

## 5. 级联影响与风险雷达

| 风险点 | 影响范围 | 触发原因 | 证据 | 初步应对 |
|--------|----------|----------|------|----------|
| prompt 文件变长 | skill 加载上下文 | 新增英文 contract | `skills/*/SKILL.md` | 保持 contract 短而具体 |

## 6. 契约、数据与配置影响

- [已确认事实] npm bin、CLI commands 和 plugin command maps 不变。

## 7. 安全、权限、中间件与可观测性影响

- [已确认事实] 无安全权限运行时变化。

## 8. 测试与回归策略建议

- 搜索所有 skill contract。
- 运行 SDC validate/check。
- 运行 Python/Node/manifest/Claude/npm 验证。

## 9. 已确认风险与复杂区域

- 无阻塞风险。

## 10. 待确认业务规则与问题清单

| 问题 | 为什么重要 | 影响哪类修改 | 缺少什么信息 |
|------|------------|--------------|--------------|
| 无 | 无 | 无 | 无 |

## 11. 推荐的实施顺序

1. 修改 skill 文件。
2. 修改 docs/metadata。
3. 运行搜索和发布验证。
4. 归档 change。

## 12. 证据索引

- `skills/`
- `README.md`
- `CHANGELOG.md`
- `package.json`
- `.claude-plugin/`
- `.codex-plugin/`
