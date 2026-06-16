# Project Memory

Memory 存放经验、候选知识和过程性记忆。它帮助未来 agent 少重复探索，但不能直接成为产品或技术事实。

## 文件

- `candidates.md` - 本次或历史需求中发现的候选知识，等待 archive 确认。
- `procedures.md` - 可复用流程、排障步骤、容易犯错的操作。
- `episodic/` - 重要工作片段、事故或里程碑的简短记录。

长期稳定事实应进入 `knowledge/`、`standards/` 或 `decisions/`，而不是一直留在 memory。
