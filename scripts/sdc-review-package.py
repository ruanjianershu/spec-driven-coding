#!/usr/bin/env python3
"""Write a task or whole-change git review package under .sdc/runtime."""

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def git(*args):
    result = subprocess.run(
        ["git", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.rstrip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", help="Base commit")
    parser.add_argument("head", help="Head commit or WORKTREE")
    parser.add_argument("change", help="Change id used for runtime directory")
    parser.add_argument("label", help="Task id such as T001 or final")
    args = parser.parse_args()

    git("rev-parse", "--show-toplevel")
    git("rev-parse", "--verify", args.base)

    working_tree = args.head.upper() == "WORKTREE"
    if working_tree:
        untracked = git("ls-files", "--others", "--exclude-standard", "--")
        if untracked:
            raise SystemExit(
                "WORKTREE review package would omit untracked files. "
                "Stage or commit them before review:\n" + untracked
            )
        head_label = "WORKTREE"
        commits = git("log", "--oneline", f"{args.base}..HEAD")
        stat = git("diff", "--stat", args.base, "--")
        diff = git("diff", "--no-ext-diff", "--unified=10", args.base, "--")
    else:
        git("rev-parse", "--verify", args.head)
        head_label = args.head
        commits = git("log", "--oneline", f"{args.base}..{args.head}")
        stat = git("diff", "--stat", f"{args.base}..{args.head}")
        diff = git("diff", "--no-ext-diff", "--unified=10", f"{args.base}..{args.head}")

    runtime = Path(".sdc/runtime") / args.change
    runtime.mkdir(parents=True, exist_ok=True)
    suffix = "final-review-package.md" if args.label.lower() == "final" else f"task-{args.label.upper()}-review-package.md"
    output = runtime / suffix
    output.write_text(
        f"""# SDC Review Package

- Base: {args.base}
- Head: {head_label}
- Change: {args.change}
- Label: {args.label}
- Generated At: {datetime.now(timezone.utc).isoformat()}

## Commits

```text
{commits or '(no commits in range)'}
```

## Diff Stat

```text
{stat or '(no diff stat)'}
```

## Diff

```diff
{diff or '(no diff)'}
```
"""
    )
    print(output)


if __name__ == "__main__":
    main()
