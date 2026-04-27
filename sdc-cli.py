#!/usr/bin/env python3
"""
SDC CLI - 规范驱动开发 薄运行层
功能：自动管理 SDC 项目文档，不用手动复制粘贴

用法：
  sdc init          # 初始化 SDC 工作区
  sdc spec          # 打开规范文档（你在 Claude 里写完粘贴进来）
  sdc plan          # 打开计划文档
  sdc implement     # 打开开发记录文档
  sdc review        # 打开审查报告
  sdc test          # 打开测试报告
  sdc quality       # 打开质量检查报告
  sdc harness       # 生成/编辑 AGENTS.md 项目级 AI 规则
  sdc status        # 查看项目进度
"""

import os
import sys
import subprocess
from pathlib import Path

SDC_DIR = Path(".sdc")
FILES = {
    "spec": "spec.md",
    "plan": "plan.md",
    "implement": "implement.md",
    "review": "review.md",
    "test": "test.md",
    "quality": "quality.md",
    "harness": "harness.md",
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


def cmd_init():
    """初始化 SDC 工作区"""
    if SDC_DIR.exists():
        print_color(YELLOW, "⚠️  SDC 工作区已经存在")
        return

    SDC_DIR.mkdir()
    
    # 创建 .gitignore
    with open(SDC_DIR / ".gitignore", "w") as f:
        f.write("# SDC 工作文件\n")
        f.write("# 可以提交也可以不提交，看你的需求\n")
    
    print_color(GREEN, "✅ SDC 工作区已初始化")
    print(f"   目录: {SDC_DIR.absolute()}")
    print()
    print("下一步:")
    print(f"  {BLUE}sdc spec{ENDC}    - 编辑规范文档")


def cmd_edit(name):
    """编辑某个文档"""
    if not SDC_DIR.exists():
        print_color(RED, "❌ 请先运行: sdc init")
        return

    filepath = SDC_DIR / FILES[name]
    if not filepath.exists():
        from datetime import datetime
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


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
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
