---
name: hadith-isnad-cum-matn-research
description: >
  Conduct comprehensive, evidence-based isnad-cum-matn research orchestrating Masar for
  takhrij and corpus curation and Riwaq for ICMA stemma analysis. Use when researchers
  request full historical investigation of a hadith tradition, variant discovery,
  stemma reconstruction, common link detection, or reproducible scholarly dossiers.
license: MIT
metadata:
  version: 1.2.0
  author: masar-riwaq-core
  category: hadith-studies
  domain: islamic-scholarship
  tier: STANDARD
  updated: 2026-10-28
  tags:
    - hadith
    - icma
    - isnad-cum-matn
    - takhrij
    - riwaq
    - masar
    - stemma-analysis
---

# Hadith Isnād-cum-Matn Research (Orchestrator)

An orchestrator skill that automates end-to-end, reproducible isnād-cum-matn investigations. It bridges **Masar** (upstream takhrīj, pericope alignment, boundary correction, and corpus curation) with **Riwaq** (topological graph derivation, Common Link detection, matn variance apparatus, and evidence-gated reporting) under rigorous scholarly standards.

---

## Overview

Modern digital hadith studies require both high-recall variant discovery across vast corpora and high-precision stemma graph analysis. This skill formalizes that dual workflow into a repeatable, 8-phase research pipeline with 4 human-in-the-loop approval gates.

By enforcing the unidirectional pipeline of meaning ($L_0$ Evidence $\to$ $L_9$ Projection), the agent ensures that computational findings are bound directly to primary witnesses without hallucinatory textual drift or unverified identity merges.

---

## Core Capabilities

- **Corpus Variant Gathering (*Takhrīj*)**: Multi-signal discovery across Sunni and Shīʿī collections, identifying lexical, semantic, and pericope variants.
- **Accretive Corpus Curation**: Non-destructive boundary bleed repair and external witness ingestion persisted to `masar-curated.db`.
- **Topological Stemma Derivation**: Directed Acyclic Graph (DAG) generation, Common Link (CL) scoring, and Partial Common Link (PCL) identification.
- **Matn Pericope Alignment**: Multi-branch textual variance apparatus tracking linguistic development across transmission generations.
- **Rival Hypothesis Discrimination**: Formal decision rules distinguishing historical originators from retrospective isnād projection (*al-rafʿ*).
- **Automated Artifact Verification**: Built-in AST validation and test execution verifying schema compliance, boundary hygiene, and gate signatures.

---

## When to Use

Activate this skill when:
- A researcher requests a comprehensive historical investigation of a ḥadīth tradition (e.g., *"Conduct an isnād-cum-matn analysis of the ḥadīth of al-Jassāsah"*).
- Analyzing the historical dating, geographic transmission, or common ancestry of parallel variants.
- Reconstructing a transmission stemma and identifying Common Links and Partial Common Links.
- Auditing an existing publication's claims against underlying textual witnesses.
- Preparing an import batch for Riwaq from unbundled digital corpora.

## When NOT to Use

Do not activate this skill for:
- Routine, non-analytical database lookups of a single ḥadīth translation (use raw database queries).
- Theological or legal rulings (*fatwā*) unrelated to transmission history or textual criticism.
- Generic NLP text summarization that does not require isnād modeling.

---

## Clarify First

Before initiating an investigation, resolve the following parameters with the researcher:
1. **Target Tradition & Seed Text**: What is the primary Arabic incipit or subject matter?
2. **Corpus Scope**: Should discovery cover Sunni canonical works only, Musannafs, Shīʿī al-Arbaʿah, or cross-sectarian corpora?
3. **Analytical Profile**: Standard topological analysis (`structural_only`) or biographical weighting (`reliability_weighted`)?
4. **Research Target**: Are we investigating a specific verbal formulation (*lafẓ*) or an entire thematic complex (*maʿnā*)?

---

## Quick Start

### 1. Verification of Research Environment

Verify system health and installed engines:
```bash
# Check Masar Takhrīj Engine health
masar diagnose

# Inspect Riwaq capability manifest across L0-L9
node /path/to/riwaq/scripts/riwaq-cli.mjs manifest
```

### 2. Run Automated Artifact Verification

Verify that all research artifacts, schema versions, and unit tests pass before generating reports:
```bash
# Verify import batch structure and boundary hygiene
python3 scripts/verify-artifacts.py --batch ../../evaluations/fixtures/jassasa-seed.json

# Execute full evaluation suite against benchmark baselines
python3 scripts/run-evals.py --verbose

# Run internal unit test suite
python3 -m unittest tests/test_verify_artifacts.py
```

---

## Tools & Scripts

| Tool / Script | Execution Command | Purpose |
| :--- | :--- | :--- |
| `verify-artifacts.py` | `python3 scripts/verify-artifacts.py --batch <file>` | Validates Riwaq `schema_version: 1`, boundary hygiene, and manifest gates. |
| `run-evals.py` | `python3 scripts/run-evals.py [--json]` | Runs benchmark fixtures against expected stemma baselines and traps. |
| `test_verify_artifacts.py` | `python3 -m unittest tests/test_verify_artifacts.py` | Executes unit tests for schema parsing and gate verification. |
| `masar` CLI | `masar search --seed <text> --compact` | High-density candidate discovery and boundary slice editing. |
| `riwaq-cli.mjs` | `node scripts/riwaq-cli.mjs pipeline <file>` | One-shot execution of validation, quality gates, and CL/PCL analysis. |

---

## Workflows: The 8-Phase Research Pipeline

```text
[Phase 1: Research Plan] ──► ◆ APPROVAL GATE 1 (Scope & Hypotheses)
         │
[Phase 2: Masar Discovery]
         │
[Phase 3: Corpus Curation] ──► ◆ APPROVAL GATE 2 (Boundaries & Quarantines)
         │
[Phase 4: Riwaq Batch Intake]
         │
[Phase 5: Structural Analysis] ──► ◆ APPROVAL GATE 3 (Transmitter Disambiguation)
         │
[Phase 6: Matn Pericopes]
         │
[Phase 7: Rival Hypotheses]
         │
[Phase 8: Scholarly Dossier] ──► ◆ APPROVAL GATE 4 (Publication Release)
```

### Phase 1: Define Problem & Scope
- Formulate central historical questions and hypotheses.
- Initialize `assets/research-plan.md` and `assets/research-manifest.json`.
- **◆ APPROVAL GATE 1**: Researcher signs off on tradition boundaries and corpus scope.

### Phase 2: Discover Witnesses via Masar
- Execute 4-signal search (`masar_search` or `masar search --format json --receipts`).
- Isolate and quarantine items marked `[TRAP]` (topical false positives).
- Record candidates in `assets/witness-matrix.csv`.

### Phase 3: Verify & Curate Corpus in Accretive Store
- Inspect each candidate with `masar_inspect`.
- Correct boundary bleed using `masar_adjust_split` (saved to `masar-curated.db`).
- Ingest external folios or missing citations via `masar_add_manual`.
- **◆ APPROVAL GATE 2**: Researcher reviews boundary adjustments and quarantined candidates.

### Phase 4: Transfer Verified Corpus to Riwaq
- Validate preflight gates (`GateSchema`, `GateFamilyConsistency`, `GateBoundaryHygiene`, `GateIsnadIntegrity`).
- Generate `import-batch.json` and validate with `riwaq_validate`.

### Phase 5: Execute Structural Analysis in Riwaq
- Execute `riwaq_analyze` under `structural_only` profile.
- Evaluate CL and PCL candidates, fan-out degree, and collector diversity.
- If transmitter homonyms appear, stage resolution proposals via `riwaq_stage_proposal`.
- **◆ APPROVAL GATE 3**: Review staged proposals; commit approved resolutions with `riwaq_commit_proposal`.

### Phase 6: Perform Matn Analysis & Pericope Distribution
- Align pericopes across transmission branches to test textual correlation.
- Test whether specific phrases correlate with particular PCLs or regional centers.
- If matn segmentation is not conducted, report textual coherence as *unmeasured*.

### Phase 7: Formulate & Test Competing Hypotheses
- Evaluate competing explanations:
  - *Hypothesis A*: First systematic circulation by the Common Link.
  - *Hypothesis B*: Pre-CL circulation with partial stemma loss.
  - *Hypothesis C*: Retrospective isnād projection (*rafʿ* / *idrāj*).
- Perform sensitivity sweeps under alternative narrator identifications.

### Phase 8: Assemble Reproducible Scholarly Dossier
- Verify release criteria with `riwaq_export` (checking `canExport()`).
- Run `verify-artifacts.py` against all generated outputs.
- Compile final dossier including witness matrix, stemma DAG, apparatus, and audit trail.
- **◆ APPROVAL GATE 4**: Present complete dossier and SHA-256 seal for publication release.

---

## Detailed Tool Usage & Practical Examples

### Example 1: Masar Discovery with Receipts
When calling `masar_search`, inspect candidate receipts to filter out topical false positives:
```json
{
  "seed": "فلقيتهم دابة أهلب كثير الشعر لا يدرى قبله من دبره",
  "scope": "all",
  "limit": 15
}
```
If `receipt.is_topical_false_positive` is `true`, leave the record in quarantine unless parallel isnāds confirm membership.

### Example 2: Boundary Bleed Repair
When CRF boundary bleed is detected in an inspected witness:
```json
{
  "hadith_id": "muslim_2942a",
  "start": 142,
  "end": 285
}
```
This sets the matn slice boundary in `masar-curated.db` without mutating the base corpus database.

### Example 3: Proposal Staging in Riwaq
To disambiguate two transmitters sharing the name *Hammad*:
```json
{
  "filePath": "evaluations/fixtures/homonym-trap.json",
  "type": "PROPOSAL_NARRATOR_SPLIT",
  "payload": {
    "sourceId": "hammad",
    "splitTargets": ["hammad_ibn_salamah", "hammad_ibn_zayd"],
    "rule": "Affan transmits from Hammad ibn Salamah; Sulayman from Hammad ibn Zayd"
  },
  "rationale": "Biographical consensus in Tahdhib al-Kamal verifies distinct teachers"
}
```

---

## Anti-Patterns & Common Traps

| Anti-Pattern | Severity | Remediation |
| :--- | :--- | :--- |
| **Topical False Positive Conflation** | Critical | Never bundle hadiths sharing legal themes without pericope overlap or isnād convergence. |
| **Silent Transmitter Merges** | Critical | Never merge homonyms (e.g., bare *Hammad*) without explicit biographical confirmation; stage in `ProposalStore`. |
| **Spider Line Over-Interpretation** | High | Never present the single strand preceding the CL as historically corroborated by stemma analysis alone. |
| **CRF Boundary Bleed Passthrough** | High | Never export uninspected records with isnād verbs (`حدثنا`) inside the matn; adjust via `masar_adjust_split`. |
| **Conflating Score with Authenticity** | High | Never interpret topological CL scores as "percentage probability of prophetic origin". |

---

## System Invariants & Epistemic Boundaries

1. **L0 Immutability**: Reported witness text from primary collections is never altered.
2. **Reversible Mutations**: All curate actions save to accretive overlays and session journals.
3. **Deterministic Verification**: Every generated artifact must be verifiable via `verify-artifacts.py`.

---

## References & Documentation

Progressively load detailed reference documents as required:
- **Methodology**: [`references/methodology.md`](references/methodology.md) — Mathematical graph criteria and pericope apparatus.
- **Evidence Standards**: [`references/evidence-standards.md`](references/evidence-standards.md) — The 8 operational principles and epistemic lattice.
- **Masar Interface**: [`references/masar-interface.md`](references/masar-interface.md) — Typed MCP and CLI contracts for Masar.
- **Riwaq Interface**: [`references/riwaq-interface.md`](references/riwaq-interface.md) — Typed MCP and CLI contracts for Riwaq.
- **Interpretation Rules**: [`references/interpretation-rules.md`](references/interpretation-rules.md) — Evaluating rival historical hypotheses.
- **Walkthrough Example**: [`examples/example-research-flow.md`](examples/example-research-flow.md) — End-to-end research session log.
