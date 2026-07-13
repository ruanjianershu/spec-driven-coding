# 2026-07-11-superpowers-v6-execution Proposal

## Status

Confirmed - Discovery Closed

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| discovery.md | Confirmed | DEC-01 through DEC-04 | Defines accepted scope |
| existing SDC commands and CLI | Confirmed | repository source | Defines compatibility boundaries |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## 背景

Superpowers 6 improved post-plan execution cost and quality. SDC needs the core execution mechanisms while preserving its smaller public workflow and stronger governance model.

## 目标

Make SDC plans independently executable, review-gated, context-efficient, and recoverable after compaction.

## 非目标

- No new public command.
- No brainstorm web server.
- No mandatory worktree or mandatory commit per task.
- No dependency on Superpowers.

## 初始场景

An agent receives a confirmed SDC plan, executes each thin task with focused context, proves it, receives an independent review, resumes safely after context loss, and finishes with one whole-change review.

## 初始需求

SDC plan/apply/check must enforce execution orchestration as an internal contract and provide deterministic helper tooling and eval coverage.

## 初始验收标准

Missing task interfaces or approved review evidence blocks delivery; helper scripts create file handoffs; Codex metadata and deterministic packaging are release-audited; existing public commands remain unchanged.

## 任务清单

See tasks.md.

## 风险和回滚

Stricter schemas can reject old active changes. Safe init upgrades generated templates with backups; user-authored change files are not silently rewritten.
