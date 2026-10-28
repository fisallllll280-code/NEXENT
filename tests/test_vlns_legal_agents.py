import unittest

from nexent.vlns import EvidenceSource, LegalKnowledgeBase, VXCoordinator


class VLNSLegalAgentTests(unittest.TestCase):
    def setUp(self):
        self.kb = LegalKnowledgeBase()
        self.kb.register(EvidenceSource(
            source_id="SA-DEMO-001",
            title="Synthetic demo source",
            jurisdiction="SA",
            citation="Demo Article 1",
            text="A synthetic rule about notice and deadlines.",
            effective_from="2025-01-01",
        ))

    def test_hash_is_stable_and_tampering_is_rejected(self):
        source = self.kb.sources()[0]
        self.assertEqual(len(source.sha256), 64)
        with self.assertRaises(ValueError):
            EvidenceSource(source_id="tampered", title="Demo", jurisdiction="SA",
                citation="Demo 2", text="changed", sha256=source.sha256)

    def test_duplicate_requires_explicit_replace(self):
        with self.assertRaises(ValueError):
            self.kb.register(self.kb.sources()[0])
        self.kb.register(self.kb.sources()[0], replace=True)
        self.assertEqual(self.kb.events()[-1]["event"], "SOURCE_REPLACED")

    def test_query_returns_provenance_and_human_gate(self):
        result = VXCoordinator(self.kb).review("notice deadlines", jurisdiction="SA")
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertEqual(result["authority"], "HUMAN_REVIEW_REQUIRED")
        self.assertFalse(result["najiz_connected"])
        self.assertFalse(result["external_actions_performed"])
        self.assertTrue(result["agent_results"][0]["findings"][0]["sha256"])

    def test_unknown_query_fails_closed(self):
        result = VXCoordinator(self.kb).review("unrelated quantum astronomy")
        self.assertEqual(result["status"], "HOLD_INSUFFICIENT_EVIDENCE")

    def test_jurisdiction_filter(self):
        result = VXCoordinator(self.kb).review("notice deadlines", jurisdiction="US")
        self.assertEqual(result["status"], "HOLD_INSUFFICIENT_EVIDENCE")

    def test_manifest_is_valid_json_with_audit_events(self):
        import json
        manifest = json.loads(self.kb.export_manifest())
        self.assertEqual(manifest["schema_version"], "1.0.0")
        self.assertEqual(len(manifest["sources"]), 1)
        self.assertEqual(len(manifest["events"]), 1)

    def test_empty_query_rejected(self):
        with self.assertRaises(ValueError):
            VXCoordinator(self.kb).review("   ")

    def test_invalid_effective_date_rejected(self):
        with self.assertRaises(ValueError):
            EvidenceSource(source_id="bad-date", title="Demo", jurisdiction="SA",
                citation="Demo 3", text="text", effective_from="not-a-date")


if __name__ == "__main__":
    unittest.main()
