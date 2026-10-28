# Historical Interpretation & Hypothesis Testing Rules

## 1. The Core Analytical Dilemma

In ICMA research, observing a Common Link (CL) at transmitter $X$ raises four competing historical explanations:

1. **Hypothesis A (Historical Originator/First Systematic Distributor)**: Transmitter $X$ was the first to circulate this specific tradition in this formulated wording.
2. **Hypothesis B (Faithful Transmitter of Pre-Existing Text)**: Transmitter $X$ accurately received the tradition from their teacher (or earlier authorities), but was the earliest whose teaching reached multiple surviving independent lines.
3. **Hypothesis C (Retrospective Isnād Convergence / Projection)**: Later transmitters or collectors projected independent chains back to $X$ (*al-rafʿ*, *al-idrāj*, or *ziyādah*) due to $X$'s authoritative status in the region.
4. **Hypothesis D (Textual Expansion / Contamination)**: The core tradition originated earlier, but specific theological or legal pericopes were appended at the level of $X$ or subsequent PCLs.

---

## 2. Decision Rules for Distinguishing Hypotheses

### Rule 1: Textual Independence Test
- If transmission lines branching from two different Partial Common Links ($PCL_1$ and $PCL_2$) share identical idiosyncratic grammatical constructions or uncommon vocabulary (*gharīb*) not present in parallel traditions, this supports **Hypothesis A or B** (common ancestor) over independent emergence.

### Rule 2: Corroboration Depth Test
- If a proposed CL has branches terminating in only one collection or one geographic region (e.g., all paths lead to Kufa through one school), classify the node as **PCL_ONLY** or **LOCAL_CONVERGENCE**, not a universal Common Link.

### Rule 3: Single Strand Skepticism
- The chain of transmission between the CL and the Prophet (the "spider line") cannot be corroborated through stemma topology alone.
- In research dossiers, always explicitly state:
  > *"Topological convergence corroborates circulation at the level of [CL Name] (d. [Year] AH). The preceding single strand back to [Companion] is historically unverified by stemma analysis alone."*

### Rule 4: Divergent Transmission Branches (*Turuq Khārijah*)
- Look for transmission routes that bypass the proposed CL entirely.
- If a reliable divergent branch exists with an independent PCL and identical pericopes, **Hypothesis B** (pre-CL origin) is substantially strengthened.
- If divergent branches exhibit severe textual corruption or appear only in late 5th-century collections without corroboration, investigate potential retrospective projection (**Hypothesis C**).

---

## 3. Negative Controls & Boundary Traps

1. **The Homonym Trap (*Mushtabah al-Nisbah*)**:
   - Beware of identifying transmitters with common names (e.g., *Ismāʿīl*, *Ibrāhīm*) across regions without explicit biographical validation. An artificial identity merge creates a false Common Link.
2. **The Anachronism Check**:
   - Every edge $(u, v)$ in the DAG must satisfy chronological feasibility:
     $$death(v) - death(u) > 0 \quad \text{and} \quad death(v) - death(u) \le 80$$
   - Negative or excessively wide gaps indicate missing links (*irsal*), misidentifications, or forged isnāds.
3. **Topical vs. Textual Similarity**:
   - Never combine hadiths into a single transmission stemma simply because they share a legal ruling or theological theme. Only shared pericope structure and transmission lineage warrant bundle membership.
