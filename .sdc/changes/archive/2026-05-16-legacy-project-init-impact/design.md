# Design

## 背景

SDC 已有 repo/brownfield 和 impact 分析模式，但流程时机需要更精确：项目整体认知属于 init/repo 阶段，具体需求影响分析属于 change 需求确认后。

## 方案

1. `sdc:init`
   - 生成 `project-cognition.md` 和 `templates/project-cognition.md`。
   - 在技能说明中要求识别 Greenfield 与 Brownfield/Legacy。
   - 对遗留项目提示 `/sdc:check repo` 用代码证据补全项目整体认知。

2. `sdc:change`
   - 每个 change 增加 `impact.md` 文件。
   - 明确 Change Impact Gate 的调用时机：Discovery Gate 退出、spec Confirmed 之后，plan/apply 之前。
   - 使用本地参考流程的证据优先结构：分析快照、入口、调用链、直接修改点、级联影响、契约/数据/配置、安全/观测、测试回归、实施顺序、待确认问题。

3. `sdc:plan` / `sdc:apply`
   - 遗留项目必须读取 `impact.md`。
   - 如 `impact.md` 存在影响范围/验收/契约/数据/安全的待确认问题，必须停线。

4. `sdc:review` / `sdc:check`
   - 遗留项目最终输出“老系统改造点与影响点分析”。
   - 用实际 diff、notes、测试结果对照 `impact.md`，标出符合、偏离、新增影响和残余风险。

## 影响范围

- CLI 初始化模板和 change 模板。
- SDC init/change/plan/apply/check/review/validate/core skills。
- README、discipline docs、marketplace docs、package/plugin metadata。
- `.sdc` 自身工作区模板和本次 change 记录。

## 不改范围

- 不新增公开 slash command。
- 不引入外部服务或 MCP。
- 不自动深度扫描并填充完整报告；真实认知和影响分析由 AI skill 基于项目代码完成。

## 数据和接口变化

- 新增 `.sdc/project-cognition.md`。
- 新增 `.sdc/templates/project-cognition.md`。
- 每个新 change 新增 `.sdc/changes/active/<change-id>/impact.md`。
- `sdc-cli.py change` 创建 `impact.md`。

## REQ/AC 到设计决策的映射

| REQ | AC | 设计点 |
|-----|----|--------|
| REQ-01 | AC-01 | init 生成 project cognition 模板并说明 legacy 路径 |
| REQ-02 | AC-02, AC-03 | change/plan/apply 引入 Change Impact Gate |
| REQ-03 | AC-04 | review/check 增加 Legacy Final Impact Review |

## 风险

- 模板多：通过“不新增公开命令”和“仅 legacy 强制”控制复杂度。
- 误判 legacy：CLI 只提示，最终由用户/AI 结合项目事实确认。

## 回滚方案

恢复 CLI 模板和 skill 文档到上一版本，删除新增模板字段即可。

## 替代方案

- 新增 `/sdc:legacy-impact` 指令：拒绝，增加用户记忆负担。
- init 阶段直接生成影响分析：拒绝，没有需求时无法分析具体影响。
