# Discovery

## Current Understanding

SDC skills already include Chinese workflow rules, quality gates, red flags, and output formats. The user wants stronger SDDInAction-style role definition and requirements in English so each skill invocation carries a clear expert persona, operating contract, evidence discipline, and output contract.

## Candidate Directions

| Option | Description | Pros | Cons | Status |
|--------|-------------|------|------|--------|
| A | Add role contract only to core public skills | Small change | Advanced skills remain inconsistent | Rejected |
| B | Add concise English Role Prompt Contract to every SDC skill | Consistent invocation behavior | More files touched | Accepted |
| C | Put one shared contract only in README | Easy to maintain | Not reliably loaded when a skill fires | Rejected |

## Tradeoffs

The contract should be explicit enough to shape behavior, but not so long that every skill becomes noisy. It should complement the Chinese process rules, not replace them.

## Recommended MVP

Add a standardized English section to each `skills/*/SKILL.md`:

- Role
- Operating Contract
- Evidence Rules
- Output Contract

## Decision Ledger

| ID | Decision | Status | Source | Impact | Next Step |
|----|----------|--------|--------|--------|-----------|
| DEC-01 | Add English Role Prompt Contract to every SDC skill | Confirmed | User request | High | Implement |
| DEC-02 | Keep existing Chinese workflow sections | Confirmed | Preserve current SDC user-facing docs | Medium | Implement |
| DEC-03 | Bump package/plugin version | Confirmed | Published package metadata should reflect skill behavior change | Medium | Implement |

## Open Questions

| ID | Question | Why It Matters | Options | Required Before |
|----|----------|----------------|---------|-----------------|
| OQ-01 | Should contracts be English only | User explicitly requested English supplement | English only / bilingual | Resolved: English supplement |

## Exit Criteria

- [x] MVP scope confirmed
- [x] high-impact decisions confirmed or explicitly deferred
- [x] acceptance direction is clear
