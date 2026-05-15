# SDC Project Constitution

## 1. Governance Priority

`.sdc/constitution.md > AGENTS.md > conversation instructions`

If these sources conflict, stop and produce a Stop-Line Report.

## 2. Fact Priority

`spec.md > design.md/plan.md > tasks.md > code`

Code is evidence of current behavior, but it does not automatically override the agreed spec.

## 3. Core Chain

`spec -> plan -> tasks -> code -> verify -> archive`

## 4. Stop-The-Line Rules

Stop and produce a Stop-Line Report when:

- spec, design, or tasks are missing, conflicting, or not verifiable
- implementation requires changing business behavior, public contract, acceptance criteria, or key technical decisions
- current task requires scope expansion
- validation cannot prove the acceptance criteria

## 5. Traceability Rules

- specs must define `SCN-*`, `REQ-*`, and `AC-*` identifiers
- tasks must reference `REQ-*` and `AC-*`
- tests or validation notes must reference `AC-*`
- implementation notes must record validation evidence
