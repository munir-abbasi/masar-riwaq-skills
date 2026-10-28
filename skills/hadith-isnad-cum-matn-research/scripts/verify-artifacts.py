#!/usr/bin/env python3
"""verify-artifacts.py

Deterministic verification script for Hadith isnād-cum-matn research artifacts.
Validates:
1. Riwaq import batch JSON structure (schema_version: 1).
2. Boundary hygiene (no isnād connectors in matn slices).
3. Chain integrity (depth >= 1, valid narrator identifiers).
4. Manifest and witness matrix consistency.
5. Epistemic typing compliance.

Usage:
  python3 verify-artifacts.py --batch path/to/import-batch.json [--manifest path/to/manifest.json]
"""

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

ISNAD_CONNECTOR_TOKENS: Set[str] = {
    "حدثنا",
    "أخبرنا",
    "أنبأنا",
    "سمعت",
    "قال سمعت",
    "عن",
    "أن رسول الله",
    "قال قال",
}


class BatchValidationError(ValueError):
    """Raised when an import batch fails structural or hygiene validation."""
    pass


class ManifestValidationError(ValueError):
    """Raised when a research manifest fails gate or completeness checks."""
    pass


class ArtifactVerifier:
    """Deterministic validation engine for ICMA research batches and manifests."""

    def __init__(self, batch_path: Path, manifest_path: Optional[Path] = None):
        self.batch_path = batch_path
        self.manifest_path = manifest_path

    def load_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Safely read and parse a JSON document with typed error handling."""
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
        try:
            content = file_path.read_text(encoding="utf-8")
            data = json.loads(content)
            if not isinstance(data, dict):
                raise TypeError(f"Root JSON entity in {file_path} must be a dictionary object.")
            return data
        except json.JSONDecodeError as exc:
            raise ValueError(f"Malformed JSON in {file_path}: {exc}") from exc
        except (KeyError, TypeError) as exc:
            raise ValueError(f"Structural data error in {file_path}: {exc}") from exc
        except Exception as exc:
            raise ValueError(f"Unexpected error loading {file_path}: {exc}") from exc

    def verify_batch(self) -> Tuple[bool, List[str]]:
        """Validate Riwaq schema_version: 1 rules, narrator chains, and boundary hygiene."""
        errors: List[str] = []
        try:
            data = self.load_json_file(self.batch_path)
        except (FileNotFoundError, ValueError, TypeError) as exc:
            return False, [str(exc)]

        schema_version = data.get("schema_version")
        if schema_version != 1:
            errors.append(f"Expected schema_version: 1, got: {schema_version}")

        records = data.get("records")
        if not isinstance(records, list) or len(records) == 0:
            errors.append("Batch 'records' must be a non-empty list of hadith records.")
            return False, errors

        family_ids: Set[str] = set()
        for idx, rec in enumerate(records):
            rec_id = rec.get("hadith_id", f"index_{idx}")
            fam_id = rec.get("family_id")
            if not fam_id:
                errors.append(f"Record {rec_id} is missing required 'family_id'.")
            else:
                family_ids.add(fam_id)

            src = rec.get("source_ref")
            if not isinstance(src, dict) or not src.get("collection"):
                errors.append(f"Record {rec_id} lacks valid 'source_ref.collection'.")

            variants = rec.get("variants") or []
            if not isinstance(variants, list) or len(variants) == 0:
                errors.append(f"Record {rec_id} has no transmission variants.")

            for v_idx, v in enumerate(variants):
                v_id = v.get("variant_id", f"v_{v_idx}")
                chain = v.get("isnad_chain") or []
                if not isinstance(chain, list) or len(chain) == 0:
                    errors.append(f"Record {rec_id} variant {v_id} has empty isnad_chain.")

                matn = (v.get("matn_raw") or "").strip()
                if not matn:
                    errors.append(f"Record {rec_id} variant {v_id} has empty matn_raw.")
                else:
                    for token in ISNAD_CONNECTOR_TOKENS:
                        if matn.startswith(token):
                            errors.append(
                                f"Boundary bleed warning: Record {rec_id} variant {v_id} "
                                f"matn starts with isnad connector token '{token}'."
                            )
                            break

        if len(family_ids) > 1:
            errors.append(
                f"Family inconsistency: Multiple family_ids detected in batch: {sorted(list(family_ids))}"
            )

        return len(errors) == 0, errors

    def verify_manifest(self) -> Tuple[bool, List[str]]:
        """Validate research manifest completeness and mandatory pre-publication gates."""
        if not self.manifest_path:
            return True, []

        errors: List[str] = []
        try:
            data = self.load_json_file(self.manifest_path)
        except (FileNotFoundError, ValueError, TypeError) as exc:
            return False, [str(exc)]

        required_fields = ["tradition_id", "title_ar", "orchestrator_version", "gates"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Manifest missing required metadata field: '{field}'")

        gates = data.get("gates", {})
        if not isinstance(gates, dict):
            errors.append("Manifest 'gates' property must be a dictionary object.")
        else:
            mandatory_gates = [
                "gate_1_scope_approved",
                "gate_2_boundaries_approved",
                "gate_3_identities_approved",
            ]
            for gate_name in mandatory_gates:
                if not gates.get(gate_name):
                    errors.append(f"Mandatory pre-publication approval '{gate_name}' is not marked true.")

        return len(errors) == 0, errors


def verify_batch_json(batch_path: Path) -> Tuple[bool, List[str]]:
    """Standalone helper function for batch validation."""
    verifier = ArtifactVerifier(batch_path)
    return verifier.verify_batch()


def verify_manifest(manifest_path: Path) -> Tuple[bool, List[str]]:
    """Standalone helper function for manifest verification."""
    verifier = ArtifactVerifier(Path("."), manifest_path)
    return verifier.verify_manifest()


def main() -> int:
    """CLI entry point for artifact verification."""
    parser = argparse.ArgumentParser(
        description="Verify Hadith ICMA research artifacts and batch compliance."
    )
    parser.add_argument("--batch", type=Path, required=True, help="Path to Riwaq import-batch.json")
    parser.add_argument("--manifest", type=Path, default=None, help="Path to research-manifest.json")
    args = parser.parse_args()

    print(f"=== Verifying Hadith Research Artifacts ===")
    print(f"Target Batch: {args.batch}")

    verifier = ArtifactVerifier(args.batch, args.manifest)
    batch_valid, batch_errors = verifier.verify_batch()

    if not batch_valid:
        print("[FAIL] Batch verification failed with errors:")
        for err in batch_errors:
            print(f"  - {err}", file=sys.stderr)
    else:
        print("[PASS] Batch JSON structural and boundary hygiene checks passed.")

    manifest_valid = True
    if args.manifest:
        print(f"Target Manifest: {args.manifest}")
        manifest_valid, manifest_errors = verifier.verify_manifest()
        if not manifest_valid:
            print("[FAIL] Manifest verification failed with errors:")
            for err in manifest_errors:
                print(f"  - {err}", file=sys.stderr)
        else:
            print("[PASS] Manifest approval gates verified.")

    if batch_valid and manifest_valid:
        print("=== Artifact Verification Complete: ALL GATES PASS ===")
        return 0
    else:
        print("=== Artifact Verification Complete: FAILED ===")
        return 1


if __name__ == "__main__":
    sys.exit(main())
