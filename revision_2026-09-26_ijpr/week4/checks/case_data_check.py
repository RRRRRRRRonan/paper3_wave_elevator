"""Protocol §11.2 checks on the downloaded UCI Online Retail II file, before Stage L2 tuning.
Runs load_raw -> clean -> eligible_days of src.case_online_retail (the code the case driver uses) plus
read-only sanity checks. No case pool is drawn (stream 89 is not touched); nothing is written to
prototype/results/. Output: revision_2026-09-26_ijpr/week4/case_data_check_2026-09-27.json"""
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

import pandas as pd

sys.path.insert(0, r"F:/Paper 3/prototype")
sys.stdout.reconfigure(encoding="utf-8")
from src.case_online_retail import MIN_LINES_PER_DAY, PRODUCT_CODE, clean, eligible_days, load_raw  # noqa: E402

DATA = Path(r"F:/Paper 3/prototype/data")
XLSX, ZIP = DATA / "online_retail_II.xlsx", DATA / "online_retail_ii.zip"
OUT = Path(r"F:/Paper 3/revision_2026-09-26_ijpr/week4/case_data_check_2026-09-27.json")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


t0 = time.time()
sheets = pd.read_excel(XLSX, sheet_name=None)
sheet_info = {name: {"rows": len(d), "columns": list(map(str, d.columns)),
                     "first_invoice_date": str(d["InvoiceDate"].min()),
                     "last_invoice_date": str(d["InvoiceDate"].max())} for name, d in sheets.items()}
raw = load_raw(XLSX)
t_load = time.time() - t0
df, report = clean(raw)
days = eligible_days(df)
per_day = df.groupby("date").size()

# read-only sanity checks
stock_types = Counter(type(v).__name__ for v in pd.concat(list(sheets.values()))["StockCode"].head(200000))
kept_codes = df["stock"].unique()
checks = {
    "all_kept_codes_start_with_five_digits": bool(all(PRODUCT_CODE.match(s) for s in kept_codes)),
    "no_cancellation_invoice_kept": bool(not df["invoice"].str.upper().str.startswith("C").any()),
    "all_qty_and_price_positive": bool((df["qty"] > 0).all() and (df["price"] > 0).all()),
    "no_exact_duplicates_left": bool(not df.duplicated(subset=["invoice", "stock", "qty", "time", "price"]).any()),
    "eligible_days_all_have_at_least_600_lines": bool((per_day.loc[days] >= MIN_LINES_PER_DAY).all()),
    "invoice_dates_parsed": bool(df["time"].notna().all()),
}
removed_codes = sorted(set(raw["stock"]) - set(df["stock"]))
non_product = [c for c in removed_codes if not PRODUCT_CODE.match(c)]
overlap = None
names = list(sheets)
if len(names) == 2:
    a, b = sheets[names[0]], sheets[names[1]]
    lo, hi = b["InvoiceDate"].min(), a["InvoiceDate"].max()
    overlap = {"from": str(lo), "to": str(hi),
               "rows_sheet1_in_window": int((a["InvoiceDate"] >= lo).sum()),
               "rows_sheet2_in_window": int((b["InvoiceDate"] <= hi).sum())}

res = {
    "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
    "purpose": "Protocol §11.2 checks before Stage L2 (case_included requires D-K signed and these checks passed). "
               "No case pool drawn; stream 89 untouched; nothing written to prototype/results/.",
    "source": {"dataset": "Online Retail II, UCI Machine Learning Repository (Chen, D., 2012), doi:10.24432/C5CG6D",
               "licence": "CC BY 4.0 (stated on https://archive.ics.uci.edu/dataset/502/online+retail+ii, checked 2026-09-27)",
               "download_url": "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip",
               "downloaded": "2026-09-27",
               "zip_sha256": sha(ZIP), "xlsx_sha256": sha(XLSX), "xlsx_bytes": XLSX.stat().st_size},
    "sheets": sheet_info,
    "sheet_overlap_window": overlap,
    "load_seconds": round(t_load, 1),
    "cleaning_report": report,
    "removed_share": round(1 - report["after_duplicates"] / report["input"], 4),
    "removed_non_product_codes_examples": non_product[:40],
    "n_removed_non_product_codes": len(non_product),
    "n_distinct_kept_stock_codes": int(len(kept_codes)),
    "n_calendar_days_with_lines": int(len(per_day)),
    "n_eligible_days": len(days),
    "eligible_days_first_last": [str(days[0]), str(days[-1])] if days else None,
    "lines_per_eligible_day": {"min": int(per_day.loc[days].min()), "median": float(per_day.loc[days].median()),
                               "max": int(per_day.loc[days].max())} if days else None,
    "stockcode_python_types_first_200k": dict(stock_types),
    "checks": checks,
    "all_checks_pass": all(checks.values()) and len(days) > 0,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({k: res[k] for k in ("cleaning_report", "n_eligible_days", "eligible_days_first_last",
                                      "lines_per_eligible_day", "checks", "all_checks_pass",
                                      "sheet_overlap_window", "n_removed_non_product_codes",
                                      "stockcode_python_types_first_200k", "load_seconds")},
                 indent=1, ensure_ascii=False))
print("examples of removed non-product codes:", non_product[:25])
