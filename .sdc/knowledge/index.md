<!-- SDC-MANAGED path=knowledge/index.md; sha256=4116e1d09f5993ffcb45644db47cf349d932e4b8702cbe09f6f904e7028d67e5 -->
# Knowledge Index

> 每次非平凡 change/plan/apply 前先读这里，再按任务打开相关知识文件。

## Product Knowledge

| Topic | File | Status | When To Read | Evidence Rule |
|-------|------|--------|--------------|---------------|
| Product overview | `product/overview.md` | Candidate | 新需求、范围讨论、产品目标变化 | Source + Verified Against required |
| Roles and permissions | `product/roles.md` | Candidate | 涉及用户、权限、审批或可见性 | Source + Verified Against required |
| Domain concepts | `product/domain.md` | Candidate | 涉及业务术语、对象和状态 | Source + Verified Against required |
| Product flows | `product/flows.md` | Candidate | 涉及流程、状态机、用户路径 | Source + Verified Against required |
| Business rules | `product/rules.md` | Candidate | 涉及业务规则、验收标准、不变量 | Source + Verified Against required |
| Product decisions | `product/decisions.md` | Candidate | 涉及产品取舍、非目标、延期范围 | Source + Verified Against required |

## Technical Knowledge

| Topic | File | Status | When To Read | Evidence Rule |
|-------|------|--------|--------------|---------------|
| Stack | `technical/stack.md` | Candidate | 技术选型、依赖、运行环境 | Code/config evidence required |
| Architecture | `technical/architecture.md` | Candidate | 模块边界、依赖方向、设计变化 | Code/config evidence required |
| Modules | `technical/modules.md` | Candidate | 查找实现位置、影响面 | Code evidence required |
| Data and interfaces | `technical/data-and-interfaces.md` | Candidate | 数据模型、API、事件、集成 | Code/schema/contract evidence required |
| Operations | `technical/operations.md` | Candidate | 启动、部署、回滚、排障 | Script/config evidence required |
| Testing | `technical/testing.md` | Candidate | 验证策略、测试命令、回归风险 | Test/build evidence required |

## Current State

- Current focus: `current.md`
- Project cognition: `../project-cognition.md`
- Standards: `../standards/`
- Decisions: `../decisions/`

## Retrieval Rule

Read only the entries relevant to the current task. If a needed knowledge file is missing or stale, record a Knowledge Gap and ask whether to refresh it.

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|--------|-------------------|----------------|--------|-----------|--------|
