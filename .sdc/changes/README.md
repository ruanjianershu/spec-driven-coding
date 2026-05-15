# Changes

每一次需求迭代一个目录，放在 `active/` 下，推荐命名：

```text
active/YYYY-MM-DD-short-name/
```

每个迭代目录建议包含：

- `proposal.md` - 这次为什么要改、改什么、不改什么
- `tasks.md` - 可执行任务清单
- `design.md` - 关键设计和技术取舍
- `spec.md` - 最终沉淀的需求规范
- `notes.md` - 实现过程记录和问题

归档后移动到：

```text
archive/YYYY-MM-DD-short-name/
```
