---
name: masar-takhrij
description: >
  Discover hadith variants, repair CRF isnad/matn boundaries, resolve transmitter
  homonyms, and export verified transmission bundles using Masar. Use when discovering
  parallel traditions (takhrīj), aligning fragmented quotations (taqṭīʿ), quarantining
  topical false positives, or preparing schema-compliant import batches for Riwaq.
license: MIT
metadata:
  version: 1.1.0
  author: masar-riwaq-core
  category: hadith-studies
  domain: corpus-curation
  tier: BASIC
  updated: 2026-10-28
  tags:
    - hadith
    - takhrij
    - masar
    - corpus-curation
    - boundary-repair
---

# Masar Takhrīj & Corpus Curation

Masar (مسار) is a high-precision Hadith Takhrīj (variant discovery and bundling) engine serving as the upstream corpus feeder for Riwaq ICMA stemma analysis. It searches unbundled collections (Sunni and Shīʿī corpora, custom datasets, and manuscript transcriptions) and curates verified `family_id` bundles conforming to Riwaq `schema_version: 1` (`import-batch.json`).

---

## Overview

The primary bottleneck in digital isnād-cum-matn analysis is noisy upstream data: OCR errors, boundary bleed between isnād and matn, homonym collisions, and topical false positives. Masar resolves these challenges by combining a 4-signal discovery engine with a human-in-the-loop accretive curation layer (`masar-curated.db`).

---

## Core Capabilities

- **4-Signal Hybrid Discovery**: Combines lexical BM25, semantic embeddings, pericope alignment, and isnād filtering.
- **Topical False Positive Quarantine**: Automatically detects and quarantines thematic lookalikes (`[TRAP]`) that lack genealogical isnād convergence.
- **Accretive Boundary Repair**: Allows surgical 1-click adjustment of matn slices without altering the immutable base corpus (`corpus.db`).
- **Manuscript Ingestion**: Supports manual ingestion of raw unsegmented texts and external folios into existing family bundles.
- **Deterministic Preflight Gating**: Validates bundles against 4 strict gates before passing data to Riwaq.

---

## When to Use

Trigger this skill whenever an agent must:
- Discover textual and transmission variants (*takhrīj*) across canonical and regional hadith corpora.
- Detect and align fragmented quotations (*taqṭīʿ*) using sliding-window pericope matching.
- Identify semantic variants (*riwāyah bi-l-maʿnā*) without full lexical overlap.
- Repair automated parser boundaries (CRF isnād/matn boundary bleed) before analysis.
- Ingest external manuscript transcriptions or print citations into an existing family.
- Validate and export candidate bundles into Riwaq-compatible JSON batches.

## When NOT to Use

Do not use this skill for:
- Stemma graph analysis, Common Link calculation, or historical hypothesis evaluation (route to `riwaq-analysis`).
- Theological debates or jurisprudential rulings.

---

## Operating Principles & Invariants

1. **Discovery ≠ Canonical Truth**: Automated CRF parser boundaries are inherently noisy. Never export uninspected records where isnād connectors bleed into the matn or vice versa.
2. **Topical False Positive Quarantine**: High semantic similarity without lexical pericope overlap or isnād convergence is automatically quarantined as `TOPICAL_FALSE_POSITIVE`. Never release quarantined records without explicit textual evidence.
3. **Accretive Knowledge Overlay**: Base corpus databases (`corpus.db`) remain strictly immutable. All boundary splits, narrator tags, and manual additions persist to the accretive overlay (`masar-curated.db`).
4. **Deterministic Preflight Gating**: Every candidate export must pass all four deterministic gates:
   - `GateSchema`: Strict structural conformance with Riwaq `schema_version: 1`.
   - `GateFamilyConsistency`: All records share a single validated `family_id`.
   - `GateBoundaryHygiene`: No isnād connector tokens inside the matn slice.
   - `GateIsnadIntegrity`: Minimum transmitter chain depth ($\ge 1$) with valid identifiers.

---

## Tool & Interface Contracts

### 1. Model Context Protocol (MCP) Tools

When connected to `masar mcp` over stdio JSON-RPC 2.0:

| Tool | Parameters | Purpose & Output |
| :--- | :--- | :--- |
| `masar_search` | `seed` (string, required)<br>`scope` ("all" \| "sunni" \| "shia", default "all")<br>`limit` (int, default 10) | Executes 4-signal hybrid discovery. Returns candidate records with explainability receipts and quarantine flags. |
| `masar_inspect` | `hadith_id` (string, required) | Retrieves full text, parsed isnād chain, raw matn slice, collection metadata, and current boundary status. |
| `masar_adjust_split` | `hadith_id` (string, required)<br>`start` (int, required)<br>`end` (int, required) | Persists zero-based start and end indices of the matn slice to `masar-curated.db`. |
| `masar_add_manual` | `text` (string, required)<br>`collection` (string, required)<br>`ref` (string, required)<br>`family_id` (string, default "fam_manual") | Ingests unsegmented manuscript text, applies heuristic boundary detection, and logs an accretive record. |
| `masar_diagnose` | *(none)* | Emits cross-layer diagnostics, database health statistics, and curated overlay override counts. |

### 2. Machine CLI Commands

Execute via terminal within the Masar environment (`uv run masar <command>` or `masar <command>`):

```bash
# 1. Candidate triage with compact token projection (< 300 tokens)
masar search --seed "إنما الأعمال بالنيات" --scope all --compact

# 2. Structured JSON projection with full explainability receipts
masar search --seed "إنما الأعمال بالنيات" --format json --receipts --limit 25

# 3. Inspect full text and transmitter identifiers
masar inspect --id "bukhari_1"

# 4. Correct CRF boundary bleed (slice override)
masar split --id "bukhari_1" --start 142 --end 285

# 5. Add external manuscript folio with source citation
masar add --text "حدثنا الحميدي قال حدثنا سفيان..." --collection "Zahiriyya MS 34" --ref "Folio 14a" --family "fam_niyyat"

# 6. Reversible session rollback
masar session undo
masar session history
```

---

## Anti-Patterns

- **Exporting Raw CRF Splits**: Pushing uninspected automated splits into Riwaq without checking for narrator bleed.
- **Bypassing Quarantine**: Including records marked `TOPICAL_FALSE_POSITIVE` merely because of semantic keywords.
- **Mutating Base Corpus**: Attempting direct SQL updates against `corpus.db` rather than writing through `masar-curated.db`.
