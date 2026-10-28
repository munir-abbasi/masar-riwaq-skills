# Hadith Research Skills Ecosystem (Masar & Riwaq)

A researcher-oriented agent skills ecosystem for disciplined, reproducible, and verifiable Isnād-cum-Matn Analysis (ICMA) of early Islamic traditions across arbitrary corpora.

This ecosystem connects and orchestrates two complementary open-source engines:
- **[Masar (مسار)](https://github.com/munir-abbasi/masar)**: High-precision Takhrīj, multi-signal variant discovery, CRF boundary bleed repair, and accretive corpus curation.
- **[Riwaq (رواق)](https://github.com/munir-abbasi/riwaq)**: 10-layer ICMA stemma engine, DAG transmission modeling, Common Link (CL/PCL) detection, and evidence-gated scholarly reporting.

Rather than merely providing scripts that execute commands, this ecosystem encodes rigorous scholarly methodology, evidentiary standards, progressive disclosure, and human-in-the-loop review controls.

---

## Architectural Division of Responsibilities

```
┌──────────────────────────────────────────────┐
│                    MASAR                     │
│    Discovery, Takhrij & Corpus Curation      │
│  GitHub: https://github.com/munir-abbasi/masar
│  - Multi-signal search (BM25, vector, isnad) │
│  - Topical false-positive quarantine         │
│  - CRF isnad/matn boundary repair            │
│  - Accretive overlay (masar-curated.db)      │
└──────────────────────┬───────────────────────┘
                       │
                       │ Schema-validated export batch
                       ▼ (schema_version: 1)
┌──────────────────────────────────────────────┐
│                    RIWAQ                     │
│    Transmission Stemma & Textual Analysis    │
│  GitHub: https://github.com/munir-abbasi/riwaq
│  - Directed Acyclic Graph (DAG) derivation   │
│  - Common Link (CL & PCL) detection          │
│  - Non-destructive proposal staging          │
│  - Publication gates (canExport)             │
└──────────────────────────────────────────────┘
```

**The Principal Invariant**: Masar establishes and verifies the textual corpus; Riwaq analyzes the resulting transmission evidence. Downstream analytical parameters in Riwaq must never be adjusted to compensate for an incomplete or noisy corpus extraction in Masar.

---

## Repository Structure

Following the open [Agent Skills Specification](https://github.com/agentskills/agentskills):

```text
masar-riwaq-skills/
├── skills/
│   ├── masar-takhrij/
│   │   └── SKILL.md                          # Application skill: variant discovery & boundary editing
│   │
│   ├── riwaq-analysis/
│   │   └── SKILL.md                          # Application skill: ICMA stemma & 10-layer abstraction tower
│   │
│   └── hadith-isnad-cum-matn-research/       # Core Mother Skill orchestrator (Tier: STANDARD)
│       ├── SKILL.md                          # 8-phase research workflow & approval gates (201 lines)
│       ├── README.md                         # Package documentation and CLI reference
│       ├── references/
│       │   ├── methodology.md                # Mathematical ICMA stemma & topological rules
│       │   ├── evidence-standards.md         # 8 operating principles & authority lattice
│       │   ├── interpretation-rules.md       # Evaluating competing historical hypotheses
│       │   ├── masar-interface.md            # Exact MCP & CLI interface contracts for Masar
│       │   └── riwaq-interface.md            # Exact MCP & CLI interface contracts for Riwaq
│       ├── scripts/
│       │   ├── verify-artifacts.py           # Validates batch schemas, hygiene, and manifest gates
│       │   └── run-evals.py                  # Executes benchmark fixtures and adversarial traps
│       ├── tests/
│       │   └── test_verify_artifacts.py      # Standard library unittest suite
│       ├── assets/
│       │   ├── research-plan.md              # Template for hadith research plans
│       │   ├── witness-matrix.csv            # Standard witness tracking table
│       │   └── research-manifest.json        # Research dossier manifest schema
│       ├── examples/
│       │   ├── example-research-flow.md      # Full end-to-end research session walkthrough
│       │   ├── sample-batch-input.json       # Minimal valid batch input
│       │   └── sample-mcp-calls.json         # JSON-RPC 2.0 tool invocation samples
│       └── expected_outputs/
│           ├── jassasa-analysis.json         # Reference Riwaq topological analysis
│           └── jassasa-dossier.md            # Reference scholarly research dossier
│
├── evaluations/
│   ├── fixtures/
│   │   └── jassasa-seed.json                 # Curated multi-variant import batch for Hadith al-Jassasah
│   ├── expected-results/
│   │   └── jassasa-stemma.json               # Benchmark topological findings (CL at al-Sha'bi)
│   └── failure-cases/
│       └── homonym-trap.json                 # Adversarial homonym collision test
│
└── README.md
```

---

## The 8 Non-Negotiable Scholarly Principles

1. **Zero Textual Fabrication**: Never invent a source witness, narrator, isnād chain, textual variant, or manuscript folio.
2. **Candidates ≠ Attestations**: Treat automated search results as candidates until individually verified.
3. **Dual Representation**: Preserve verbatim Arabic texts separately from normalized forms.
4. **No Silent Identity Merges**: Never merge ambiguous transmitters without corroborating biographical evidence.
5. **Schema Conformance ≠ Scholarly Verification**: Valid JSON structure does not constitute historical proof.
6. **No Probability Conflation**: Structural CL scores represent graph topological features, never historical probabilities of authenticity or fabrication.
7. **Strict Epistemic Typing**: Distinguish observations ($L_0$), structural derivations ($L_4$), historical hypotheses ($L_5$), and unresolved doubts ($L_7$).
8. **Provenance & Reproducibility**: Retain complete tool versions, queries, boundary modifications, and SHA-256 seals.

---

## The 4 Human-in-the-Loop Approval Gates

1. **◆ APPROVAL GATE 1 (Scope & Hypotheses)**: Executed after Phase 1 to confirm target tradition, scope of corpora, and candidate hypotheses with the researcher.
2. **◆ APPROVAL GATE 2 (Corpus Curation)**: Executed after Phase 3 to review proposed CRF boundary split corrections and quarantined false positives.
3. **◆ APPROVAL GATE 3 (Identity Resolution)**: Executed after Phase 5 to review non-destructively staged transmitter merges/splits in Riwaq's `ProposalStore` before committing.
4. **◆ APPROVAL GATE 4 (Publication Release)**: Executed after Phase 8 to inspect canonical report validity (`canExport()`) and verification script results before releasing the scholarly dossier.

---

## Quality & Validation Benchmark

Validated using [`engineering__skill-tester`](file:///home/meer/ai-tools/.unified_skills/engineering__skill-tester/SKILL.md):
- **Structural Compliance**: **95.2% (EXCELLENT)** — Meets STANDARD tier requirements with 0 errors.
- **Quality Score**: **78.4 / 100 (Grade B)** across all four dimensions:
  - Documentation: **85.0%**
  - Completeness: **84.0%**
  - Usability: **74.0%**
  - Code Quality: **70.5%**
- **Evaluation Suite**: **100% Pass Rate** (`run-evals.py`).
- **Unit Test Suite**: **5/5 Passing** (`test_verify_artifacts.py`).

---

## Quick Start & Verification

```bash
# 1. Run unit test suite
python3 -m unittest skills/hadith-isnad-cum-matn-research/tests/test_verify_artifacts.py

# 2. Run automated evaluation suite
python3 skills/hadith-isnad-cum-matn-research/scripts/run-evals.py

# 3. Verify single batch file against research manifest
python3 skills/hadith-isnad-cum-matn-research/scripts/verify-artifacts.py \
  --batch evaluations/fixtures/jassasa-seed.json \
  --manifest skills/hadith-isnad-cum-matn-research/assets/research-manifest.json
```
