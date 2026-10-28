import json
import unittest

from nexent.gap_engine import (
    CapabilityRecord, EvidenceState, analyze_gaps, build_report,
    generate_candidate_manifests,
)


class GapEngineTests(unittest.TestCase):
    def test_verified_is_not_a_gap(self):
        rows = [CapabilityRecord("CAP-1", "Existing", True, EvidenceState.VERIFIED, ("src/a.py",))]
        self.assertEqual(analyze_gaps(rows), [])

    def test_not_observed_is_inventory_gap_not_missing(self):
        rows = [CapabilityRecord("CAP-2", "Unknown", True, EvidenceState.NOT_OBSERVED)]
        gap = analyze_gaps(rows)[0]
        self.assertEqual(gap.gap_type, "INVENTORY_GAP")
        self.assertIn("bounded inventory", gap.safe_next_step)

    def test_unverified_implementation_requires_tests(self):
        rows = [CapabilityRecord("CAP-3", "Code", True, EvidenceState.IMPLEMENTED_UNVERIFIED, ("src/code.py",))]
        self.assertEqual(analyze_gaps(rows)[0].gap_type, "VERIFICATION_GAP")

    def test_conflicts_do_not_autogenerate_candidates(self):
        rows = [CapabilityRecord("CAP-4", "Conflict", True, EvidenceState.CONFLICT, ("doc/a.md", "doc/b.md"))]
        gaps = analyze_gaps(rows)
        self.assertEqual(gaps[0].gap_type, "CONFLICT")
        self.assertEqual(generate_candidate_manifests(gaps), [])

    def test_specified_gap_generates_reviewable_candidate(self):
        rows = [CapabilityRecord("CAP-5", "Planned", True, EvidenceState.SPECIFIED, ("docs/spec.md",), ("test passes",))]
        candidate = generate_candidate_manifests(analyze_gaps(rows))[0]
        self.assertEqual(candidate["status"], "PROPOSED")
        self.assertTrue(candidate["required_human_review"])
        self.assertFalse(candidate["merge_authorized"])
        self.assertFalse(candidate["deployment_authorized"])

    def test_duplicate_ids_rejected(self):
        rows = [
            CapabilityRecord("CAP-X", "A", True, EvidenceState.PROPOSED),
            CapabilityRecord("CAP-X", "B", True, EvidenceState.PROPOSED),
        ]
        with self.assertRaises(ValueError):
            analyze_gaps(rows)

    def test_report_is_deterministic_and_json_serializable(self):
        rows = [CapabilityRecord("CAP-7", "Planned", True, EvidenceState.PROPOSED)]
        a = build_report(rows)
        b = build_report(rows)
        self.assertEqual(a, b)
        self.assertEqual(json.loads(json.dumps(a))["status"], "ANALYSIS_ONLY")


if __name__ == "__main__":
    unittest.main()
