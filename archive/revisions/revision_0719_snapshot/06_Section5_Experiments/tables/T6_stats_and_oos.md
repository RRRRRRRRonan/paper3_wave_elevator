# Table 6. Statistical hardening and out-of-sample checks (amendments A-R2, A-R3)

| item | pre-registered artefact | amendment result | reading |
|---|---|---|---|
| D1-d resolved sub-cells | 57/72 (PARTIAL, gate not re-judged) | BH-FDR(q=0.05): 62/72 | the one-cell miss is not a multiplicity artefact; under FDR control MORE cells resolve |
| H-D3 mean corner-ranking Spearman rho | 0.75 (point) | 95% bootstrap CI [0.52, 0.87] | model-sensitive branch confirmed with uncertainty attached |
| Block C pooled dominance | 99.2% | Wilson 95% CI [98.9%, 99.4%] | chain-dominance frequency tightly estimated |
| Block B distribution tests | none | 221/336 Mann-Whitney tests significant after BH(0.05) | policy differences are real at the per-cell distribution level |
| M_Phi winner's-curse check | in-sample mean 0.0170 | out-of-sample mean 0.0142 (shrink 16.6%, below the locked 25% materiality bar) | in-sample M_Phi mildly optimistic; conclusions unchanged |
| H_up out-of-sample | in-sample mean 0.0430 | OOS mean 0.0339 (shrink 21.2%) | capacity share stable: 0.717 in-sample vs 0.705 OOS |

Corner-selection stability (A-R3): train argmin != test argmin in 17/72 sub-cells; M_Phi_oos < 0 in 9/72 (winner's-curse correction where the corner landscape is flat).
