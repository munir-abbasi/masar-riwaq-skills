# End-to-End ICMA Research Walkthrough Example

This document demonstrates an execution walkthrough of the `hadith-isnad-cum-matn-research` skill investigating the ḥadīth tradition of *al-Jassāsah*.

---

## 1. Initial Prompt & Phase 1 Scope

**User Instruction**:
> "Conduct a comprehensive isnād-cum-matn analysis of the ḥadīth of al-Jassāsah. Discover its variants, verify primary-source references, construct transmission families, and evaluate competing historical explanations."

**Agent Action (Phase 1)**:
- Clarifies scope: target tradition incipit `إن تميما الداري كان رجلا نصرانيا... فلقيتهم دابة أهلب...`.
- Sets analysis profile: `structural_only`.
- Prepares `assets/research-plan.md`.
- **◆ APPROVAL GATE 1**: Requests user confirmation before querying the corpora.

---

## 2. Masar Takhrīj Discovery (Phase 2 & 3)

**Tool Calls**:
```json
// 1. Search for candidates across Sunni corpora
masar_search({
  "seed": "ركب في سفينة بحرية مع ثلاثين رجلا من لخم وجذام فلقيتهم دابة",
  "scope": "all",
  "limit": 20
})
```

**Output**:
- 16 candidates retrieved from Sahih Muslim, Sunan Abi Dawud, Jami al-Tirmidhi, Sunan Ibn Majah, and Musnad Ahmad.
- 2 candidates flagged as `TOPICAL_FALSE_POSITIVE` (`[TRAP]`) due to general apocalyptic discussions lacking Tamīm al-Dārī pericopes; quarantined into `topical_quarantine_report.json`.

**Boundary Hygiene & Split Adjustment**:
```json
// Inspect candidate and correct CRF boundary bleed
masar_inspect({"hadith_id": "muslim_2942a"})
masar_adjust_split({
  "hadith_id": "muslim_2942a",
  "start": 142,
  "end": 285
})
```
- **◆ APPROVAL GATE 2**: Reviewing boundary overrides and quarantined false positives with researcher.

---

## 3. Transfer to Riwaq & Stemma Analysis (Phase 4 & 5)

**Execution**:
```bash
# Verify preflight gates on exported batch
python3 scripts/verify-artifacts.py --batch ../../evaluations/fixtures/jassasa-seed.json

# Execute topological CL/PCL analysis
node /path/to/riwaq/scripts/riwaq-cli.mjs analyze ../../evaluations/fixtures/jassasa-seed.json --profile structural_only
```

**Analytical Finding**:
- `family_status: cl_detected`
- `cl_candidate: amir-al-shabi` (ʿĀmir b. Sharāḥīl al-Shaʿbī, d. ~104 AH) with `fan_out: 7`, `collector_diversity: 7`.
- `pcls`: Ismāʿīl b. Abī Khālid, ʿAbd Allāh b. Buraydah, Ghaylān b. Jarīr, Sayyār Abū al-Ḥakam, Mujālid b. Saʿīd.
- **◆ APPROVAL GATE 3**: Reviewing narrator disambiguation before matn alignment.

---

## 4. Matn Pericope Alignment & Rival Hypotheses (Phase 6 & 7)

**Pericope Apparatus**:
- $P_1$ (Sea journey with 30 men of Lakhm & Judhām): Present in 14/16 witnesses across all 5 PCLs.
- $P_2$ (Encounter with the beast al-Jassāsah): Present in 15/16 witnesses.
- $P_3$ (Prophet's minbar gesture identifying Taybah as Medina): Present selectively in Basran branch through Sayyār Abū al-Ḥakam.

**Hypothesis Verdict**:
- Supports **Hypothesis A** (al-Shaʿbī as the primary systematic distributor in Kufa in the late 1st century AH).
- Rejects **Hypothesis C** (later retrospective fabrication) due to the wide collector diversity across multiple geographic centers.

---

## 5. Artifact Delivery & Gate 4

- Verified with `verify-artifacts.py` and `run-evals.py`.
- **◆ APPROVAL GATE 4**: Research dossier exported to Markdown and DOCX with SHA-256 seal.
