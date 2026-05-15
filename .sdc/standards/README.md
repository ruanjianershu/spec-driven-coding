# Development Standards

这里存放项目长期开发规范。它回答“这个项目应该怎么写、怎么测、怎么协作”。

建议把这些文件提交到仓库，让人类开发者和 AI 助手共同遵守。

## 文件

- `coding.md` - 代码风格、命名、错误处理、日志、注释规范
- `testing.md` - 测试策略、覆盖率、测试命名、测试数据
- `architecture.md` - 分层、模块边界、依赖方向、扩展方式
- `security.md` - 输入校验、敏感信息、权限、依赖安全
- `git.md` - 分支、提交、PR、变更粒度
- `ai.md` - AI 助手必须遵守的项目规则

## 与 AGENTS.md 的关系

`.sdc/standards/` 是完整开发规范，适合长期维护。
`AGENTS.md` 是 AI 执行护栏，可以由 `/sdc:harness` 从 standards 中提炼。
