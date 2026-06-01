#!/usr/bin/env python3
"""Run deterministic SDC flow evals without requiring an LLM provider."""

import sys
import tempfile
from pathlib import Path

from sdc_flow_provider import SCENARIOS


def main() -> int:
    failures = []

    print("SDC flow evals")
    print("=" * 50)

    for name, scenario in SCENARIOS.items():
        with tempfile.TemporaryDirectory(prefix="sdc-flow-eval-") as tmp:
            output = scenario(Path(tmp))

        passed = "RESULT: PASS" in output and "RESULT: FAIL" not in output
        status = "PASS" if passed else "FAIL"
        print(f"{status} {name}")

        if not passed:
            failures.append((name, output))

    print("=" * 50)

    if failures:
        print(f"{len(failures)} eval(s) failed")
        for name, output in failures:
            print()
            print(f"--- {name} output ---")
            print(output)
        return 1

    print(f"All {len(SCENARIOS)} evals passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
