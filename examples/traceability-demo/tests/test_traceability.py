import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


DEMO_DIR = Path(__file__).resolve().parents[1]
RECORD_PATH = DEMO_DIR.parent / "synthetic-record.json"
SPEC = importlib.util.spec_from_file_location(
    "validate_traceability", DEMO_DIR / "validate_traceability.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class TraceabilityTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(RECORD_PATH.read_text(encoding="utf-8"))

    def test_synthetic_record_is_valid(self):
        result = MODULE.validate_record(self.record)
        self.assertTrue(result.valid, result.errors)
        self.assertEqual(2, len(result.traces))

    def test_unknown_card_fails(self):
        record = copy.deepcopy(self.record)
        record["findings"][0]["card_ids"].append("CARD-MISSING")
        result = MODULE.validate_record(record)
        self.assertFalse(result.valid)
        self.assertIn("FINDING-001 references unknown card: CARD-MISSING", result.errors)

    def test_out_of_range_page_fails(self):
        record = copy.deepcopy(self.record)
        record["documents"][1]["cards"][0]["source_reference"] = "DOC-B, p. 9, para. 1"
        result = MODULE.validate_record(record)
        self.assertFalse(result.valid)
        self.assertTrue(any("references page 9" in error for error in result.errors))

    def test_wrong_document_prefix_fails(self):
        record = copy.deepcopy(self.record)
        record["documents"][0]["cards"][0]["source_reference"] = "DOC-X, p. 1"
        result = MODULE.validate_record(record)
        self.assertFalse(result.valid)
        self.assertTrue(any("must begin with DOC-A" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
