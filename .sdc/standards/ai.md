# AI Collaboration Standard

## 必须做

- 开始新需求前确认 `.sdc/` 是否存在
- 先读 `.sdc/constitution.md`，再读 `AGENTS.md`
- 非平凡需求先读 `.sdc/knowledge/index.md`，再按任务读取相关产品/技术知识
- 如果 `.sdc/standards/company/README.md` 存在且当前任务涉及代码生成、架构、接口、数据、事务、测试、安全或公司约定，先读该索引，再只读取相关公司规范文件
- 新需求进入 `.sdc/changes/active/`
- 遗留项目先读 `.sdc/project-cognition.md`
- 实现前先看 `discovery.md`、`proposal.md`、`spec.md`、`impact.md`、`design.md`、`tasks.md`、`context-pack.md`
- plan/check 前确认 Artifact Output Contract：触发流程、API、数据、UX、测试、部署或 AI 参与风险时，必须有对应产物或 N/A 证据
- 保持 `SCN-* -> REQ-* -> AC-* -> T### -> 验证证据` 追溯链
- apply/check 过程中把新发现写入 `knowledge-candidates.md`，不要直接污染长期知识库
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
- 不要一次性读取整个 `.sdc/standards/company/`；先读索引，按任务按需加载
- 不要把 `.sdc/memory/` 中的 Candidate/Assumed 当作 confirmed 项目事实
- 不要跳过被触发的标准产物，尤其是 final plan/check 的 Test Matrix
