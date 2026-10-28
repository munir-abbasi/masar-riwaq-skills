# Masar Machine Interface Contract

Masar exposes two primary interfaces for agent control:
1. **Native Model Context Protocol (MCP)** via stdio JSON-RPC 2.0 (`masar mcp`).
2. **Single-Hop CLI** (`masar`).

---

## 1. Model Context Protocol (MCP) Tool Reference

### `masar_search`
- **Description**: Search for hadith variants using 4-signal takhrīj engine with explainability receipts.
- **Arguments**:
  - `seed` (`string`, required): Search snippet, target phrase, or seed matn.
  - `scope` (`string`, optional): Search scope; allowed values: `"all"`, `"sunni"`, `"shia"` (default: `"all"`).
  - `limit` (`integer`, optional): Maximum candidates to return (default: `10`).
- **Response Format**:
  ```json
  [
    {
      "id": "bukhari_1",
      "collection": "Sahih al-Bukhari",
      "hadith_number": "1",
      "sect": "sunni",
      "isnad_raw": "حدثنا الحميدي...",
      "matn": "إنما الأعمال بالنيات...",
      "receipt": {
        "bm25_score": 14.82,
        "semantic_similarity": 0.94,
        "pericope_overlap": 0.88,
        "ensemble_score": 0.91,
        "is_topical_false_positive": false,
        "signals_fired": ["bm25", "semantic", "pericope"]
      }
    }
  ]
  ```

### `masar_inspect`
- **Description**: Retrieve full text, isnad chain, and boundary split of a hadith record.
- **Arguments**:
  - `hadith_id` (`string`, required): Unique record identifier.
- **Response Format**:
  ```json
  {
    "id": "bukhari_1",
    "collection": "Sahih al-Bukhari",
    "hadith_number": "1",
    "full_text": "حدثنا الحميدي... إنما الأعمال بالنيات...",
    "isnad_raw": "حدثنا الحميدي قال حدثنا سفيان...",
    "matn": "إنما الأعمال بالنيات...",
    "narrator_ids": ["al_humaydi", "sufyan_ibn_uyaynah", "yahya_ibn_said"],
    "boundary": {
      "matn_start": 142,
      "matn_end": 285,
      "post_isnad_token": "يقول",
      "is_overridden": true
    }
  }
  ```

### `masar_adjust_split`
- **Description**: Adjust isnad/matn split boundary and persist to accretive curated overlay.
- **Arguments**:
  - `hadith_id` (`string`, required): Unique record identifier.
  - `start` (`integer`, required): Zero-based start index of matn slice.
  - `end` (`integer`, required): Zero-based end index of matn slice.
- **Response Format**:
  ```json
  {
    "status": "success",
    "hadith_id": "bukhari_1",
    "matn_start": 142,
    "matn_end": 285,
    "post_isnad_token": "يقول",
    "curator": "agent_cli"
  }
  ```

### `masar_add_manual`
- **Description**: Ingest an ad-hoc unsegmented hadith report into workspace with heuristic split.
- **Arguments**:
  - `text` (`string`, required): Raw Arabic text of the tradition.
  - `collection` (`string`, required): Name of source manuscript or print edition.
  - `ref` (`string`, required): Specific page, volume, or folio locator.
  - `family_id` (`string`, optional): Target family bundle identifier (default: `"fam_manual"`).
- **Response Format**:
  ```json
  {
    "status": "success",
    "hadith_id": "manual_7f8a9b",
    "family_id": "fam_manual",
    "collection": "Berlin MS 402",
    "matn_snippet": "حدثنا فلان..."
  }
  ```

### `masar_diagnose`
- **Description**: Inspect cross-layer system health and database statistics.
- **Arguments**: *(none)*
- **Response Format**: Emits counts of base corpus records, curated boundary overrides, manual additions, and active session transactions.

---

## 2. Command Line Interface (CLI)

```bash
# High-density token-thrifty search projection (< 300 tokens)
masar search --seed "إنما الأعمال بالنيات" --scope all --compact

# Machine-readable JSON output with receipts
masar search --seed "إنما الأعمال بالنيات" --format json --receipts --limit 20

# Inspect single witness
masar inspect --id "muslim_1907"

# Adjust CRF split boundary
masar split --id "muslim_1907" --start 120 --end 310

# Add manual entry with provenance locator
masar add --text "حدثنا مسدد..." --collection "Musnad al-Bazzar" --ref "Vol 3, p. 112" --family "fam_jassasa"

# Rollback last mutation
masar session undo
```

---

## 3. Preflight Export Gates

Before exporting any bundle to Riwaq, the batch must pass:
1. `GateSchema`: Conforms to `schemas/riwaq-import-batch.json` (`schema_version: 1`).
2. `GateFamilyConsistency`: All records share identical `family_id`.
3. `GateBoundaryHygiene`: No transmitter tokens (`حدثنا`, `أخبرنا`, `عن`) in `matn_raw`.
4. `GateIsnadIntegrity`: Chains have length $\ge 1$ and non-empty narrator IDs.
