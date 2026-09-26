# Table 5. Partition-sensitivity of the capacity share (amendment A-R1, reanalysis of stored A4 data)

Six configs, wave size 16, model M2. Two share metrics: the partition-intrinsic `H_up/UB` (oracle-slack denominator, defined for every scheme) and, for reference, the Phi-rule share `H_up/(H_up+M_Phi)` from the 72-sub-cell Block A grid (defined only for the 2x2 scheme, sizes {8,30}, models {M1,M2}).

| config | scheme | H_up | oracle slack | capacity share H_up/UB | 95% CI |
|---:|---|---:|---:|---:|---|
| 1 | 2x2_CI | 0.032 | 0.053 | 0.38 | [0.18, 0.75] |
| 3 | 2x2_CI | 0.026 | 0.072 | 0.26 | [0.05, 0.58] |
| 5 | 2x2_CI | 0.037 | 0.026 | 0.59 | [-0.05, 1.34] |
| 7 | 2x2_CI | 0.090 | 0.083 | 0.52 | [0.26, 0.74] |
| 9 | 2x2_CI | 0.016 | 0.022 | 0.41 | [-0.41, 0.95] |
| 11 | 2x2_CI | 0.023 | 0.036 | 0.39 | [-0.14, 0.95] |
| 1 | 2x2x2_CIT | 0.103 | 0.024 | 0.81 | [0.48, 1.00] |
| 3 | 2x2x2_CIT | 0.076 | 0.054 | 0.58 | [0.24, 0.93] |
| 5 | 2x2x2_CIT | 0.029 | 0.056 | 0.34 | [0.09, 0.88] |
| 7 | 2x2x2_CIT | 0.119 | 0.075 | 0.61 | [0.33, 0.79] |
| 9 | 2x2x2_CIT | 0.079 | -0.025 | 1.45 | [0.72, 1.86] |
| 11 | 2x2x2_CIT | 0.049 | 0.011 | 0.82 | [0.34, 1.18] |
| 1 | 3x3_CI | 0.081 | 0.076 | 0.52 | [0.28, 0.71] |
| 3 | 3x3_CI | 0.064 | 0.064 | 0.50 | [0.17, 0.80] |
| 5 | 3x3_CI | 0.056 | 0.014 | 0.80 | [0.52, 1.23] |
| 7 | 3x3_CI | 0.148 | 0.108 | 0.58 | [0.48, 0.69] |
| 9 | 3x3_CI | 0.027 | 0.031 | 0.47 | [-0.06, 0.94] |
| 11 | 3x3_CI | 0.081 | 0.018 | 0.82 | [0.54, 1.10] |

| scheme | configs with capacity share > 0.5 | locked rule (>= 5/6) |
|---|---:|---|
| 2x2_CI | 2/6 | FAILS |
| 2x2x2_CIT | 5/6 | meets |
| 3x3_CI | 4/6 | FAILS |

**Outcome (locked rule fired).** Under the oracle-slack metric the capacity-dominant reading is NOT scheme-stable (2x2: 2/6; 3x3: 4/6; 2x2x2 with T: 5/6). The manuscript therefore states capacity-side dominance as a partition- and metric-conditional finding: it holds for the Phi-rule share on the 72-sub-cell grid (0.72 of mean GAP) and must not be quoted as a universal property. Terciles require new simulation (amendment B-6).
