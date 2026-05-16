# Design

## 背景

本次改动属于 prompt asset 增强，不涉及运行时服务。核心是让 skill 文件本身携带英文角色化 contract。

## 方案

1. 在所有 `skills/*/SKILL.md` 的核心使命后增加 `## Role Prompt Contract`。
2. 每个 contract 使用统一英文小节：
   - `### Role`
   - `### Operating Contract`
   - `### Evidence Rules`
   - `### Output Contract`
3. 每个 skill 的 Role 和 contract 内容按实际职责定制。
4. README、docs、CHANGELOG、package/plugin metadata 升级到 1.1.4。

## 影响范围

- 所有 `skills/*/SKILL.md`
- README/docs/changelog/package/plugin metadata
- 本次 `.sdc` change 记录

## 不改范围

- 不修改 commands 文件。
- 不新增 CLI 子命令。
- 不改变安装路径。

## 数据和接口变化

- 无运行时接口变化。
- package/plugin version 更新到 1.1.4。

## REQ/AC 到设计决策的映射

| REQ | AC | 设计点 |
|-----|----|--------|
| REQ-01 | AC-01 | 所有 skill 添加 Role Prompt Contract |
| REQ-02 | AC-02 | 统一英文四段结构 |
| REQ-03 | AC-03 | README/metadata/changelog 更新 |

## 风险

- 文件变长：通过短 contract 控制。
- 内容重复：统一标题，正文按 skill 定制。

## 回滚方案

删除新增 `## Role Prompt Contract` 段落，版本号回退。

## 替代方案

- 只更新 README：拒绝，skill 调用时不一定加载。
- 只更新核心 6 个 skill：拒绝，用户问的是每次 skill 调用。
