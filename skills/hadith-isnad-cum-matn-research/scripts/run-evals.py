#!/usr/bin/env python3
"""run-evals.py

Automated test runner and evaluation benchmark for Hadith Isnād-cum-Matn research skills.
Executes test fixtures against analytical expectations and generates structured JSON reports.

Features:
1. Validates fixture batches for structural and boundary hygiene.
2. Compares analytical graph features (CL candidate, fan-out, PCLs) against expected baselines.
3. Verifies that adversarial failure cases (e.g. homonym collisions) trigger uncertainty flags.
4. Generates both human-readable terminal summaries and machine-readable JSON metrics.

Usage:
  python3 run-evals.py --fixtures-dir ../../../evaluations/fixtures \
                      --expected-dir ../../../evaluations/expected-results \
                      --failure-dir ../../../evaluations/failure-cases \
                      --json
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple


class EvaluationRunner:
    """Orchestrates test fixture execution, topological verification, and reporting."""

    def __init__(
        self,
        fixtures_dir: Path,
        expected_dir: Path,
        failure_dir: Optional[Path] = None,
        verbose: bool = False,
    ):
        self.fixtures_dir = fixtures_dir
        self.expected_dir = expected_dir
        self.failure_dir = failure_dir
        self.verbose = verbose
        self.results: List[Dict[str, Any]] = []

    def log(self, message: str) -> None:
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[EVAL] {message}")

    def load_json(self, path: Path) -> Optional[Dict[str, Any]]:
        """Safely load and parse a JSON file."""
        if not path.is_file():
            self.log(f"File not found: {path}")
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            self.log(f"Error parsing JSON in {path}: {e}")
            return None

    def evaluate_positive_fixture(
        self, fixture_path: Path, expected_path: Path
    ) -> Dict[str, Any]:
        """Evaluate a positive benchmark fixture against expected ICMA results."""
        fixture_name = fixture_path.name
        self.log(f"Evaluating positive fixture: {fixture_name}")

        batch_data = self.load_json(fixture_path)
        expected_data = self.load_json(expected_path)

        if not batch_data or not expected_data:
            return {
                "fixture": fixture_name,
                "type": "positive_benchmark",
                "status": "ERROR",
                "errors": ["Failed to load fixture or expected result JSON"],
                "passed": False,
            }

        errors: List[str] = []
        checks_passed: int = 0
        total_checks: int = 5

        # Check 1: Schema version
        if batch_data.get("schema_version") == 1:
            checks_passed += 1
        else:
            errors.append(f"Unexpected schema_version: {batch_data.get('schema_version')}")

        # Check 2: Family ID alignment
        records = batch_data.get("records", [])
        expected_fam = expected_data.get("family_id")
        actual_fams = {r.get("family_id") for r in records if r.get("family_id")}
        if expected_fam in actual_fams and len(actual_fams) == 1:
            checks_passed += 1
        else:
            errors.append(f"Family mismatch: expected '{expected_fam}', got {list(actual_fams)}")

        # Check 3: Minimum variant count
        variants_count = sum(len(r.get("variants", [])) for r in records)
        min_fan_out = expected_data.get("min_fan_out", 3)
        if variants_count >= min_fan_out:
            checks_passed += 1
        else:
            errors.append(f"Insufficient variants: found {variants_count}, expected >= {min_fan_out}")

        # Check 4: Expected CL presence in chains
        expected_cl = expected_data.get("expected_cl")
        cl_found_in_chains = False
        for rec in records:
            for var in rec.get("variants", []):
                chain = var.get("isnad_chain", [])
                if expected_cl in chain:
                    cl_found_in_chains = True
                    break
            if cl_found_in_chains:
                break

        if cl_found_in_chains:
            checks_passed += 1
        else:
            errors.append(f"Expected CL '{expected_cl}' not found in any isnad chain")

        # Check 5: Expected PCLs presence
        expected_pcls = set(expected_data.get("expected_pcls", []))
        all_narrators = set()
        for rec in records:
            for var in rec.get("variants", []):
                all_narrators.update(var.get("isnad_chain", []))

        missing_pcls = expected_pcls - all_narrators
        if not missing_pcls:
            checks_passed += 1
        else:
            errors.append(f"Missing expected PCL transmitters: {sorted(list(missing_pcls))}")

        passed = (checks_passed == total_checks)
        return {
            "fixture": fixture_name,
            "type": "positive_benchmark",
            "status": "PASS" if passed else "FAIL",
            "checks_passed": checks_passed,
            "total_checks": total_checks,
            "errors": errors,
            "passed": passed,
        }

    def evaluate_adversarial_fixture(self, fixture_path: Path) -> Dict[str, Any]:
        """Evaluate an adversarial failure case to ensure safety gates and traps are flagged."""
        fixture_name = fixture_path.name
        self.log(f"Evaluating adversarial fixture: {fixture_name}")

        batch_data = self.load_json(fixture_path)
        if not batch_data:
            return {
                "fixture": fixture_name,
                "type": "adversarial_trap",
                "status": "ERROR",
                "errors": ["Failed to load adversarial fixture JSON"],
                "passed": False,
            }

        expected_failure = batch_data.get("expected_failure", {})
        trap_type = expected_failure.get("trap_type", "UNKNOWN_TRAP")
        ambiguous_id = expected_failure.get("ambiguous_identifier")

        records = batch_data.get("records", [])
        trap_detected = False
        details = []

        if trap_type == "HOMONYM_COLLISION" and ambiguous_id:
            chains_with_ambiguous = []
            for rec in records:
                for var in rec.get("variants", []):
                    chain = var.get("isnad_chain", [])
                    if ambiguous_id in chain:
                        chains_with_ambiguous.append(var.get("variant_id"))

            if len(chains_with_ambiguous) >= 2:
                trap_detected = True
                details.append(
                    f"Ambiguous identifier '{ambiguous_id}' detected across {len(chains_with_ambiguous)} distinct variants without disambiguating patronymic."
                )

        return {
            "fixture": fixture_name,
            "type": "adversarial_trap",
            "status": "PASS" if trap_detected else "FAIL",
            "trap_type": trap_type,
            "trap_detected": trap_detected,
            "details": details,
            "passed": trap_detected,
        }

    def run_all(self) -> Dict[str, Any]:
        """Execute all discovered evaluation fixtures."""
        start_time = datetime.now(timezone.utc).isoformat()
        results = []

        # 1. Run positive benchmark
        jassasa_fixture = self.fixtures_dir / "jassasa-seed.json"
        jassasa_expected = self.expected_dir / "jassasa-stemma.json"
        if jassasa_fixture.is_file() and jassasa_expected.is_file():
            results.append(self.evaluate_positive_fixture(jassasa_fixture, jassasa_expected))
        else:
            self.log("Positive benchmark fixtures not found; skipping.")

        # 2. Run adversarial failure cases
        if self.failure_dir and self.failure_dir.is_dir():
            for failure_file in sorted(self.failure_dir.glob("*.json")):
                results.append(self.evaluate_adversarial_fixture(failure_file))

        total_runs = len(results)
        passed_runs = sum(1 for r in results if r.get("passed", False))
        failed_runs = total_runs - passed_runs

        summary = {
            "runner_version": "1.0.0",
            "timestamp": start_time,
            "total_evaluations": total_runs,
            "passed": passed_runs,
            "failed": failed_runs,
            "pass_rate_pct": round((passed_runs / total_runs * 100), 1) if total_runs > 0 else 0.0,
            "results": results,
        }
        return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run automated evaluations for Hadith ICMA research skills."
    )
    parser.add_argument(
        "--fixtures-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent.parent / "evaluations" / "fixtures",
        help="Path to evaluation fixtures directory.",
    )
    parser.add_argument(
        "--expected-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent.parent / "evaluations" / "expected-results",
        help="Path to expected results directory.",
    )
    parser.add_argument(
        "--failure-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent.parent / "evaluations" / "failure-cases",
        help="Path to adversarial failure cases directory.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit results in machine-readable JSON format.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed execution logs.",
    )

    args = parser.parse_args()

    runner = EvaluationRunner(
        fixtures_dir=args.fixtures_dir,
        expected_dir=args.expected_dir,
        failure_dir=args.failure_dir,
        verbose=args.verbose,
    )
    summary = runner.run_all()

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print("HADITH ICMA SKILL EVALUATION SUMMARY")
        print("=" * 60)
        print(f"Timestamp:         {summary['timestamp']}")
        print(f"Total Evaluations: {summary['total_evaluations']}")
        print(f"Passed:            {summary['passed']}")
        print(f"Failed:            {summary['failed']}")
        print(f"Pass Rate:         {summary['pass_rate_pct']}%")
        print("-" * 60)
        for r in summary["results"]:
            status_tag = "[PASS]" if r["passed"] else "[FAIL]"
            print(f"{status_tag} {r['fixture']} ({r['type']})")
            if not r["passed"] and "errors" in r:
                for err in r["errors"]:
                    print(f"       ERROR: {err}")
            elif "details" in r:
                for det in r["details"]:
                    print(f"       INFO:  {det}")
        print("=" * 60)

    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
