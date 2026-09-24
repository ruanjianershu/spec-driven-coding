# Test Quality

Load this reference when planning or evaluating behavior tests, reproducing a bug, or investigating a failing check. [Workflow standards](workflow-standards.md) own risk and acceptance policy; [execution orchestration](execution-orchestration.md) owns task and review gates; [runtime context](runtime-context.md) owns receipt mechanics. This guidance assesses what tests prove, not a new testing stage or universal test-count requirement.

## Observable Behavior And Independent Expectations

- Exercise the relevant public boundary: a user action, exported function, CLI, API, or externally visible state transition. Assert concrete returned values, output, state, or side effects tied to confirmed acceptance, not private method names or incidental call order.
- Derive expected values independently from the confirmed requirement, a worked example, a trusted external contract, or an invariant. Do not call the implementation under test or copy its algorithm to compute the expected answer. Do not bless a generated snapshot without checking its expected meaning.
- Include the boundary, error, and regression cases that could distinguish this change from a plausible wrong implementation. Choose cases from affected risks, not a coverage percentage, arbitrary quota, or every theoretical combination.
- Use mocks or fakes at external boundaries when appropriate for deterministic, safe tests, including clocks, networks, and third-party services. Exercise the real behavior under test; mocking the internal decision being checked only proves the mock. Verify observable effects and relevant external contract assumptions, not just mock call counts.

For a confirmed rule "an invitation is invalid at or after its expiry", test a fixed time before expiry, exactly at expiry, and after expiry through the invitation acceptance boundary. Independently expect membership creation only before expiry and a specified rejection with no membership afterward. A controlled clock is useful; replacing the expiry decision with a mock is not. This example supplies no project policy without confirmation.

## Prove The Original Bug Before Fixing It

1. Identify the reported symptom, affected acceptance, and a reproducible input/state. Establish the expected result from its governing source before changing implementation.
2. Run a focused regression test or reproducible harness against the unfixed code. Capture the command, source snapshot, setup, expected versus actual result, and observed failure. Confirm that it fails because of the reported defect, not a broken fixture, missing dependency, or unrelated error.
3. Make the scoped fix only after the harness demonstrates the original bug. Run the same harness with the same inputs and expected behavior against the fix; it must now succeed. Do not weaken assertions or change expected values to match the implementation. If the reproducer was wrong, correct it and establish the failing baseline again before claiming regression proof.
4. Run affected neighboring boundary/error checks and retain both red and green evidence in the existing task report or notes. A red-phase result explains the bug; only current successful verification can support delivery.

When reproduction or execution is unavailable, record exactly what was attempted, the missing environment or evidence, and the next bounded check. Mark the affected acceptance `Cannot verify` and stop the dependent fix or delivery claim; inability is not a fake pass. If a fix already exists without a baseline, disclose the gap and reproduce against an isolated unfixed snapshot when possible without discarding user work. Do not invent a past failure or present unrelated passing tests as proof of the original bug.

For behavior-neutral documentation or mechanical edits, use meaningful structural or compatibility validation instead of manufacturing a failing behavior test.

## Focused Bug Hypotheses

Keep only evidence-supported hypotheses relevant to the symptom. Give each a stable local ID and record its supporting observation, predicted outcome, next discriminating check, and disposition in the existing bug report or notes. Preserve IDs and outcomes as evidence changes; do not replace the list each round or invent a minimum number of causes.

Choose the next check for its ability to distinguish the plausible causes. Update or reject a hypothesis contradicted by the result; do not repeatedly rerun the same failing action without new evidence. Stop investigation when the cause is demonstrated, or when the next useful check exceeds scope or needs unavailable evidence. Report any unresolved hypothesis and blocker instead of expanding into an unfocused repository audit. [Bug mode](delivery-gates.md#combined-check-modes) remains analysis-only unless a fix is explicitly requested; an authorized fix still needs the original regression to succeed before claiming resolution.
