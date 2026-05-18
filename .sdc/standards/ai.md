# AI Collaboration Standard

## 必须做

- 开始新需求前确认 `.sdc/` 是否存在
- 先读 `.sdc/constitution.md`，再读 `AGENTS.md`
- 新需求进入 `.sdc/changes/active/`
- 遗留项目先读 `.sdc/project-cognition.md`
- 实现前先看 `discovery.md`、`proposal.md`、`spec.md`、`impact.md`、`design.md`、`tasks.md`
- 保持 `SCN-* -> REQ-* -> AC-* -> T### -> 验证证据` 追溯链
- 完成前执行 `/sdc:check`
- 归档时执行 `/sdc:archive`

## 绝对不要做

- 不要跳过需求记录直接改代码
- 不要把模板内容当作有效规范
- 不要在 spec/design/tasks/code 冲突时继续猜测
- 不要在需求不确定时跳过 Discovery Gate
- 不要在遗留项目需求确认后跳过 Change Impact Gate
- 不要覆盖用户编写的 `.sdc/` 文件；SDC 托管模板升级必须保留备份
- 不要删除 change 历史
- 不要忽略 `.sdc/standards/` 中的项目规范
