---
description: SDC main entry. Route init, change, plan, apply, check, archive, and harness for spec-driven coding.
---

# SDC Main Entry

Follow the installed `sdc` skill exactly.

Use this command as the unified SDC entry. Interpret "$ARGUMENTS" as the user's current intent and route to the correct SDC stage:

- initialize workspace -> `sdc-init`
- new requirement/change -> `sdc-change`, then `sdc-spec` and `sdc-plan`
- implement current change -> `sdc-apply`
- delivery check -> `sdc-check`
- archive completed work -> `sdc-archive`
- generate project AI rules -> `sdc-harness`

