# Isnād-cum-Matn Analysis (ICMA) Methodology

## 1. Theoretical Foundations

Isnād-cum-matn analysis (ICMA)—pioneered by Josef van Ess, Harald Motzki, and Gregor Schoeler—is an empirical method for reconstructing the historical transmission of early Islamic traditions. It operates on the premise that independent transmission lines carrying correlated textual variants allow dating the tradition to the period of their convergence.

### Key Concepts

- **Common Link (CL)**: The earliest transmitter from whom multiple independent transmission branches emanate, each branch confirmed by distinct collectors and chains.
- **Partial Common Link (PCL)**: A transmitter in a subsequent generation who receives the tradition from the CL and distributes it to multiple independent pupils.
- **Single Strand (Spider Line)**: An uncorroborated single line connecting the CL back to the putative authority (Companion or Prophet). Under classical ICMA, single strands cannot be mathematically corroborated through transmission stemma alone.
- **Divergent Paths**: Transmission routes that bypass the proposed CL. If genuine, they indicate either an earlier circulation or a parallel independent transmission.

---

## 2. Graph Derivation & Stemma Rules (Riwaq Layer $L_4$)

Riwaq formalizes transmission chains into a Directed Acyclic Graph (DAG) $G = (V, E)$:
- **Vertices ($V$)**: Transmitters (narrators) and collectors.
- **Edges ($E$)**: Teacher-to-student transmission relationships $(u, v)$ where $u$ transmits to $v$.
- **Source Nodes**: Putative authorities (Prophet, Companions).
- **Sink Nodes**: Collectors (e.g., al-Bukhārī, Muslim, al-Kulaynī).

### Topological Criteria for CL Detection

A node $v \in V$ is evaluated as a candidate Common Link based on:
1. **Branch Fan-Out**: Out-degree $d^+(v) \ge 3$ leading to distinct collector nodes.
2. **Collector Diversity**: Paths from $v$ terminate in at least 2 distinct regional/sectarian collections.
3. **PCL Corroboration**: At least 2 outgoing branches contain verified Partial Common Links with their own fan-out ($d^+ \ge 2$).
4. **Independent Transmission Depth**: Minimum graph depth between $v$ and terminal collectors $\ge 2$ generations.

---

## 3. Matn Segmentation & Pericope Apparatus (Riwaq Layer $L_3$)

Textual variance analysis requires segmenting the matn into atomic semantic units (*pericopes*):

1. **Pericope Segmentation**: Split the core narrative into numbered clauses $P_1, P_2, \dots, P_n$.
2. **Variant Matrix**: For each witness $W_i$ and pericope $P_j$, record the exact textual reading $R_{i,j}$.
3. **Branch Correlation**:
   - Compute whether variant readings $R_{a}$ vs. $R_{b}$ map onto specific transmission sub-trees rooted in distinct PCLs.
   - If variant $R_a$ occurs *exclusively* under PCL $A$ and variant $R_b$ occurs *exclusively* under PCL $B$, this constitutes strong textual evidence confirming the structural PCLs as independent transmitters.
4. **Handling Unsegmented Traditions**:
   - If pericope segmentation has not been formally conducted, textual correspondence must be reported as **unmeasured**.
   - Agents must never report a default mathematical similarity score as evidence of textual alignment.

---

## 4. Chronological & Regional Mapping

Every transmitter in the graph is contextualized by:
- **Death Date ($AH$)**: Flourishing window estimated as $[d - 40, d]$.
- **Regional Center**: Medina, Mecca, Basra, Kufa, Damascus, Baghdad, Rayy, Qom.
- **Transmission Plausibility**: Chronological consistency between teacher ($u$) and student ($v$). A positive age gap ($death(v) > death(u)$) is required; anachronisms flag potential chain fabrication or missed homonyms.
