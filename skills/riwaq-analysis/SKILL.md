---
name: riwaq-analysis
description: >
  Execute isnad-cum-matn analysis (ICMA), stemma DAG generation, common link (CL/PCL)
  detection, and evidence-gated scholarly reporting using Riwaq. Use when validating
  import batches (schema_version: 1), running structural transmission analysis, staging
  transmitter identity proposals, or generating publishable research dossiers.
license: MIT
metadata:
  version: 1.1.0
  author: masar-riwaq-core
  category: hadith-studies
  domain: transmission-analysis
  tier: BASIC
  updated: 2026-10-28
  tags:
    - hadith
    - icma
    - riwaq
    - common-link
    - stemma-analysis
---

# Riwaq ICMA Transmission & Stemma Analysis

Riwaq (رواق) is a computational engine for Isnād-cum-Matn Analysis (ICMA). It models ḥadīth transmission as directed acyclic graphs (DAGs), identifies Common Links (CL) and Partial Common Links (PCL), aligns matn pericopes, binds analytical claims to primary evidence, and enforces strict pre-publication gates.

---

## Overview

Riwaq formalizes the mathematical and topological rules of isnād-cum-matn analysis into an auditable 10-layer abstraction tower ($L_0 \to L_9$). Downstream layers derive information strictly from validated upstream primitives and are forbidden from mutating raw source evidence.

---

## Core Capabilities

- **Strict Schema Validation**: Validates incoming batches against Riwaq `schema_version: 1` (`import-batch.json`).
- **Directed Acyclic Graph (DAG) Modeling**: Constructs formal transmission graphs from ordered narrator chains.
- **Topological CL/PCL Detection**: Evaluates candidate nodes for branch fan-out, collector diversity, and corroboration depth.
- **Non-Destructive Proposal Staging**: Stages AI interventions (narrator merges/splits and matn segmentation) in `ProposalStore` before human approval.
- **Publication Release Gating**: Prohibits export generation unless all evidence bindings pass the `canExport()` check.

---

## When to Use

Trigger this skill whenever an agent must:
- Validate an import batch against `schema_version: 1` (`import-batch.json`).
- Run topological analysis to identify Common Links (CL), Partial Common Links (PCL), and transmission fan-out.
- Inspect cross-layer health across the 10-layer abstraction tower ($L_0 \to L_9$).
- Non-destructively stage transmitter identity resolution (merges/splits) or matn segmentation in the `ProposalStore`.
- Commit verified researcher approvals and mint immutable SHA-256 operation receipts.
- Run anti-hallucination sweeps to verify citations, narrator chains, and evidence bindings.
- Generate canonical reports and export publication artifacts (Markdown, DOCX, PDF).

## When NOT to Use

Do not use this skill for:
- Initial variant searching across large uncurated collections (use `masar-takhrij`).
- Reinterpreting raw texts without schema-validated batch structures.

---

## The 10-Layer Abstraction Tower

Riwaq enforces a strict unidirectional pipeline of meaning:

| Layer | Semantic Role | Module Owner | Critical Invariant |
| :--- | :--- | :--- | :--- |
| **$L_0$ Evidence** | Source witnesses, manuscript citations, raw texts | Imported records | Absolute immutability of reported witness text. |
| **$L_1$ Intake** | Validated, normalized batch structure | `json-validator.js` | Invalid structure cannot masquerade as canonical data. |
| **$L_2$ Identity** | Canonical narrator identities, aliases, merges | `entity-resolution.js` | No orphan IDs, silent merges, or unreceipted mutations. |
| **$L_3$ Transmission** | Families, variants, narrator chains, pericopes | Canonical batch | Family and variant boundaries remain explicit. |
| **$L_4$ Graph/Features** | Nodes, edges, fan-out, chronology, coverage | `clpcl-analyzer.js` | Pure mathematical derivation from family data. |
| **$L_5$ Interpretation** | CL/PCL candidates, scores, profile classification | `clpcl-analyzer.js` | Methodology is explicit; map data remains method-agnostic. |
| **$L_6$ Claim Validity**| Evidence bindings, rule violations, proceed/block | `evidence-binding.js` | Reliability claims require verifiable primary evidence. |
| **$L_7$ Explanation** | Audit trail, structural uncertainty, weak paths | `explainability.js` | Uncertainty remains visible; never collapsed away. |
| **$L_8$ Report** | Unified family-level analytical representation | `canonical-report.js` | Single semantic source for all human exports. |
| **$L_9$ Projection** | Markdown, DOCX, PDF, CLI JSON, MCP | Exporter modules | Projections format; they do not reinterpret. |

---

## Control-Semantics Taxonomy

Always type every control signal before acting:

1. **Observational Signal**: Informational metrics (e.g., quality scores, diagnostic warnings). Does *not* block execution unless explicitly wired into a gate.
2. **Blocking Precondition**: Structural requirements (e.g., JSON schema failure, missing required fields). Halts downstream operations immediately.
3. **Analytical State**: Algorithmic classification (e.g., `family_status: cl_detected` vs. `pcl_only` vs. `insufficient_data`). Represents mathematical findings, not historical authenticity.
4. **Publication Gate**: Hard release check (`CanonicalReport.canExport()`). If false, publishing/exporting is strictly refused until violations are resolved.
5. **Projection**: Rendered outputs (Markdown, DOCX). Exporters must preserve canonical report semantics without editorial drift.

---

## Tool & Interface Contracts

### 1. Model Context Protocol (MCP) Tools

When connected to `scripts/riwaq-mcp.mjs` over stdio JSON-RPC 2.0:

| Tool | Parameters | Purpose & Output |
| :--- | :--- | :--- |
| `riwaq_manifest` | *(none)* | Emits machine-readable contract manifest across layers $L_0 \to L_9$. |
| `riwaq_diagnose` | `filePath` (string, required)<br>`profile` ("structural_only" \| "reliability_weighted")<br>`withReliability` (boolean) | Evaluates cross-layer health ($L_1 \to L_8$) and outputs typed remediation prescriptions. |
| `riwaq_validate` | `filePath` (string, required) | Validates batch schema, required provenance fields, and anti-hallucination invariants. |
| `riwaq_analyze` | `filePath` (string, required)<br>`profile` ("structural_only" \| "reliability_weighted")<br>`withReliability` (boolean) | Runs graph derivation and CL/PCL scoring across all families in the batch. |
| `riwaq_stage_proposal` | `filePath` (string, required)<br>`type` (enum)<br>`payload` (object)<br>`rationale` (string) | Stages non-destructive candidate interventions in `ProposalStore`. |
| `riwaq_commit_proposal` | `filePath` (string, required)<br>`proposalId` (string)<br>`reviewerId` (string)<br>`notes` (string) | Applies an approved proposal to canonical state and mints an immutable SHA-256 receipt. |
| `riwaq_export` | `filePath` (string, required)<br>`profile` ("structural_only" \| "reliability_weighted") | Generates publishable Markdown report (enforces `canExport()` gate). |

### 2. Machine CLI Commands

Execute via terminal within the Riwaq repository:

```bash
# 1. Validate schema and intake invariants (L1)
node scripts/riwaq-cli.mjs validate path/to/batch.json

# 2. Run pre-analysis anti-hallucination integrity sweep
node scripts/riwaq-cli.mjs hallucination path/to/batch.json

# 3. Automated cross-layer diagnosis with actionable remediation hints
node scripts/riwaq-cli.mjs diagnose path/to/batch.json

# 4. Topological analysis and CL/PCL classification (L4-L5)
node scripts/riwaq-cli.mjs analyze path/to/batch.json --profile structural_only

# 5. One-shot verification pipeline (validate -> gates -> AH -> report)
node scripts/riwaq-cli.mjs pipeline path/to/batch.json --profile structural_only

# 6. Export verified analytical report (Gated by canExport)
node scripts/riwaq-cli.mjs export path/to/batch.json --format md --out report.md

# 7. Integrity seal generation and verification
node scripts/riwaq-cli.mjs seal path/to/batch.json
node scripts/riwaq-cli.mjs verify-seal path/to/batch.json --manifest batch.json.seal.json
```

---

## Anti-Patterns

- **Direct Canonical Mutation**: Modifying imported narrator chains without staging through `ProposalStore`.
- **Bypassing canExport**: Forcing a markdown export when claim violations or unresolved doubts block publication.
- **Collapsing Uncertainty**: Treating an `uncertain` candidate as definitively disproven rather than flagging it for scholarly review.
