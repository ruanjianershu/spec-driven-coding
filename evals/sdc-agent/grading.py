"""Conservative structural grading. Never execute model-written Python to grade it."""

import ast
import hashlib
import json
import math
from pathlib import Path


def infrastructure_category(error):
    """Classify CLI error diagnostics, never ordinary model answers or tool output."""
    text = json.dumps(error).lower() if isinstance(error, (dict, list)) else str(error).lower()
    markers = {
        "authentication": ("authentication_failed", "authentication_error", "not logged in", "invalid_api_key", "unauthorized", "authentication required"),
        "network": ("tls handshake", "connection refused", "connection reset", "connection_error", "network_error", "failed to connect", "stream disconnected", "econnreset", "enotfound"),
        "service": ("rate_limit", "rate limit", "overloaded", "service_unavailable", "service unavailable", "http 503", "quota exceeded", "insufficient_quota"),
        "configuration": ("error loading config", "unknown option", "unrecognized option", "unrecognized arguments"),
    }
    return next((category for category, values in markers.items() if any(value in text for value in values)), None)


def parse_transcript(agent: str, raw: str):
    result = {
        "model_status": "unknown", "model_exit": None, "observed_models": [],
        "usage": {"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "cost_usd": None},
        "tool_exits": [], "final_text": "", "malformed_lines": 0, "retry_events": [],
        "infrastructure_failure": None, "result_is_error": None,
    }
    usage = result["usage"]
    models = set()
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except (ValueError, TypeError):
            result["malformed_lines"] += 1
            continue
        if not isinstance(event, dict):
            result["malformed_lines"] += 1
            continue
        kind = event.get("type")
        if any(key in event and not isinstance(event[key], dict) for key in ("usage", "item", "message", "modelUsage") if key != "message" or kind in {"assistant", "user"}):
            result["malformed_lines"] += 1
            continue
        # Error envelopes outrank a later success-shaped terminal event. In
        # particular, Claude emits synthetic assistant messages for auth errors.
        if (kind in {"error", "turn.failed"} or (kind == "assistant" and event.get("error"))
                or (kind == "result" and event.get("is_error") is True)):
            result["model_status"] = "failed"
            for value in (event.get("error"), event.get("message"), event.get("result"), event.get("errors")):
                category = infrastructure_category(value)
                if category:
                    result["infrastructure_failure"] = result["infrastructure_failure"] or category
        if agent == "codex":
            if kind == "turn.completed":
                if result["model_status"] != "failed":
                    result["model_status"] = "completed"
                    result["model_exit"] = kind
                for key in ("input_tokens", "cached_input_tokens", "output_tokens"):
                    value = (event.get("usage") or {}).get(key)
                    if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0:
                        usage[key] = (usage[key] or 0) + value
            elif kind in {"turn.failed", "error"}:
                result["model_status"] = "failed"
                result["model_exit"] = kind
                if "reconnect" in str(event.get("message", "")).lower() or "retry" in str(event.get("message", "")).lower():
                    result["retry_events"].append(event.get("message"))
            elif kind == "item.completed":
                item = event.get("item") or {}
                if item.get("type") == "command_execution":
                    result["tool_exits"].append({
                        "tool": "command_execution", "command": item.get("command"),
                        "exit_code": item.get("exit_code"), "status": item.get("status", "unknown"),
                    })
                elif item.get("type") == "agent_message":
                    result["final_text"] += str(item.get("text", "")) + "\n"
        else:
            if kind == "system" and isinstance(event.get("model"), str):
                models.add(event["model"])
            elif kind == "assistant":
                message = event.get("message") or {}
                if isinstance(message.get("model"), str) and not message["model"].startswith("<"):
                    models.add(message["model"])
            elif kind == "user":
                content = (event.get("message") or {}).get("content", [])
                if not isinstance(content, list):
                    content = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "tool_result":
                        tool_status = "failed" if item.get("is_error") is True else "completed" if item.get("is_error") is False else "unknown"
                        result["tool_exits"].append({"tool": item.get("tool_use_id"), "exit_code": None, "status": tool_status})
            elif kind == "result":
                subtype = event.get("subtype")
                result["model_exit"] = subtype
                result["result_is_error"] = event.get("is_error")
                if result["model_status"] != "failed":
                    result["model_status"] = "failed" if subtype and subtype != "success" else "completed" if subtype == "success" and event.get("is_error") is False else "unknown"
                result["final_text"] = event.get("result", "")
                for key in ("input_tokens", "output_tokens"):
                    usage[key] = (event.get("usage") or {}).get(key)
                usage["cached_input_tokens"] = (event.get("usage") or {}).get("cache_read_input_tokens")
                usage["cost_usd"] = event.get("total_cost_usd")
                models.update((event.get("modelUsage") or {}).keys())
    result["observed_models"] = sorted(model for model in models if not model.startswith("<"))
    for key, value in usage.items():
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
            usage[key] = None
    if result["malformed_lines"] and result["model_status"] == "completed":
        result["model_status"] = "unknown"
    return result


def classify_execution(process, telemetry, stderr=""):
    category = telemetry.get("infrastructure_failure")
    if process.get("status") != "completed" or telemetry.get("model_status") != "completed":
        category = category or infrastructure_category(stderr)
    if category:
        return {"status": "blocked", "failure_category": category}
    if process.get("status") == "launch_error":
        return {"status": "unavailable", "failure_category": "launch"}
    if process.get("status") != "completed":
        return {"status": process.get("status", "unknown"), "failure_category": "execution"}
    if telemetry.get("model_status") != "completed":
        return {"status": "incomplete", "failure_category": "model_completion"}
    return {"status": "completed", "failure_category": None}


def aggregate_outcome(process_status, model_status, checks):
    # A process/setup failure cannot prove the task behavior failed. Retain the
    # raw artifact checks, but grade behavior only after confirmed completion.
    if process_status != "completed" or model_status != "completed":
        return "unknown"
    if any(c["status"] == "fail" for c in checks):
        return "fail"
    if not checks or any(c["status"] != "pass" for c in checks):
        return "unknown"
    return "pass"


def check(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def safe_file(root, path):
    if root not in path.parents:
        return False
    current = path
    while current != root:
        if current.is_symlink():
            return False
        current = current.parent
    return path.is_file() and path.stat().st_size <= 1_000_000


def digest(root, path):
    if not safe_file(root, path):
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_behavior(root: Path, mode="lower"):
    """A deliberately small pure expression interpreter, not eval/exec/import."""
    path = root / "src/labels.py"
    if not safe_file(root, path) or path.stat().st_size > 100_000:
        return check("normalize_behavior", "fail", "Missing, symlinked or oversized module")
    try:
        tree = ast.parse(path.read_text())
    except (SyntaxError, UnicodeError):
        return check("normalize_behavior", "fail", "Python syntax invalid")
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "normalize"]
    if len(functions) != 1:
        return check("normalize_behavior", "fail", "Expected one normalize function")
    function = functions[0]
    body = [n for n in function.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str))]
    if (len(tree.body) != 1 or function.decorator_list or len(body) != 1 or not isinstance(body[0], ast.Return)
            or len(function.args.args) != 1 or function.args.defaults or function.args.kwonlyargs
            or function.args.posonlyargs or function.args.vararg or function.args.kwarg
            or function.returns is not None or any(a.annotation is not None for a in function.args.args)):
        return check("normalize_behavior", "unknown", "Implementation outside safe AST grading subset; requires review")

    def interpret(node, value):
        if isinstance(node, ast.Name) and node.id == function.args.args[0].arg:
            return value
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in {"strip", "lower", "upper"} and not node.args and not node.keywords):
            return getattr(interpret(node.func.value, value), node.func.attr)()
        raise ValueError("Outside pure string-method subset")

    values = [" Mixed Case ", "", " \tA B\n", "already", "ABC"]
    try:
        observed = [interpret(body[0].value, value) for value in values]
    except (ValueError, TypeError, RecursionError):
        return check("normalize_behavior", "unknown", "Implementation requires independent review")
    expected = [getattr(value.strip(), mode)() for value in values]
    return check("normalize_behavior", "pass" if observed == expected else "fail", {"inputs": values, "expected": expected, "observed": observed, "method": "pure AST subset, not a test execution"})


def structural_checks(scenario: str, root: Path, before: dict, phases: list):
    checks = []
    immutable = [name for name in before if name.startswith("tests/")]
    if scenario in {"failed-test-delivery", "brownfield-conflict"}:
        immutable += [name for name in before if name.startswith("src/") or name.startswith("knowledge/")]
    if scenario == "interruption-resume":
        immutable.append("completed.txt")
    changed = [name for name in immutable if digest(root, root / name) != before.get(name)]
    checks.append(check("immutable_fixture_files", "fail" if changed else "pass", {"changed": changed, "count": len(immutable)}))
    if scenario == "vague-intake":
        created = [p.relative_to(root).as_posix() for p in root.rglob("*")
                   if p.is_file() and p.suffix in {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".java", ".rs", ".html", ".sh"}
                   and p.relative_to(root).as_posix() not in before]
        checks.append(check("no_unapproved_implementation", "fail" if created else "pass", created))
    if scenario in {"authorized-maintenance", "revision-invalidation", "interruption-resume"}:
        checks.append(normalize_behavior(root))
    if scenario == "failed-test-delivery":
        failures = [tool for phase in phases for tool in phase.get("telemetry", {}).get("tool_exits", [])
                    if "unittest" in (tool.get("command") or "") and isinstance(tool.get("exit_code"), int) and tool["exit_code"] > 0]
        checks.append(check("observed_failed_test", "pass" if failures else "unknown", failures or "No structured failing unittest tool exit observed"))
    if scenario == "revision-invalidation":
        checks.append(check("two_revision_sessions", "pass" if len(phases) == 2 and all(p.get("process", {}).get("status") == "completed" for p in phases) else "unknown", "Both revisions require distinct completed invocations"))
        checks.append(check("durable_revision_evidence", "pass" if safe_file(root, root / "evidence.md") else "fail", "Existence only; provenance/freshness is semantic review"))
    if scenario == "interruption-resume":
        try:
            if not safe_file(root, root / "progress.json"):
                raise ValueError("Unsafe progress file")
            data = json.loads((root / "progress.json").read_text())
            status = "pass" if data.get("pending") == [] and "step-1" in data.get("completed", []) else "fail"
        except (OSError, ValueError, AttributeError):
            status = "fail"
        checks.append(check("durable_progress_updated", status, "Pending is empty and completed step preserved"))
    return checks
