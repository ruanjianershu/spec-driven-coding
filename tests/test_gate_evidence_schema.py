#!/usr/bin/env python3
"""Direct, local checks for the versioned Gate Evidence Markdown contract."""

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
    """Return peer-level Gate Evidence section bodies without touching sources."""

    return re.findall(
        r"(?ms)^## Gate Evidence[ \t]*(?:\r?\n|\r|\Z)(.*?)(?=^## |\Z)",
        markdown,
    )


def parse_record(markdown):
    """Validate one local record and expose only rule/field classes on failure."""

    sections = gate_evidence_sections(markdown)
    if len(sections) != 1:
        raise AssertionError("section-count")

    lines = [line for line in sections[0].splitlines() if line.strip()]
    if len(lines) != len(FIELD_NAMES):
        raise AssertionError("field-count")

    values = {}
    for expected_field, line in zip(FIELD_NAMES, lines):
        match = re.fullmatch(
            rf"- {re.escape(expected_field)}:[ \t]*([^\r\n]*)",
            line,
        )
        if match is None:
            raise AssertionError(f"field:{expected_field}")
        values[expected_field] = match.group(1)

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
    def test_standard_declares_one_audit_safe_gate_evidence_section(self):
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
        self.assertIn("does not parse, open, dereference, or authenticate", sections[0])

    def test_compliant_record_is_accepted(self):
        values = parse_record(VALID_RECORD)
        self.assertEqual(values["Status"], "Closed")
        self.assertEqual(values["Resolution Source"], "opaque-resolution-source")

    def test_invalid_ids_are_rejected(self):
        cases = {
            "resolution-id": VALID_RECORD.replace(
                "01234567-89ab-cdef-0123-456789abcdef",
                "01234567-89AB-cdef-0123-456789abcdef",
            ),
            "closure-id": VALID_RECORD.replace(
                "fedcba98-7654-3210-fedc-ba9876543210",
                "fedcba98-7654-3210-fedc-ba987654321",
            ),
        }
        for rule, record in cases.items():
            with self.subTest(rule=rule):
                with self.assertRaises(AssertionError):
                    parse_record(record)

    def test_each_missing_required_field_is_rejected(self):
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
        record = VALID_RECORD.replace("- Status: Closed", "- Status: Open")
        with self.assertRaises(AssertionError):
            parse_record(record)

    def test_named_sources_must_be_single_nonblank_lines(self):
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
                with self.assertRaises(AssertionError):
                    parse_record(record)

    def test_duplicate_gate_evidence_sections_are_rejected(self):
        with self.assertRaises(AssertionError):
            parse_record(VALID_RECORD + VALID_RECORD)

    def test_eof_duplicate_gate_evidence_titles_are_rejected(self):
        cases = {
            "eof": "## Gate Evidence",
            "eof-space": "## Gate Evidence ",
            "eof-tab": "## Gate Evidence\t",
            "newline": "## Gate Evidence\n",
            "carriage-return": "## Gate Evidence\r",
            "carriage-return-newline": "## Gate Evidence\r\n",
            "space-carriage-return-newline": "## Gate Evidence \r\n",
            "tab-carriage-return-newline": "## Gate Evidence\t\r\n",
        }
        for boundary, duplicate_title in cases.items():
            with self.subTest(boundary=boundary):
                with self.assertRaisesRegex(AssertionError, r"^section-count$"):
                    parse_record(VALID_RECORD + duplicate_title)

    def test_failures_do_not_echo_opaque_source_values(self):
        invalid_record = VALID_RECORD.replace(
            "- Status: Closed", "- Status: Open"
        )
        with self.assertRaises(AssertionError) as failure:
            parse_record(invalid_record)
        self.assertNotIn("opaque-resolution-source", str(failure.exception))
        self.assertNotIn("opaque-closure-source", str(failure.exception))


if __name__ == "__main__":
    unittest.main()
