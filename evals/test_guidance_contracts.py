"""Static reference routing contracts, not agent-behavior or prose-quality tests."""

from pathlib import Path
import os
import re
import shlex
import subprocess
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "sdc-references"
GUIDANCE = (
    "discovery-gate.md",
    "execution-orchestration.md",
    "domain-knowledge.md",
    "test-quality.md",
)


class GuidanceContractsTest(unittest.TestCase):
    def local_targets(self, name):
        source = REFERENCES / name
        self.assertTrue(source.is_file(), f"Missing guidance reference: {name}")
        targets = set()
        # These references use inline Markdown links, not reference-style links.
        for destination in re.findall(r"\[[^\]\n]+\]\(([^\s)]+)\)",
                                      source.read_text(encoding="utf-8")):
            url = urlsplit(destination)
            if not url.scheme and not url.netloc and url.path:
                targets.add((source.parent / unquote(url.path)).resolve())
        return targets

    def test_specialized_guidance_is_reachable_from_its_existing_entrypoint(self):
        routes = {
            "discovery-gate.md": "domain-knowledge.md",
            "execution-orchestration.md": "test-quality.md",
        }
        for entrypoint, target in routes.items():
            with self.subTest(entrypoint=entrypoint, target=target):
                destination = REFERENCES / target
                self.assertIn(destination, self.local_targets(entrypoint))
                self.assertTrue(destination.is_file(), f"Missing route target: {target}")

    def test_guidance_routes_back_to_shared_policy(self):
        authority = REFERENCES / "workflow-standards.md"
        for name in GUIDANCE:
            with self.subTest(reference=name):
                self.assertIn(authority, self.local_targets(name))

    def test_local_links_resolve_inside_the_repository(self):
        for name in GUIDANCE:
            with self.subTest(reference=name):
                for target in self.local_targets(name):
                    self.assertIn(ROOT, target.parents, f"Link escapes repository: {target}")
                    self.assertTrue(target.is_file(), f"Broken reference in {name}: {target}")

    def test_findings_list_example_runs_from_the_product_project(self):
        text = (REFERENCES / "review-findings.md").read_text()
        command = next(line for line in text.splitlines() if "sdc_findings.py" in line and "list --change example" in line)
        with tempfile.TemporaryDirectory(prefix="sdc-findings-doc-") as directory:
            project = Path(directory)
            (project / ".sdc/changes/active/example").mkdir(parents=True)
            command = command.replace("$SDC_PLUGIN_ROOT", str(ROOT))
            result = subprocess.run(shlex.split(command), cwd=project, text=True,
                                    capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
