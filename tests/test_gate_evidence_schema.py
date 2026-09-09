#!/usr/bin/env python3
"""Direct local checks for the Gate Evidence Markdown contract.

The fixtures are intentionally local and opaque: no source value is parsed,
opened, dereferenced, or sent to an external system.
"""

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_STANDARDS = REPO_ROOT / "sdc-references" / "workflow-standards.md"

UUID_PATTERN = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
FIELD_NAMES = (
    "Status",
    "Resolution ID",
    "Resolution Source",
    "Closure ID",
    "Closure Source",
)

VALID_RECORD = """\
## Gate Evidence

- Status: Closed
- Resolution ID: 01234567-89ab-cdef-0123-456789abcdef
- Resolution Source: opaque-resolution-source
- Closure ID: fedcba98-7654-3210-fedc-ba9876543210
- Closure Source: opaque-closure-source
"""


def gate_evidence_sections(markdown):
    """Return peer-level Gate Evidence bodies without inspecting source values."""

    return re.findall(
        r"(?ms)^## Gate Evidence[ \t]*\r?\n(.*?)(?=^## |\Z)",
        markdown,
    )


def parse_record(markdown):
    """Validate one local record and report only rule/field classes on failure."""

    sections = gate_evidence_sections(markdown)
    if len(sections) != 1:
        raise AssertionError("section-count")

    body = sections[0]
    lines = [line for line in body.splitlines() if line.strip()]

    values = {}
    for field in FIELD_NAMES:
        matches = re.findall(
            rf"(?m)^- {re.escape(field)}:[ \t]*([^\r\n]*)$",
            body,
        )
        if len(matches) != 1:
            raise AssertionError(f"field:{field}")
        values[field] = matches[0]

    if len(lines) != len(FIELD_NAMES):
        raise AssertionError("field-count")
    expected_prefixes = [f"- {field}:" for field in FIELD_NAMES]
    actual_prefixes = [line.split(":", 1)[0] + ":" for line in lines]
    if actual_prefixes != expected_prefixes:
        raise AssertionError("field-order")

    if values["Status"] != "Closed":
        raise AssertionError("status")
    for field in ("Resolution ID", "Closure ID"):
        if re.fullmatch(UUID_PATTERN, values[field]) is None:
            raise AssertionError(f"uuid:{field}")
    for field in ("Resolution Source", "Closure Source"):
        if not values[field].strip():
            raise AssertionError(f"source:{field}")
    return values


class GateEvidenceSchemaTests(unittest.TestCase):
    def test_standard_declares_one_audit_safe_section(self):
        """AC-GE-01: the governed section is unique and outside the audit range."""

        standard = WORKFLOW_STANDARDS.read_text(encoding="utf-8")
        sections = gate_evidence_sections(standard)

        self.assertEqual(len(sections), 1, "section-count")
        task_format_start = standard.index("## Task Format")
        evidence_end = standard.index("## Evidence Discipline") + len(
            "## Evidence Discipline"
        )
        section_start = standard.index("## Gate Evidence")
        self.assertLess(task_format_start, evidence_end, "task-format-boundary")
        self.assertGreater(section_start, evidence_end, "placement")

        field_rows = re.findall(
            r"(?m)^\| (Status|Resolution ID|Resolution Source|Closure ID|Closure Source) \|",
            sections[0],
        )
        self.assertEqual(field_rows, list(FIELD_NAMES), "field-layout")
        self.assertIn("exactly `Closed`", sections[0], "closed-status-rule")
        self.assertIn("lowercase hexadecimal", sections[0], "uuid-rule")
        self.assertIn("8-4-4-4-12", sections[0], "uuid-shape")
        self.assertIn("exactly once", sections[0], "source-cardinality-rule")
        self.assertIn("opaque local Markdown", sections[0], "local-provenance-rule")
        self.assertIn(
            "does not parse, open, dereference, or authenticate",
            sections[0],
            "local-provenance-boundary",
        )

    def test_compliant_record_is_accepted(self):
        """AC-GE-02: a complete Layout A record passes local validation."""

        values = parse_record(VALID_RECORD)
        self.assertEqual(values["Status"], "Closed")
        self.assertEqual(values["Resolution Source"], "opaque-resolution-source")

    def test_noncanonical_ids_are_rejected(self):
        """AC-GE-02: IDs must be lowercase hexadecimal 8-4-4-4-12 text."""

        cases = {
            "resolution-id-uppercase": VALID_RECORD.replace(
                "01234567-89ab-cdef-0123-456789abcdef",
                "01234567-89AB-cdef-0123-456789abcdef",
            ),
            "closure-id-short": VALID_RECORD.replace(
                "fedcba98-7654-3210-fedc-ba9876543210",
                "fedcba98-7654-3210-fedc-ba987654321",
            ),
        }
        for rule, record in cases.items():
            with self.subTest(rule=rule):
                with self.assertRaisesRegex(AssertionError, r"^(uuid|field):"):
                    parse_record(record)

    def test_each_required_field_is_present_once(self):
        """AC-GE-02: removing any of the five fields fails closed."""

        for field in FIELD_NAMES:
            with self.subTest(field=field):
                record = "\n".join(
                    line
                    for line in VALID_RECORD.splitlines()
                    if not line.startswith(f"- {field}:")
                )
                with self.assertRaises(AssertionError):
                    parse_record(record)

    def test_non_closed_status_is_rejected(self):
        """AC-GE-02: only the literal Closed status is valid."""

        record = VALID_RECORD.replace("- Status: Closed", "- Status: Open")
        with self.assertRaisesRegex(AssertionError, "^status$"):
            parse_record(record)

    def test_named_sources_are_single_and_nonblank(self):
        """AC-GE-02: each named source is present exactly once and nonblank."""

        cases = {
            "resolution-source-missing": VALID_RECORD.replace(
                "- Resolution Source: opaque-resolution-source\n", ""
            ),
            "resolution-source-blank": VALID_RECORD.replace(
                "- Resolution Source: opaque-resolution-source",
                "- Resolution Source:   ",
            ),
            "resolution-source-duplicate": VALID_RECORD.replace(
                "- Resolution Source: opaque-resolution-source",
                "- Resolution Source: opaque-resolution-source\n"
                "- Resolution Source: second-opaque-source",
            ),
            "closure-source-missing": VALID_RECORD.replace(
                "- Closure Source: opaque-closure-source\n", ""
            ),
            "closure-source-blank": VALID_RECORD.replace(
                "- Closure Source: opaque-closure-source",
                "- Closure Source:   ",
            ),
            "closure-source-duplicate": VALID_RECORD.replace(
                "- Closure Source: opaque-closure-source",
                "- Closure Source: opaque-closure-source\n"
                "- Closure Source: second-opaque-source",
            ),
        }
        for rule, record in cases.items():
            with self.subTest(rule=rule):
                with self.assertRaisesRegex(AssertionError, r"^(field|source):"):
                    parse_record(record)

    def test_duplicate_gate_evidence_sections_are_rejected(self):
        """AC-GE-02: more than one peer section fails closed."""

        with self.assertRaisesRegex(AssertionError, "^section-count$"):
            parse_record(VALID_RECORD + VALID_RECORD)

    def test_diagnostics_do_not_echo_opaque_sources(self):
        """AC-GE-02: failures identify classes, never opaque source values."""

        invalid_record = VALID_RECORD.replace("- Status: Closed", "- Status: Open")
        with self.assertRaises(AssertionError) as failure:
            parse_record(invalid_record)
        self.assertNotIn("opaque-resolution-source", str(failure.exception))
        self.assertNotIn("opaque-closure-source", str(failure.exception))


if __name__ == "__main__":
    unittest.main()
