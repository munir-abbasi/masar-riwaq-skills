# Evidentiary Standards & Epistemic Guardrails

## 1. Epistemic Taxonomy: Keeping Objects Distinct

Scholarly integrity requires maintaining strict boundaries between different categories of information:

| Object | Definition | Examples | Riwaq Layer |
| :--- | :--- | :--- | :--- |
| **Observation** | Primary, uninterpreted textual witness or verified citation | Extracted Arabic text, page/hadith number, manuscript folio | $L_0$ Evidence |
| **Normalised Data** | Cleaned, segmented, and schema-validated representation | UTF-8 NFC text, parsed narrator IDs, variant bundles | $L_1-L_3$ Intake |
| **Derivation** | Pure mathematical or graph-theoretical computation | Fan-out degree, DAG depth, betweenness centrality, cluster | $L_4$ Features |
| **Analytical Inference**| Algorithmic classification under a stated methodological profile | CL candidate designation, PCL detection, structural score | $L_5$ Interpretation |
| **Historical Hypothesis**| A proposed historical explanation accounting for the findings | Wording originated with al-Zuhrī vs. circulated earlier in Medina | $L_5, L_7$ |
| **Unresolved Doubt** | Documented ambiguity, competing readings, or unverified claims | Transmitter homonym collision, disputed hearing (*samāʿ*) | $L_7$ Audit |

**Critical Directive**: Never collapse these categories. An algorithmic CL detection is a *derivation*, not historical proof that the narrator authored or fabricated the tradition.

---

## 2. The 8 Operational Commandments

1. **Zero Textual Fabrication**:
   - Never invent or hallucinate a hadith witness, narrator name, death date, biographical citation, or manuscript folio.
   - If a primary citation is unverified, flag it explicitly: `UNVERIFIED_CITATION`.
2. **Candidates ≠ Attestations**:
   - Search results returned by Masar are potential candidates.
   - A candidate becomes an accepted witness only after boundary verification and source reference confirmation.
3. **Preservation of Dual Representations**:
   - Keep verbatim Arabic text intact (including diacritics, orthographic oddities, and vocalizations where present).
   - Use normalized representations (stripped of tatweel, unified hamzas) strictly for search indexing and graph matching.
4. **No Silent Transmitter Merges**:
   - Transmitters sharing names (e.g., *Sufyān*, *Hammād*, *ʿAbd Allāh b. ʿUmar*) must not be merged automatically.
   - Any proposed identification must be staged non-destructively in `ProposalStore` and confirmed by human approval.
5. **Schema Conformance ≠ Scholarly Verification**:
   - A dataset passing `validateBatch()` or `PreflightValidator` means the JSON structure is valid. It does *not* prove historical accuracy.
6. **No Probability Conflation**:
   - Do not translate CL scores into "percent chance of authenticity" or "probability of being prophetic."
   - Explicitly label scores as *structural convergence indicators under the selected analysis profile*.
7. **Traceable Attribution**:
   - Every analytical claim must bind directly to primary source IDs ($L_0$) and reproducible tool invocations.
8. **Preservation of Software Provenance**:
   - Dossiers must record tool versions, git commit hashes, execution parameters, and database snapshots.

---

## 3. Contradiction Resolution & Authority Lattice

When evidence conflicts across documentation, schemas, and runtime behavior, adhere strictly to the following authority lattice:

```
1. Owning Source Code + Passing Unit/E2E Tests
   ▲
2. Local Contract Documentation (e.g., schemas, module READMEs)
   ▲
3. Agent Operating Model (docs/AGENT-OPERATING-MODEL.md)
   ▲
4. Mutable Project Status (STATUS.md)
   ▲
5. Durable Intentions & Architecture Records (DECISIONS.md)
   ▲
6. Background Research & Conceptual Prose
```

If code and documentation disagree, record the discrepancy as a **contradiction** and report it to the researcher. Never write speculative prose to make contradictions disappear.
