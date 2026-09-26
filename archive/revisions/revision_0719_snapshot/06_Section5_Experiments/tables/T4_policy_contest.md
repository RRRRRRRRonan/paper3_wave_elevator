# Table 4. Complete wave-release policy contest (Block B, publication scale)

All seven pre-registered comparators plus the P7 local-search reference, over the 12 (config, size) cells. Win fractions use strict inequality of cell-median makespans; ties shown separately. Wilson 95% CIs from amendment A-R2 (n = 12, so intervals are wide; reported as such).

## 4a. Grand mean of cell-median makespans (time units)

| policy | description | grand mean |
|---|---|---:|
| P0 | random selection (naive baseline) | 317.6 |
| P1 | destination-clustered (practitioner heuristic) | 313.4 |
| P2 | cardinality-only (fewest cross-floor orders) | 299.2 |
| P3 | direction-balanced | 319.6 |
| P4 | temporal-clustered | 317.8 |
| P5 | Phi corner rule (cell-median, the diagnostic policy) | 303.6 |
| P6 | SPO-Tree cell-mean predictor | 310.0 |
| P7 | 40-iteration local search (reference optimum) | 224.6 |

## 4b. Pairwise wins over 12 cells (row beats column / ties)

| | P0 | P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|---|---|
| **P0** | - | 3 (t1) | 0 | 6 (t1) | 5 (t1) | 1 (t1) | 2 (t2) | 0 |
| **P1** | 8 (t1) | - | 1 (t1) | 9 (t1) | 8 (t2) | 2 | 5 | 0 |
| **P2** | 12 | 10 (t1) | - | 12 | 12 | 5 | 10 | 0 |
| **P3** | 5 (t1) | 2 (t1) | 0 | - | 6 (t1) | 2 | 4 | 0 |
| **P4** | 6 (t1) | 2 (t2) | 0 | 5 (t1) | - | 2 | 3 | 0 |
| **P5** | 10 (t1) | 10 | 7 | 10 | 10 | - | 8 (t1) | 0 |
| **P6** | 8 (t2) | 7 | 2 | 8 | 9 | 3 (t1) | - | 0 |
| **P7** | 12 | 12 | 12 | 12 | 12 | 12 | 12 | - |

## 4c. Key comparisons with uncertainty

| comparison | wins / n | win frac | Wilson 95% CI |
|---|---:|---:|---|
| P5 beats P0 | 10/12 | 0.83 | [0.55, 0.95] |
| P5 beats P1 | 10/12 | 0.83 | [0.55, 0.95] |
| P5 beats P6 | 8/12 | 0.67 | [0.39, 0.86] |
| P5 beats P7 | 0/12 | 0.00 | [0.00, 0.24] |
| P2 beats P5 | 5/12 | 0.42 | [0.19, 0.68] |

P5 sits 46.4% above the P7 local-search reference on average and never beats it. The cardinality-only heuristic P2 beats P5 in 5/12 cells and posts a lower grand mean (299.2 vs 303.6): low cross-floor count is itself a strong lever, consistent with the capacity-side diagnosis. P5's value is diagnostic (simulation-free, interpretable), not a performance champion; this is the pre-registered framing.
