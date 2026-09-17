"""Explicit CLI adapters; no fallback model, plugin installation, or credential reads."""

import json
import shutil
import subprocess


REQUIRED_FLAGS = {
    "codex": ["--ignore-user-config", "--ignore-rules", "--ephemeral", "--json", "--sandbox"],
    "claude": ["--safe-mode", "--restricted", "--strict-mcp-config", "--no-session-persistence", "--permission-prompts"],
}


def probe_agent(agent, env, cwd, timeout=8):
    executable = shutil.which(agent, path=env.get("PATH"))
    result = {"agent": agent, "executable": executable, "installed": bool(executable),
              "authenticated": None, "auth_method": "unknown", "compatible": False,
              "version": None, "reason": None}
    if not executable:
        result["reason"] = "CLI not installed"
        return result

    def probe(args):
        return subprocess.run([executable, *args], cwd=cwd, env=env, capture_output=True,
                              text=True, timeout=timeout, check=False)

    try:
        version = probe(["--version"])
        result["version"] = version.stdout.strip()[:200]
        help_result = probe(["exec", "--help"] if agent == "codex" else ["--help"])
        missing = [flag for flag in REQUIRED_FLAGS[agent] if flag not in help_result.stdout]
        if agent == "codex":
            features = probe(["features", "list"])
            if "skip_host_skill_discovery" not in features.stdout:
                missing.append("skip_host_skill_discovery feature")
        result["compatible"] = help_result.returncode == 0 and not missing
        if missing:
            result["reason"] = "Missing isolation controls: " + ", ".join(missing)
        auth = probe(["login", "status"] if agent == "codex" else ["auth", "status"])
        result["auth_status_exit"] = auth.returncode
        if agent == "codex":
            status = (auth.stdout + auth.stderr).lower()
            result["authenticated"] = auth.returncode == 0 and "logged in" in status
            result["auth_method"] = "subscription" if "chatgpt" in status else "other-or-unknown"
        else:
            status = json.loads(auth.stdout)
            result["authenticated"] = status.get("loggedIn") is True
            result["auth_method"] = "subscription" if status.get("authMethod") in {"oauth_token", "claude.ai"} and status.get("apiProvider") == "firstParty" else "other-or-unknown"
        if not result["authenticated"]:
            result["reason"] = "No authenticated session in the selected environment; no login attempted"
        elif result["auth_method"] != "subscription":
            result["reason"] = "Only existing first-party subscription login is allowed; API billing/provider not authorized"
    except (OSError, subprocess.TimeoutExpired, ValueError, AttributeError) as exc:
        result["reason"] = "Status probe failed: " + type(exc).__name__
    result["ready"] = bool(result["compatible"] and result["authenticated"] and result["auth_method"] == "subscription")
    return result


def agent_command(agent, executable, model="default"):
    if agent == "codex":
        command = [executable, "--ask-for-approval", "never", "exec", "--json", "--ephemeral",
                   "--skip-git-repo-check", "--ignore-user-config", "--ignore-rules", "--sandbox", "workspace-write",
                   "--enable", "skip_host_skill_discovery"]
        for feature in ("plugins", "hooks", "apps", "browser_use", "computer_use", "image_generation", "multi_agent", "memories", "unbounded_connection_retries"):
            command += ["--disable", feature]
        for setting in ("project_doc_max_bytes=0", 'web_search="disabled"', 'model_provider="openai"',
                        "sandbox_workspace_write.network_access=false", "sandbox_workspace_write.exclude_slash_tmp=true",
                        "sandbox_workspace_write.exclude_tmpdir_env_var=true", "shell_environment_policy.inherit=none"):
            command += ["-c", setting]
        if model != "default":
            command += ["--model", model]
        return command + ["-"]
    # No Bash in this adapter: file tools are confined by --restricted. This is
    # intentionally not claimed to be equivalent to Codex's sandboxed shell.
    command = [executable, "--print", "--verbose", "--output-format", "stream-json",
               "--safe-mode", "--restricted", "--disable-slash-commands", "--no-chrome",
               "--no-session-persistence", "--setting-sources", "", "--strict-mcp-config",
               "--mcp-config", '{"mcpServers":{}}', "--tools", "Read,Glob,Grep,Edit,Write",
               "--permission-mode", "acceptEdits", "--permission-prompts", "none"]
    if model != "default":
        command += ["--model", model]
    return command
