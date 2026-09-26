# Section 4 reference check — 2026-09-11

This record supports the two external citations in the reconstructed Section 4. It is a focused source check, not a new literature review or a record of experiment validation. Existing bibliography entries were checked against primary-source pages using web search because the preferred research-lookup command was unavailable.

## Smart Predict-then-Optimize

Elmachtoub, A. N., and Grigas, P. (2022). Smart “Predict, then Optimize.” *Management Science*, 68(1), 9–26. DOI: [10.1287/mnsc.2020.3922](https://doi.org/10.1287/mnsc.2020.3922). Primary author manuscript: [arXiv:1710.08005](https://arxiv.org/abs/1710.08005).

Checked use: the SPO loss measures the decision cost induced by predicted coefficients relative to the true-cost optimum. Section 4 specializes this definition to class actions. It does not import SPO+ training or generalization guarantees into the manuscript's diagnostic identity.

## Wasserstein distributionally robust optimization

Mohajerin Esfahani, P., and Kuhn, D. (2018). Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations. *Mathematical Programming*, 171, 115–166. DOI: [10.1007/s10107-017-1172-1](https://doi.org/10.1007/s10107-017-1172-1). Primary author manuscript: [arXiv:1505.05116](https://arxiv.org/abs/1505.05116).

Checked use: Wasserstein balls define distributional ambiguity around a reference distribution. The manuscript proves its scalar mean comparison directly, using a model-calibrated radius and the rival distribution as an attaining distribution. It does not claim that the cited paper establishes the manuscript's median-based class equivalence or supplies statistical calibration for its model-chosen radii.

## Retrieval

Searches used the exact titles with author names and restricted initial results to arxiv.org. Both arXiv records and both journal DOI landing pages were opened. Existing keys `elmachtoub2022smart` and `mohajerin2018data` in `paper_draft/manuscript/references_related_works.bib` remain unchanged. Historical work packages W1/W2/W3/W8/W9/W10 provide the local derivation trail; the current statement and numbering decisions are recorded in `revision_2026-09-02/MASTER_REVISION_BY_SECTION.md`, Section 7.
