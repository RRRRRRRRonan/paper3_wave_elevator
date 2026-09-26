# Case data: UCI Online Retail II

Used only by the Study 2 calibrated case (protocol `paper_draft/phase6_method_study_protocol.md` §11; decision D-K).
The raw files are not committed (see `.gitignore`). To restore them, download and check the hashes below.

| Item | Value |
|---|---|
| Dataset | Online Retail II, UCI Machine Learning Repository. Chen, D. (2012), doi:10.24432/C5CG6D |
| Licence | CC BY 4.0 (stated on https://archive.ics.uci.edu/dataset/502/online+retail+ii, checked 2026-09-27) |
| Download | https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip (downloaded 2026-09-27) |
| `online_retail_ii.zip` | 45,622,418 bytes, SHA-256 `572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb` |
| `online_retail_II.xlsx` (the only member of the zip) | 45,622,278 bytes, SHA-256 `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980` |
| Reader | `src/case_online_retail.load_raw` (both sheets, in sheet order); needs `openpyxl` |

The case driver takes the workbook path: `python -m src.experiments_phase6 case --case-data data/online_retail_II.xlsx`. That command runs the registered case and writes into `prototype/results/`. Run it only after the L2 addendum is signed and only at the author's request.

The §11.2 checks run on 2026-09-27, before Stage L2, are recorded in `revision_2026-09-26_ijpr/week4/case_data_check_2026-09-27.json`: 1,067,371 input lines, 1,003,212 after cleaning, and 588 eligible days (at least 600 lines each). All checks passed. The two sheets overlap on 2010-12-01 to 2010-12-09 with 22,523 identical rows. The exact-duplicate rule keeps the sheet-1 copy, so those days are not counted twice.
