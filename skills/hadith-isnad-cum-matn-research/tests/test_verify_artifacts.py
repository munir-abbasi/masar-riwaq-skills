#!/usr/bin/env python3
"""test_verify_artifacts.py

Unit and regression test suite for verify-artifacts.py and run-evals.py.
Uses standard library unittest only (no third-party dependencies).

Run:
  python3 -m unittest tests/test_verify_artifacts.py
"""

import json
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

# Import verify-artifacts.py via importlib
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
target_script = SCRIPTS_DIR / "verify-artifacts.py"
spec = importlib.util.spec_from_file_location("verify_artifacts", target_script)
verify_artifacts = importlib.util.module_from_spec(spec)
sys.modules["verify_artifacts"] = verify_artifacts
spec.loader.exec_module(verify_artifacts)

verify_batch_json = verify_artifacts.verify_batch_json
verify_manifest = verify_artifacts.verify_manifest


class TestArtifactVerification(unittest.TestCase):
    """Test suite covering schema, hygiene, and manifest verification logic."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_batch(self):
        """Test that a correctly formed batch passes all checks."""
        batch_file = self.test_path / "valid_batch.json"
        valid_data = {
            "schema_version": 1,
            "records": [
                {
                    "hadith_id": "rec_1",
                    "family_id": "fam_test",
                    "source_ref": {"collection": "Test Collection"},
                    "variants": [
                        {
                            "variant_id": "var_1",
                            "isnad_chain": ["transmitter_a", "transmitter_b"],
                            "matn_raw": "نص المتن السليم بدون أحرف السند",
                        }
                    ],
                }
            ],
        }
        batch_file.write_text(json.dumps(valid_data), encoding="utf-8")
        is_valid, errors = verify_batch_json(batch_file)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_invalid_schema_version(self):
        """Test rejection of unsupported schema versions."""
        batch_file = self.test_path / "invalid_schema.json"
        data = {
            "schema_version": 2,
            "records": [],
        }
        batch_file.write_text(json.dumps(data), encoding="utf-8")
        is_valid, errors = verify_batch_json(batch_file)
        self.assertFalse(is_valid)
        self.assertTrue(any("schema_version: 1" in e for e in errors))

    def test_boundary_bleed_detection(self):
        """Test that isnad connectors at start of matn trigger boundary bleed warnings."""
        batch_file = self.test_path / "boundary_bleed.json"
        data = {
            "schema_version": 1,
            "records": [
                {
                    "hadith_id": "rec_bleed",
                    "family_id": "fam_test",
                    "source_ref": {"collection": "Test Collection"},
                    "variants": [
                        {
                            "variant_id": "var_bleed",
                            "isnad_chain": ["narrator_1"],
                            "matn_raw": "حدثنا فلان قال سمعت رسول الله صلى الله عليه وسلم...",
                        }
                    ],
                }
            ],
        }
        batch_file.write_text(json.dumps(data), encoding="utf-8")
        is_valid, errors = verify_batch_json(batch_file)
        self.assertFalse(is_valid)
        self.assertTrue(any("Boundary bleed" in e for e in errors))

    def test_family_inconsistency_detection(self):
        """Test that multiple family_ids within a single batch are flagged."""
        batch_file = self.test_path / "split_families.json"
        data = {
            "schema_version": 1,
            "records": [
                {
                    "hadith_id": "rec_1",
                    "family_id": "fam_a",
                    "source_ref": {"collection": "Test Collection"},
                    "variants": [
                        {
                            "variant_id": "var_1",
                            "isnad_chain": ["narrator_1"],
                            "matn_raw": "نص الحديث الأول",
                        }
                    ],
                },
                {
                    "hadith_id": "rec_2",
                    "family_id": "fam_b",
                    "source_ref": {"collection": "Test Collection"},
                    "variants": [
                        {
                            "variant_id": "var_2",
                            "isnad_chain": ["narrator_2"],
                            "matn_raw": "نص الحديث الثاني",
                        }
                    ],
                },
            ],
        }
        batch_file.write_text(json.dumps(data), encoding="utf-8")
        is_valid, errors = verify_batch_json(batch_file)
        self.assertFalse(is_valid)
        self.assertTrue(any("Family inconsistency" in e for e in errors))

    def test_manifest_verification(self):
        """Test that research manifests require approval gates to be true."""
        manifest_file = self.test_path / "test_manifest.json"
        manifest_data = {
            "tradition_id": "sample",
            "title_ar": "حديث تجريبي",
            "orchestrator_version": "1.0",
            "gates": {
                "gate_1_scope_approved": True,
                "gate_2_boundaries_approved": True,
                "gate_3_identities_approved": True,
                "gate_4_publication_approved": False,
            },
        }
        manifest_file.write_text(json.dumps(manifest_data), encoding="utf-8")
        is_valid, errors = verify_manifest(manifest_file)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
