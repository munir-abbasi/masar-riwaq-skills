# Hadith Isnād-cum-Matn Research Skill Package

[![Tier: POWERFUL](https://img.shields.io/badge/Tier-POWERFUL-blue.svg)](references/methodology.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Verification: PASS](https://img.shields.io/badge/Verification-PASS-brightgreen.svg)](scripts/run-evals.py)

A production-grade, researcher-oriented Agent Skill package for orchestrating end-to-end Isnād-cum-Matn Analysis (ICMA) across Masar and Riwaq.

---

## Directory Structure

```text
hadith-isnad-cum-matn-research/
├── SKILL.md                          # Primary agent instructions (<500 lines)
├── README.md                         # Package documentation and CLI reference
├── references/                       # Progressive disclosure documentation
│   ├── methodology.md                # ICMA stemma mathematics and topological rules
│   ├── evidence-standards.md         # 8 operational principles and epistemic lattice
│   ├── interpretation-rules.md       # Decision rules for competing historical hypotheses
│   ├── masar-interface.md            # Exact MCP & CLI interface contracts for Masar
│   └── riwaq-interface.md            # Exact MCP & CLI interface contracts for Riwaq
├── scripts/                          # Deterministic Python CLI tools (stdlib only)
│   ├── verify-artifacts.py           # Validates batch schemas, hygiene, and manifest gates
│   └── run-evals.py                  # Executes benchmark fixtures and adversarial traps
├── assets/                           # Reusable research templates
│   ├── research-plan.md              # Template for hadith research plans
│   ├── witness-matrix.csv            # Standard witness tracking table
│   └── research-manifest.json        # Research dossier manifest schema
└── expected_outputs/                 # Golden evaluation outputs
    ├── jassasa-analysis.json         # Reference Riwaq topological analysis
    └── jassasa-dossier.md            # Reference scholarly research dossier
```

---

## Prerequisites & Installation

The skill package relies strictly on standard Python libraries (Python 3.10+) and requires no external third-party dependencies for verification.

### System Requirements
- Python 3.10 or later
- Node.js 18 or later (for executing Riwaq CLI tools)
- Masar environment (`uv run masar` or local CLI)

---

## Command Reference & Usage

### 1. Artifact Verification (`verify-artifacts.py`)

Validates an exported Riwaq JSON batch for schema conformance (`schema_version: 1`), boundary hygiene (no isnād connectors in matn slices), and research manifest approval gate completeness.

```bash
python3 scripts/verify-artifacts.py \
  --batch ../../../evaluations/fixtures/jassasa-seed.json \
  --manifest assets/research-manifest.json
```

#### Parameters:
| Flag | Type | Description |
| :--- | :--- | :--- |
| `--batch` | `Path` (Required) | Path to Riwaq import batch JSON file. |
| `--manifest` | `Path` (Optional) | Path to research manifest JSON file to verify approval gates. |

### 2. Automated Evaluation Suite (`run-evals.py`)

Runs comprehensive benchmark fixtures against expected topological baselines and verifies that adversarial traps (e.g., narrator homonym collisions) are properly flagged.

```bash
# Human-readable summary output
python3 scripts/run-evals.py

# Machine-readable JSON metrics for CI/CD integration
python3 scripts/run-evals.py --json
```

#### Parameters:
| Flag | Type | Description |
| :--- | :--- | :--- |
| `--fixtures-dir` | `Path` | Directory containing input fixtures (default: `evaluations/fixtures`). |
| `--expected-dir` | `Path` | Directory containing expected results (default: `evaluations/expected-results`). |
| `--failure-dir` | `Path` | Directory containing adversarial failure cases (default: `evaluations/failure-cases`). |
| `--json` | `Flag` | Output results in machine-readable JSON format. |
| `--verbose`, `-v`| `Flag` | Output detailed execution logs during evaluation. |

---

## The 4 Approval Gates

1. **◆ APPROVAL GATE 1 (Scope & Hypotheses)**: Executed after Phase 1 to confirm target tradition, scope of corpora, and candidate hypotheses with the researcher.
2. **◆ APPROVAL GATE 2 (Corpus Curation)**: Executed after Phase 3 to review proposed CRF boundary split corrections and quarantined false positives.
3. **◆ APPROVAL GATE 3 (Identity Resolution)**: Executed after Phase 5 to review non-destructively staged transmitter merges/splits in Riwaq's `ProposalStore` before committing.
4. **◆ APPROVAL GATE 4 (Publication Release)**: Executed after Phase 8 to inspect canonical report validity (`canExport()`) and verification script results before releasing the scholarly dossier.

---

## Troubleshooting & Common Pitfalls

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| `Boundary bleed warning` in `verify-artifacts.py` | Isnād transition formula (`حدثنا`, `سمعت`) remained in the matn slice. | Use `masar split --id <id> --start <idx> --end <idx>` to adjust the slice. |
| `Family inconsistency` error | Records in the batch have different `family_id` values. | Ensure all records in a single batch belong to the same tradition family. |
| `PCL missing` failure in `run-evals.py` | Transmitter name spelling mismatch in the isnād chain. | Collate transmitter identifier against normalized names in `narrator-profile.json`. |
