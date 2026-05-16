---
name: sdc-harness
description: "Generate AGENTS.md project AI guardrails from project scan and SDC standards to prevent repeated mistakes."
---

# Skill: SDC Harness 生成 /sdc:harness

## 触发条件
当用户输入以下任一内容时，自动触发本技能：
- `/sdc:harness`
- "生成 AI 规则"
- "创建 AGENTS.md"
- "不要再犯同样的错"

## 核心使命
把"这次犯的错"变成"以后永远不会再犯"。
每发现一个 AI 经常踩的坑，就立即把它封死在 Harness 里。

`/sdc:harness` 生成的是执行护栏，不替代 `.sdc/constitution.md` 和 `.sdc/standards/`。

护栏优先级：

```text
.sdc/constitution.md > AGENTS.md > 对话即时要求
```

如果项目还没有 `.sdc/constitution.md`，应先建议或执行 `/sdc:init`，再生成 AGENTS.md。

---

## 执行步骤

### 第一步：项目扫描（自动）
先分析当前项目：
1. `.sdc/constitution.md` 是否存在，治理优先级是什么？
2. `.sdc/standards/` 中已有开发、测试、架构、安全、Git、AI 协作规则是什么？
3. 有什么编程语言？
4. 有什么构建工具？（npm, pip, cargo, make 等）
5. 有什么测试框架？
6. 有什么常见的坑？
7. 已经犯过什么错？（看 `.sdc/history`、`.sdc/reports` 或用户描述）

---

### 第二步：生成 Harness 三件套

#### 1. AGENTS.md（核心）
按照以下精确格式生成：

```markdown
# 🤖 AGENTS.md - 本项目 AI 助手必须遵守的规则

> 本文件是项目级执行护栏。最高治理文件是 `.sdc/constitution.md`。
> 所有 AI 助手必须阅读并严格遵守。

---

## 0. 裁决链

| 类型 | 优先级 |
|------|--------|
| 治理规则 | `.sdc/constitution.md` > `AGENTS.md` > 对话即时要求 |
| 事实来源 | `discovery.md` > `spec.md` > `design.md/plan.md` > `tasks.md` > code |

如果发现冲突，必须停止执行并输出 Stop-Line Report。

## 1. 人类确认规则

- AI 可以提出候选方案，但不得自主决定高影响事项
- 高影响事项包括产品规则、权限、状态机、审批、提醒、技术栈、架构、数据模型、认证、安全策略
- 未经用户确认、权威文档支持或显式授权，不得把候选方案写成 REQ/AC/INV/design/tasks
- 所有 AI 默认值必须进入 Decision Ledger，状态为 Proposed 或 Assumed
- Proposed、Assumed、TBD、Conflict 不可进入 apply
- 需求不确定时必须先进入 Discovery Gate，确认 MVP 后再生成 spec

---

## ✅ 这个项目必须做

| 规则 | 验证方式 |
|------|---------|
| 所有 Python 代码必须兼容 3.9+ | `python --version` |
| 所有函数必须有 docstring | 静态检查 |
| 提交前必须运行黑盒测试 | `make test` |
| 所有配置必须有默认值 | 代码检查 |
...

---

## ❌ 这个项目绝对不要做

| 禁止事项 | 原因 |
|---------|------|
| 不要引入第三方依赖 | 这个项目要求零依赖 |
| 不要写单元测试 | 这个项目只有黑盒测试 |
| 不要改 Makefile | 构建流程已经固定 |
| 不要用 TypeScript | 这是纯 Python 项目 |
...

---

## 🔍 验证命令

| 操作 | 命令 |
|------|------|
| 语法检查 | `python -m py_compile src/*.py` |
| 黑盒测试 | `make test` |
| 代码格式化 | `black src/` |
| 冒烟测试 | `./run.sh --help` |

---

## 📂 项目结构说明

```
项目根目录/
├── src/           # 源代码在这里
├── tests/         # 黑盒测试在这里
├── Makefile       # 构建入口（不要改）
└── AGENTS.md      # 就是本文件
```

---

## 💀 历史上犯过的错误（不要再踩）

| 错误 | 发生时间 | 正确做法 |
|------|---------|---------|
| 尝试运行 `pytest` | 2026-04-27 | 这个项目只有 `make test` |
| 尝试改 Makefile | 2026-04-26 | 构建流程是固定的 |
| 引入了 requests 依赖 | 2026-04-25 | 这个项目要求零依赖 |

---

## 📝 更新记录

本文件应该持续更新。
每次 AI 犯了一个新类型的错误，就立即追加到上面。
目标：同一个错误，永远不发生第二次。
```

---

#### 2. .sdc/harness.sh（可选的验证脚本）
```bash
#!/bin/bash
# SDC Harness - AI 提交前必须运行的验证脚本
# 用法: .sdc/harness.sh

set -e

echo "🔍 Running SDC Harness checks..."

# 检查 1: 没有新增第三方依赖
if grep -q "requests" requirements.txt 2>/dev/null; then
    echo "❌ ERROR: 这个项目不允许用 requests！"
    exit 1
fi

# 检查 2: 所有函数有 docstring
# ...

echo "✅ All checks passed!"
```

---

#### 3. 更新 .sdc/config（技能配置）
告诉所有 SDC 技能："以后先读 AGENTS.md"

如果项目已经有 `.sdc/standards/ai.md`，同步写入：
- `AGENTS.md` 只放执行护栏
- `.sdc/standards/` 保留完整开发规范
- `.sdc/constitution.md` 保留最高裁决规则

---

### 第三步：输出使用说明

```
✅ Harness 已生成！

现在你的项目有了 AI 护栏：

📄 AGENTS.md - 所有 AI 助手必须遵守的规则
    - 告诉 AI"这个项目有什么、没有什么"
    - 告诉 AI"哪些坑已经有人踩过了"
    - 告诉 AI"怎么验证自己做的对不对"

🔧 .sdc/harness.sh - 提交前验证脚本
    - 一键运行所有检查

💡 使用建议：
1. 每次 AI 犯了一个新类型的错误 → 立即更新 AGENTS.md
2. 让 AI 提交代码前先跑 `.sdc/harness.sh`
3. 目标：同一个错误，永远不发生第二次

下次 AI 再想犯同样的错，它会先看到 AGENTS.md 里的规则！
```

---

## 🚦 质量红线（必须严格遵守）

| 序号 | 规则 | 违反后果 |
|------|------|---------|
| 1 | 必须包含"✅ 必须做"和"❌ 绝对不要做" | 输出无效，重做 |
| 2 | 必须包含"验证命令"表格 | 输出无效，重做 |
| 3 | 必须包含"历史错误"部分（即使是空的） | 输出无效，重做 |
| 4 | 必须包含"0. 裁决链" | 输出无效，重做 |
| 5 | 必须包含 Human Confirmation / No Silent Defaults | 输出无效，重做 |
| 6 | 格式必须清晰易读，AI 一眼能看懂 | 输出无效，重做 |

---

## 💡 设计理念

> 不要只是"纠错"，要"封错"。
>
> 纠错是：这一次别再犯。
> 封错是：以后永远都别再犯。
>
> 每发现一个坑，就立即把它写进 AGENTS.md。
> 时间久了，你的项目会变得越来越"AI 友好"。
