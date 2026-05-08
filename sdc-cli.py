#!/usr/bin/env python3
"""
SDC CLI - 规范驱动开发 薄运行层
功能：自动管理 SDC 项目文档，不用手动复制粘贴

用法：
  sdc init          # 初始化标准 SDC 工作区
  sdc change <name> # 创建一次需求迭代
  sdc validate [target] # 校验 current 或某个 change
  sdc archive <change> # 归档完成的需求迭代
  sdc spec          # 打开规范文档（你在 Claude 里写完粘贴进来）
  sdc plan          # 打开计划文档
  sdc apply         # 执行/记录当前需求迭代
  sdc implement     # apply 的兼容别名
  sdc check [target] # 综合检查 current 或某个 change
  sdc review        # 打开审查报告
  sdc test          # 打开测试报告
  sdc quality       # 打开质量检查报告
  sdc harness       # 生成/编辑 AGENTS.md 项目级 AI 规则
  sdc status        # 查看项目进度
"""

import os
import re
import sys
import subprocess
from datetime import date, datetime
from pathlib import Path

SDC_DIR = Path(".sdc")
FILES = {
    "spec": "current/spec.md",
    "plan": "current/plan.md",
    "apply": "current/apply.md",
    "implement": "current/apply.md",
    "review": "reviews/current-review.md",
    "test": "reports/current-test.md",
    "quality": "reports/current-quality.md",
    "harness": "harness.md",
}

DIRS = [
    "changes",
    "changes/active",
    "changes/archive",
    "current",
    "decisions",
    "reports",
    "reviews",
    "specs",
    "standards",
    "templates",
]

INIT_FILES = {
    "README.md": """# SDC Workspace

这个目录记录项目的规范驱动开发过程。所有需求、计划、实现记录、审查、测试和质量检查都应该沉淀在这里。

## 目录

- `project.md` - 项目长期背景、目标用户、技术约束和验证命令
- `current/` - 当前正在推进的一次需求迭代
- `changes/active/` - 正在推进的需求变更，每个变更一个子目录
- `changes/archive/` - 已完成归档的需求变更
- `specs/` - 已稳定的业务规范和能力说明
- `standards/` - 项目长期开发规范，约束人和 AI 怎么写代码
- `decisions/` - 架构决策记录
- `reviews/` - 代码审查记录
- `reports/` - 测试、质量和交付报告
- `templates/` - 需求迭代模板

## 推荐流程

1. `/sdc:change <name>` 创建 `changes/active/<name>/`
2. `/sdc:plan` 生成 proposal/spec/design/tasks
3. `/sdc:apply` 执行实现并记录过程
4. `/sdc:check` 综合校验、审查、测试和质量检查
5. `/sdc:archive <name>` 归档到 `changes/archive/`

## 三类核心资产

- `specs/` - 业务规范：项目应该做什么
- `changes/` - 需求迭代：这次为什么改、怎么改、如何验收
- `standards/` - 开发规范：代码、测试、架构、安全、Git 和 AI 协作规则
""",
    "project.md": """# Project Context

## 项目目标

（这个项目长期要解决什么问题？）

## 目标用户

（谁会使用它？核心使用场景是什么？）

## 技术栈

（语言、框架、构建工具、运行环境）

## 约束条件

（性能、安全、兼容性、部署、合规等限制）

## 验证命令

| 操作 | 命令 |
|------|------|
| 安装依赖 | |
| 运行测试 | |
| 构建 | |
| 本地启动 | |

## AI 工作规则

（项目级偏好、禁忌、容易踩坑的地方）
""",
    "current/spec.md": """# Current Spec

> 当前需求规范。由 `/sdc:spec` 生成或维护。

## 需求背景

## 需求分解

## 验收标准

## 测试计划

## 风险评估
""",
    "current/plan.md": """# Current Plan

> 当前实现计划。由 `/sdc:plan` 生成或维护。

## 任务拆解

## 依赖关系

## 测试先行策略

## 交付清单
""",
    "current/apply.md": """# Current Apply Log

> 当前执行记录。由 `/sdc:apply` 持续更新。

## 已完成任务

## 修改文件

## 测试结果

## 遇到的问题
""",
    "changes/README.md": """# Changes

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
""",
    "specs/README.md": """# Specs

这里存放已经稳定下来的业务规范。不要把临时讨论直接放进来，先在 `current/` 或 `changes/` 中完成迭代。
""",
    "standards/README.md": """# Development Standards

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
""",
    "standards/coding.md": """# Coding Standard

## 命名

- 使用项目现有命名风格
- 名称必须表达业务含义，避免无意义缩写

## 函数和模块

- 单个函数只做一件事
- 优先复用项目已有工具和抽象
- 不为未来可能性提前设计复杂抽象

## 错误处理

- 不吞异常
- 错误信息必须能指导定位问题
- 用户可见错误和内部错误要区分

## 注释

- 只在复杂业务规则、边界条件或非显然取舍处写注释
- 不写重复代码含义的空注释
""",
    "standards/testing.md": """# Testing Standard

## 测试策略

- 核心业务逻辑必须有单元测试
- 跨模块流程必须有集成测试
- 用户关键路径需要冒烟测试

## 测试要求

- 测试名称表达业务行为
- 覆盖正常路径、异常路径和边界条件
- 不为了覆盖率编写无意义测试

## 运行记录

每次 `/sdc:check` 后，将测试结果记录到 `.sdc/reports/` 或当前 change 的 `notes.md`。
""",
    "standards/architecture.md": """# Architecture Standard

## 模块边界

- 保持现有分层和模块边界
- 不跨层直接访问内部实现
- 新能力优先放在最贴近业务语义的位置

## 依赖方向

- 业务核心不依赖外围适配
- 公共工具不能反向依赖业务模块

## 设计取舍

重要架构决策必须记录到 `.sdc/decisions/`。
""",
    "standards/security.md": """# Security Standard

## 输入和输出

- 所有外部输入必须校验
- 用户可控内容输出前必须按场景转义或过滤

## 敏感信息

- 不硬编码密钥、令牌、密码
- 日志不得输出敏感信息

## 依赖

- 新增依赖前必须说明用途、维护状态和替代方案
""",
    "standards/git.md": """# Git Standard

## 变更粒度

- 一个提交只表达一个清晰意图
- 不混入无关格式化或本地配置

## 提交前

- 运行相关测试
- 更新 `.sdc/changes/active/<change-id>/notes.md`
- 需要时更新 `.sdc/specs/` 或 `.sdc/standards/`

## PR

- 说明需求背景、实现摘要、测试结果和风险
""",
    "standards/ai.md": """# AI Collaboration Standard

## 必须做

- 开始新需求前确认 `.sdc/` 是否存在
- 新需求进入 `.sdc/changes/active/`
- 实现前先看 `proposal.md`、`spec.md`、`design.md`、`tasks.md`
- 完成前执行 `/sdc:check`
- 归档时执行 `/sdc:archive`

## 绝对不要做

- 不要跳过需求记录直接改代码
- 不要把模板内容当作有效规范
- 不要覆盖已有 `.sdc/` 文件
- 不要删除 change 历史
- 不要忽略 `.sdc/standards/` 中的项目规范
""",
    "decisions/README.md": """# Decisions

记录重要技术/产品决策。推荐文件名：

```text
YYYY-MM-DD-short-title.md
```
""",
    "reviews/README.md": """# Reviews

保存 `/sdc:review` 的代码审查结果。
""",
    "reports/README.md": """# Reports

保存 `/sdc:test` 和 `/sdc:quality` 的测试、覆盖率、质量检查和交付报告。
""",
    "templates/change.md": """# Change Proposal

## 背景

## 目标

## 非目标

## 需求分解

## 验收标准

## 任务清单

## 风险和回滚
""",
    "templates/tasks.md": """# Tasks

## 实现任务

- [ ] 1. 任务描述
  - 验收：可验证结果
  - 前置：无

## 验证任务

- [ ] 运行测试
- [ ] 完成质量检查
""",
    "templates/design.md": """# Design

## 背景

## 方案

## 数据和接口变化

## 风险

## 替代方案
""",
    "templates/spec.md": """# Spec

## 需求背景

## 需求分解

## 验收标准

## 测试计划

## 风险评估
""",
    "templates/decision.md": """# Decision Record

## 状态

Proposed / Accepted / Deprecated

## 背景

## 决策

## 影响

## 替代方案
""",
    ".gitignore": """# SDC workspace
# 默认建议提交 .sdc 内容，因为它是项目需求和交付记录。
# 如需忽略本地临时文件，请写在下面。

*.tmp
""",
}

TEMPLATE = """# SDC {name} 文档

> 创建时间：{time}

请在这里粘贴从 Claude / Hermes 生成的内容：

---

"""

HEADER = "\033[95m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
ENDC = "\033[0m"


def print_color(color, text):
    print(f"{color}{text}{ENDC}")


def slugify(value):
    """Convert a change name into a filesystem-friendly slug."""
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value.strip().lower())
    slug = slug.strip("-")
    return slug or "change"


def change_path(change_id):
    active = SDC_DIR / "changes" / "active" / change_id
    if active.exists():
        return active

    legacy = SDC_DIR / "changes" / change_id
    if legacy.exists():
        return legacy

    return active


def archive_change_path(change_id):
    return SDC_DIR / "changes" / "archive" / change_id


def read_text(filepath):
    if not filepath.exists():
        return ""
    return filepath.read_text()


def has_real_content(filepath):
    text = read_text(filepath)
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith(">") and not line.strip().startswith("#")
    ]
    placeholders = ("（", ")", "TODO", "todo")
    return any(not any(marker in line for marker in placeholders) for line in lines)


def write_if_missing(relative_path, content):
    """Create a workspace file without overwriting user content."""
    filepath = SDC_DIR / relative_path
    if filepath.exists():
        return False

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)
    return True


def cmd_init():
    """初始化标准 SDC 工作区"""
    created = []

    SDC_DIR.mkdir(exist_ok=True)

    for dirname in DIRS:
        directory = SDC_DIR / dirname
        if not directory.exists():
            directory.mkdir(parents=True)
            created.append(f"{dirname}/")

    for relative_path, content in INIT_FILES.items():
        if write_if_missing(relative_path, content):
            created.append(relative_path)

    if created:
        print_color(GREEN, "✅ SDC 标准工作区已初始化")
        print(f"   目录: {SDC_DIR.absolute()}")
        print()
        print("已创建:")
        for item in created:
            print(f"  - {item}")
    else:
        print_color(YELLOW, "⚠️  SDC 工作区已存在，未覆盖任何文件")

    print()
    print("下一步:")
    print(f"  {BLUE}sdc spec{ENDC}    - 编辑当前需求规范")
    print(f"  {BLUE}sdc plan{ENDC}    - 生成/编辑规范和实现计划")
    print(f"  {BLUE}sdc apply{ENDC}   - 执行当前需求迭代")
    print(f"  {BLUE}sdc change login-flow{ENDC} - 创建一次需求迭代")
    print(f"  {BLUE}sdc status{ENDC}  - 查看工作区状态")


def cmd_change(name):
    """创建一次需求迭代目录"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
        return

    change_id = f"{date.today().isoformat()}-{slugify(name)}"
    directory = SDC_DIR / "changes" / "active" / change_id

    if directory.exists():
        print_color(YELLOW, f"⚠️  需求迭代已存在: {directory}")
        return

    directory.mkdir(parents=True)
    files = {
        "proposal.md": INIT_FILES["templates/change.md"].replace("# Change Proposal", f"# {change_id} Proposal"),
        "tasks.md": INIT_FILES["templates/tasks.md"],
        "design.md": INIT_FILES["templates/design.md"],
        "spec.md": INIT_FILES["templates/spec.md"],
        "notes.md": f"""# Notes

> Change: {change_id}
> Created: {datetime.now().isoformat()}

## 实现记录

## 问题记录

## 验证记录
""",
    }

    for filename, content in files.items():
        (directory / filename).write_text(content)

    print_color(GREEN, "✅ SDC 需求迭代已创建")
    print(f"   ID: {change_id}")
    print(f"   目录: {directory.absolute()}")
    print()
    print("下一步:")
    print(f"  {BLUE}sdc plan {change_id}{ENDC}   - 生成/完善计划")
    print(f"  {BLUE}sdc check {change_id}{ENDC}  - 综合检查")


def validate_file(errors, warnings, filepath, required_headings):
    if not filepath.exists():
        errors.append(f"缺少文件: {filepath}")
        return

    text = read_text(filepath)
    if not has_real_content(filepath):
        errors.append(f"内容仍是模板或缺少有效内容: {filepath}")

    for heading in required_headings:
        if heading not in text:
            errors.append(f"{filepath} 缺少章节: {heading}")


def cmd_validate(target="current"):
    """校验 current 或某个 change"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
        return

    errors = []
    warnings = []

    if target == "current":
        base = SDC_DIR / "current"
        validate_file(errors, warnings, base / "spec.md", ["## 需求分解", "## 验收标准", "## 测试计划"])
        validate_file(errors, warnings, base / "plan.md", ["## 任务拆解", "## 测试先行策略", "## 交付清单"])
        validate_file(errors, warnings, base / "apply.md", ["## 已完成任务", "## 修改文件", "## 测试结果"])
    else:
        base = change_path(target)
        if not base.exists():
            errors.append(f"需求迭代不存在: {base}")
        else:
            validate_file(errors, warnings, base / "proposal.md", ["## 背景", "## 目标", "## 验收标准"])
            validate_file(errors, warnings, base / "tasks.md", ["## 实现任务", "## 验证任务"])
            validate_file(errors, warnings, base / "spec.md", ["## 需求分解", "## 验收标准", "## 测试计划"])

            tasks_text = read_text(base / "tasks.md")
            if "- [ ]" not in tasks_text and "- [x]" not in tasks_text:
                errors.append(f"{base / 'tasks.md'} 缺少任务复选框")

    print()
    print_color(HEADER, f"🔍 SDC 校验结果: {target}")
    print("=" * 50)

    if errors:
        print_color(RED, "❌ 必须修复")
        for item in errors:
            print(f"  - {item}")
    else:
        print_color(GREEN, "✅ 必须项通过")

    if warnings:
        print()
        print_color(YELLOW, "⚠️  建议完善")
        for item in warnings:
            print(f"  - {item}")

    print("=" * 50)
    if errors:
        print_color(RED, "结论: 不可归档 / 不建议进入实现")
    else:
        print_color(GREEN, "结论: 校验通过")
    print()


def cmd_archive(change_id):
    """归档完成的需求迭代"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
        return

    source = change_path(change_id)
    if not source.exists():
        print_color(RED, f"❌ 需求迭代不存在: {source}")
        return

    spec = source / "spec.md"
    if not spec.exists():
        print_color(RED, f"❌ 缺少 spec.md，不能归档: {spec}")
        return
    if not has_real_content(spec):
        print_color(RED, f"❌ spec.md 仍是模板或缺少有效内容，不能归档: {spec}")
        return

    tasks = source / "tasks.md"
    if tasks.exists():
        tasks_text = read_text(tasks)
        if "- [ ]" in tasks_text and "- [x]" not in tasks_text:
            print_color(RED, f"❌ tasks.md 中没有已完成任务，不能归档: {tasks}")
            return

    specs_dir = SDC_DIR / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    target = specs_dir / f"{change_id}.md"

    if target.exists():
        print_color(YELLOW, f"⚠️  稳定规范已存在，未覆盖: {target}")
    else:
        target.write_text(f"# Archived Spec: {change_id}\n\n" + spec.read_text())

    archive_file = source / "archive.md"
    if not archive_file.exists():
        archive_file.write_text(f"""# Archive

> Change: {change_id}
> Archived: {datetime.now().isoformat()}

## 归档结果

- 稳定规范: `../../specs/{change_id}.md`
- 原始变更目录: `{source}`

## 交付结论

（填写可以交付 / 已上线 / 已废弃）
""")

    print_color(GREEN, "✅ SDC 需求迭代已归档")
    print(f"   Change: {change_id}")
    print(f"   Spec: {target.absolute()}")
    print(f"   Archive: {archive_file.absolute()}")

    archived_dir = archive_change_path(change_id)
    if source != archived_dir and source.exists() and not archived_dir.exists():
        archived_dir.parent.mkdir(parents=True, exist_ok=True)
        source.rename(archived_dir)
        print(f"   Moved: {archived_dir.absolute()}")


def cmd_check(target="current"):
    """综合检查入口：CLI 层先执行结构校验，并提示后续人工/AI 检查。"""
    cmd_validate(target)
    print_color(HEADER, "🔎 后续检查")
    print("  - 代码审查: /sdc:review")
    print("  - 测试验证: /sdc:test")
    print("  - 质量门禁: /sdc:quality")
    print("  - AI 中可直接使用: /sdc:check")
    print()


def cmd_edit(name):
    """编辑某个文档"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
        return

    filepath = SDC_DIR / FILES[name]
    if not filepath.exists():
        from datetime import datetime
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(TEMPLATE.format(name=name.capitalize(), time=datetime.now().isoformat()))
    
    # 用系统默认编辑器打开
    editor = os.environ.get("EDITOR", "nano")
    subprocess.run([editor, str(filepath)])
    
    print_color(GREEN, f"✅ {name}.md 已更新")


def cmd_status():
    """查看项目状态"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 未初始化，请先运行: sdc init")
        return

    print()
    print_color(HEADER, "📋 SDC 项目状态")
    print("=" * 50)
    
    done_count = 0
    for name, filename in FILES.items():
        filepath = SDC_DIR / filename
        status = GREEN + "✅" if filepath.exists() and filepath.stat().st_size > 100 else YELLOW + "⬜"
        size = filepath.stat().st_size if filepath.exists() else 0
        if size > 100:
            done_count += 1
        print(f"  {status} {name:<12} {ENDC} {size:>5} 字节")
    
    print("=" * 50)
    progress = int(done_count / len(FILES) * 100)
    print(f"  进度: {progress}% ({done_count}/{len(FILES)})")
    print()

    print_color(HEADER, "📂 标准目录")
    for dirname in DIRS:
        directory = SDC_DIR / dirname
        status = GREEN + "✅" if directory.exists() else RED + "❌"
        print(f"  {status} {dirname}/ {ENDC}")
    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
    elif cmd == "change":
        if len(sys.argv) < 3:
            print_color(RED, "❌ 用法: sdc change <short-name>")
            return
        cmd_change(sys.argv[2])
    elif cmd == "validate":
        target = sys.argv[2] if len(sys.argv) >= 3 else "current"
        cmd_validate(target)
    elif cmd == "archive":
        if len(sys.argv) < 3:
            print_color(RED, "❌ 用法: sdc archive <change-id>")
            return
        cmd_archive(sys.argv[2])
    elif cmd == "apply":
        cmd_edit("apply")
    elif cmd == "check":
        target = sys.argv[2] if len(sys.argv) >= 3 else "current"
        cmd_check(target)
    elif cmd == "spec":
        cmd_edit("spec")
    elif cmd == "plan":
        cmd_edit("plan")
    elif cmd == "implement":
        cmd_edit("implement")
    elif cmd == "review":
        cmd_edit("review")
    elif cmd == "test":
        cmd_edit("test")
    elif cmd == "quality":
        cmd_edit("quality")
    elif cmd == "harness":
        # 特殊处理：在项目根目录生成 AGENTS.md
        if not SDC_DIR.exists():
            print_color(RED, "❌ 请先运行: sdc init")
            return
        
        agents_file = Path("AGENTS.md")
        if not agents_file.exists():
            from datetime import datetime
            with open(agents_file, "w") as f:
                f.write(f"""# 🤖 AGENTS.md - 本项目 AI 助手必须遵守的规则

> 本文件是项目级的权威规则，优先级高于任何对话中的提示。
> 所有 AI 助手必须阅读并严格遵守。
> 创建时间：{datetime.now().isoformat()}

---

## ✅ 这个项目必须做

| 规则 | 验证方式 |
|------|---------|
| (请在 Claude 中运行 /sdc:harness 自动生成) | |

---

## ❌ 这个项目绝对不要做

| 禁止事项 | 原因 |
|---------|------|
| (请在 Claude 中运行 /sdc:harness 自动生成) | |

---

## 🔍 验证命令

| 操作 | 命令 |
|------|------|
| (请在 Claude 中运行 /sdc:harness 自动生成) | |

---

## 💀 历史上犯过的错误（不要再踩）

| 错误 | 发生时间 | 正确做法 |
|------|---------|---------|
| | | |

---

## 📝 更新记录

每次 AI 犯了一个新类型的错误，就立即追加到上面。
目标：同一个错误，永远不发生第二次。
""")
            print_color(GREEN, "✅ AGENTS.md 已创建")
        else:
            print_color(YELLOW, "⚠️  AGENTS.md 已存在")
        
        # 打开文件编辑
        editor = os.environ.get("EDITOR", "nano")
        subprocess.run([editor, str(agents_file)])
        
        print_color(GREEN, "✅ Harness 已更新")
    elif cmd == "status":
        cmd_status()
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
