#!/usr/bin/env python3
"""Adapt portable SDC context to the native Codex SessionStart wire protocol.

Contract: https://learn.chatgpt.com/docs/hooks#plugin-bundled-hooks
Packaging is opt-in; the client still owns capability checks, policy, and trust.
"""

import json
import os
from pathlib import Path
import subprocess
import sys


MAX_INPUT_BYTES = 65536
MAX_CONTEXT_CHARS = 4000
FALLBACK = (
    "SDC runtime context unavailable; manual fallback remains available: "
    "run the normal SDC stage command and pass --change or set SDC_ACTIVE_CHANGE when needed."
)


def session_context():
    if os.environ.get("SDC_RUNTIME_FORCE_HOOK_FAILURE") == "1":
        return FALLBACK
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        return FALLBACK
    event = json.loads(raw)
    if not isinstance(event, dict):
        return FALLBACK
    if event.get("hook_event_name", "SessionStart") != "SessionStart":
        return FALLBACK
    if event.get("source", "startup") not in ("startup", "resume", "clear", "compact"):
        return FALLBACK
    session_id = event.get("session_id")
    if not isinstance(session_id, str):
        session_id = ""
    if not session_id and os.environ.get("SDC_ALLOW_ENV_SESSION_ID") == "1":
        session_id = os.environ.get("SDC_SESSION_ID", "")
    helper = Path(__file__).resolve().parents[1] / "scripts/sdc-runtime-context.py"
    args = [sys.executable, str(helper), "session-context", "--client", "codex"]
    if session_id:
        args.extend(["--session-id", session_id])
    # Leave time for the safe response inside the client's five-second timeout.
    result = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, timeout=3, check=True)
    payload = json.loads(result.stdout)
    context = payload.get("additionalContext") if isinstance(payload, dict) else None
    if not isinstance(context, str) or not context.strip():
        return FALLBACK
    if len(context) > MAX_CONTEXT_CHARS:
        suffix = "\n...[truncated]"
        context = context[:MAX_CONTEXT_CHARS - len(suffix)] + suffix
    return context


def main():
    try:
        context = session_context()
    except (OSError, ValueError, RecursionError, subprocess.SubprocessError):
        context = FALLBACK
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart", "additionalContext": context,
    }}))


if __name__ == "__main__":
    main()
