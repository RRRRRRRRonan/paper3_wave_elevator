"""Are the sheet-2 rows in the 2010-12-01..09 overlap exact copies of sheet-1 rows? (read-only)"""
import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
X = r"F:/Paper 3/prototype/data/online_retail_II.xlsx"
OUT = Path(r"F:/Paper 3/revision_2026-09-26_ijpr/week4/case_data_check_2026-09-27.json")
sh = pd.read_excel(X, sheet_name=None)
a, b = list(sh.values())
lo, hi = b["InvoiceDate"].min(), a["InvoiceDate"].max()
cols = ["Invoice", "StockCode", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country", "Description"]


def key(d):
    return Counter(tuple(str(v) for v in r) for r in d[cols].itertuples(index=False))


ka, kb = key(a[a["InvoiceDate"] >= lo]), key(b[b["InvoiceDate"] <= hi])
res = {"window": [str(lo), str(hi)], "rows_sheet1": sum(ka.values()), "rows_sheet2": sum(kb.values()),
       "identical_multisets_all_columns": ka == kb}
print(res)
rep = json.loads(OUT.read_text(encoding="utf-8"))
rep["sheet_overlap_window"].update({"identical_rows_all_columns": ka == kb,
                                    "note": "the exact-duplicate rule of §11.2 keeps the sheet-1 copy (file order), "
                                            "so the overlap days are not counted twice"})
OUT.write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
