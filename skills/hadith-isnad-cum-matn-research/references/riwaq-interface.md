# Riwaq Machine Interface Contract

Riwaq provides two primary interfaces for agent control:
1. **Native Model Context Protocol (MCP)** via stdio JSON-RPC 2.0 (`scripts/riwaq-mcp.mjs`).
2. **Deterministic Control CLI** (`node scripts/riwaq-cli.mjs`).

---

## 1. Model Context Protocol (MCP) Tool Reference

### `riwaq_manifest`
- **Description**: Inspect machine-readable capability/contract manifest across the Riwaq Abstraction Tower ($L_0 \to L_9$).
- **Arguments**: *(none)*
- **Response Format**: Emits JSON object defining supported layers, schema versions, registered exporters, and analysis profiles.

### `riwaq_validate`
- **Description**: Validate batch schema structure, provenance fields, and strict anti-hallucination invariants.
- **Arguments**:
  - `filePath` (`string`, required): Absolute or relative path to batch JSON file.
- **Response Format**:
  ```json
  {
    "ok": true,
    "valid": true,
    "normalized": { "schema_version": 1, "records": [...] },
    "errorCount": 0,
    "warningCount": 0
  }
  ```

### `riwaq_diagnose`
- **Description**: Automated cross-layer diagnosis evaluating health across $L_1 \to L_8$ and emitting actionable remediation packets.
- **Arguments**:
  - `filePath` (`string`, required): Path to canonical or imported JSON batch.
  - `profile` (`string`, optional): `"structural_only"` or `"reliability_weighted"` (default: `"structural_only"`).
  - `withReliability` (`boolean`, optional): Whether to include reliability layer (default: `false`).
- **Response Format**: Returns health metrics, schema warnings, disconnected graph nodes, and typed remediation prescriptions with JSON pointer paths.

### `riwaq_analyze`
- **Description**: Run CL/PCL topological analysis over hadith families in a batch.
- **Arguments**:
  - `filePath` (`string`, required): Path to validated batch JSON.
  - `profile` (`string`, optional): `"structural_only"` or `"reliability_weighted"`.
  - `withReliability` (`boolean`, optional): Default `false`.
- **Response Format**:
  ```json
  {
    "ok": true,
    "families": [
      {
        "family_id": "fam_jassasa",
        "family_status": "cl_detected",
        "cl_candidate": "amir_al_shabi",
        "cl_score": 0.88,
        "pcls": ["ismail_ibn_abi_khalid", "zakariyya_ibn_abi_zaida"],
        "node_count": 18,
        "edge_count": 24
      }
    ]
  }
  ```

### `riwaq_stage_proposal`
- **Description**: Stage an AI extraction or identity proposal into the non-destructive `ProposalStore`.
- **Arguments**:
  - `filePath` (`string`, required): Target batch JSON file.
  - `type` (`string`, required): One of:
    - `"PROPOSAL_NARRATOR_MERGE"`
    - `"PROPOSAL_NARRATOR_SPLIT"`
    - `"PROPOSAL_MATN_SEGMENTATION"`
  - `payload` (`object`, required): Proposal parameters (e.g., `sourceId`, `targetId`, or segments).
  - `rationale` (`string`, required): Scholarly justification and biographical evidence.
- **Response Format**:
  ```json
  {
    "ok": true,
    "proposalId": "prop_9f2e1a",
    "status": "staged",
    "createdAt": "2026-10-28T18:00:00Z"
  }
  ```

### `riwaq_commit_proposal`
- **Description**: Commit an approved proposal into canonical batch state and mint an immutable SHA-256 receipt.
- **Arguments**:
  - `filePath` (`string`, required): Target batch JSON file.
  - `proposalId` (`string`, required): ID returned by `riwaq_stage_proposal`.
  - `reviewerId` (`string`, required): Human reviewer identifier.
  - `notes` (`string`, optional): Review sign-off notes.
- **Response Format**:
  ```json
  {
    "ok": true,
    "committed": true,
    "receipt": {
      "proposalId": "prop_9f2e1a",
      "sha256": "3a7b8c...",
      "timestamp": "2026-10-28T18:05:00Z"
    }
  }
  ```

### `riwaq_export`
- **Description**: Generate publishable Markdown projection from canonical analysis (gated strictly by `CanonicalReport.canExport()`).
- **Arguments**:
  - `filePath` (`string`, required): Validated batch JSON.
  - `profile` (`string`, optional): Analysis profile.
- **Response Format**: Emits full markdown report text if `canExport()` is true; returns error if blocked by claim violations.

---

## 2. Command Line Interface (CLI)

Run via: `node scripts/riwaq-cli.mjs <command> <file> [options]`

```bash
# 1. Structural schema validation
node scripts/riwaq-cli.mjs validate import-batch.json

# 2. Preflight quality gates
node scripts/riwaq-cli.mjs gates import-batch.json --min-score 0.70

# 3. Pre-analysis anti-hallucination check
node scripts/riwaq-cli.mjs hallucination import-batch.json

# 4. Raw CL/PCL graph analysis
node scripts/riwaq-cli.mjs analyze import-batch.json --profile structural_only

# 5. Full one-shot pipeline
node scripts/riwaq-cli.mjs pipeline import-batch.json --profile structural_only

# 6. Export verified analytical report
node scripts/riwaq-cli.mjs export import-batch.json --format md --out dossier.md

# 7. Mint and verify deterministic integrity seals
node scripts/riwaq-cli.mjs seal import-batch.json
node scripts/riwaq-cli.mjs verify-seal import-batch.json --manifest import-batch.json.seal.json
```
