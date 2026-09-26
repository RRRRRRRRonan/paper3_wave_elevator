"""
Calibrated-case order data (Phase 6 protocol §11.2): UCI Online Retail II
(CC BY 4.0) invoice lines mapped to elevator loads.

    load_raw(path)          CSV or XLSX (all sheets); keeps the file position
    clean(df)               the registered cleaning rules, with a step report
    eligible_days(df, 600)  calendar days with at least 600 cleaned lines
    draw_case_pool(...)     one test pool: day and lines on stream 89, then
                            the mapping of experiments_phase6.case_pool_from_lines

Cleaning, in the registered order: (1) drop cancellation invoices (invoice
number starting with "C"); (2) drop lines with non-positive quantity or price;
(3) keep stock codes that begin with five digits; (4) drop exact duplicate
lines. Both the Online Retail II column names (Invoice, Price) and the
Online Retail I names (InvoiceNo, UnitPrice) are accepted.

No data file ships with the repository. The self-test uses a synthetic table
with the same columns: python -m src.case_online_retail
"""
from __future__ import annotations

import random
import re
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd

COLUMNS = {"invoice": ("Invoice", "InvoiceNo"),
           "stock": ("StockCode",),
           "qty": ("Quantity",),
           "time": ("InvoiceDate",),
           "price": ("Price", "UnitPrice")}
PRODUCT_CODE = re.compile(r"^\d{5}")
MIN_LINES_PER_DAY = 600


def standardize(df: pd.DataFrame) -> pd.DataFrame:
    """Canonical columns invoice, stock, qty, time, price (+ src_pos)."""
    out = pd.DataFrame(index=df.index)
    for key, names in COLUMNS.items():
        col = next((c for c in names if c in df.columns), None)
        if col is None:
            raise ValueError(f"missing column for {key!r}: one of {names}")
        out[key] = df[col]
    out["invoice"] = out["invoice"].astype(str).str.strip()
    out["stock"] = out["stock"].astype(str).str.strip()
    out["time"] = pd.to_datetime(out["time"])
    out["src_pos"] = df["src_pos"] if "src_pos" in df.columns else range(len(df))
    return out.reset_index(drop=True)


def load_raw(path: Path) -> pd.DataFrame:
    """Read the source file; XLSX sheets are concatenated in sheet order.
    `src_pos` records each line's position in the source."""
    path = Path(path)
    if path.suffix.lower() in (".xlsx", ".xls"):
        sheets = pd.read_excel(path, sheet_name=None)
        df = pd.concat(list(sheets.values()), ignore_index=True)
    else:
        df = pd.read_csv(path, encoding="utf-8", encoding_errors="replace")
    df["src_pos"] = range(len(df))
    return standardize(df)


def clean(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """Apply the §11.2 rules in order; return the cleaned lines and counts."""
    report = {"input": len(df)}
    df = df[~df["invoice"].str.upper().str.startswith("C")]
    report["after_cancellations"] = len(df)
    df = df[(df["qty"] > 0) & (df["price"] > 0)]
    report["after_nonpositive"] = len(df)
    df = df[df["stock"].map(lambda s: bool(PRODUCT_CODE.match(s)))]
    report["after_product_codes"] = len(df)
    key = ["invoice", "stock", "qty", "time", "price"]
    df = df.drop_duplicates(subset=key, keep="first")
    report["after_duplicates"] = len(df)
    df = df.sort_values("src_pos", kind="stable").reset_index(drop=True)
    df["date"] = df["time"].dt.date
    return df, report


def eligible_days(df: pd.DataFrame, min_lines: int = MIN_LINES_PER_DAY) -> List:
    counts = df.groupby("date").size()
    return sorted(counts[counts >= min_lines].index)


def draw_case_pool(df: pd.DataFrame, F: int, seed: int, n_orders: int = 600,
                   ready_horizon: Optional[float] = None, days=None):
    """One case test pool (§11.2): the day and the lines on one stream.
    Returns (pool, info). The same seed with ready_horizon set gives the
    sensitivity version of the same pool (same day, lines, directions)."""
    from src.experiments_phase6 import case_pool_from_lines
    days = eligible_days(df) if days is None else days
    if not days:
        raise ValueError("no eligible day with at least "
                         f"{MIN_LINES_PER_DAY} cleaned lines")
    rng = random.Random(seed)
    day = days[rng.randrange(len(days))]
    sub = df[df["date"] == day].sort_values("src_pos", kind="stable")
    lines = list(zip(sub["stock"], sub["time"]))
    pool = case_pool_from_lines(lines, F, n_orders, rng,
                                ready_horizon=ready_horizon)
    return pool, {"day": str(day), "lines_that_day": len(lines),
                  "n_eligible_days": len(days)}


# --------------------------------------------------------------------------
# Self-test on a synthetic table (no real data)
# --------------------------------------------------------------------------

def _synthetic(seed: int = 424_270) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []
    specs = [("2010-12-01", 700), ("2010-12-02", 650), ("2010-12-03", 200)]
    inv = 500000
    for day, n in specs:
        for k in range(n):
            if k % 5 == 0:
                inv += 1
            t = pd.Timestamp(day) + pd.Timedelta(minutes=rng.randint(480, 1080))
            rows.append({"Invoice": str(inv), "StockCode": f"{rng.randint(10000, 90000)}"
                         + rng.choice(["", "A", "B"]),
                         "Quantity": rng.randint(1, 24), "InvoiceDate": t,
                         "Price": round(rng.uniform(0.5, 9.0), 2)})
    # lines the rules must remove
    bad = [{"Invoice": "C500001", "StockCode": "85123A", "Quantity": -2},
           {"Invoice": "500002", "StockCode": "85123A", "Quantity": 0},
           {"Invoice": "500003", "StockCode": "POST", "Quantity": 1},
           {"Invoice": "500004", "StockCode": "BANK CHARGES", "Quantity": 1},
           {"Invoice": "500005", "StockCode": "M", "Quantity": 1},
           {"Invoice": "500006", "StockCode": "C2", "Quantity": 1}]
    for b in bad:
        rows.append({**b, "InvoiceDate": pd.Timestamp("2010-12-01 10:00"),
                     "Price": 1.0})
    rows.append(dict(rows[0]))                                  # exact duplicate
    return pd.DataFrame(rows)


def _selftest() -> None:
    raw = _synthetic()
    raw["src_pos"] = range(len(raw))
    df, rep = clean(standardize(raw))
    assert rep["input"] == 700 + 650 + 200 + 6 + 1
    assert rep["after_cancellations"] == rep["input"] - 1
    assert rep["after_nonpositive"] == rep["after_cancellations"] - 1
    assert rep["after_product_codes"] == rep["after_nonpositive"] - 4
    assert rep["after_duplicates"] == rep["after_product_codes"] - 1
    days = eligible_days(df)
    assert [str(d) for d in days] == ["2010-12-01", "2010-12-02"], days
    pool_a, info_a = draw_case_pool(df, 3, seed=424_271)
    pool_b, info_b = draw_case_pool(df, 3, seed=424_271)
    assert info_a == info_b and [(o.source_floor, o.dest_floor) for o in pool_a] \
        == [(o.source_floor, o.dest_floor) for o in pool_b], "not deterministic"
    assert len(pool_a) == 600
    assert all(o.release_time == 0.0 for o in pool_a)
    for o in pool_a:                        # storage floors 2..F, packing floor 1
        assert (o.dest_floor == 1 and o.source_floor in (2, 3)) or \
               (o.source_floor == 1 and o.dest_floor in (2, 3))
    share_out = sum(o.dest_floor == 1 for o in pool_a) / len(pool_a)
    assert 0.7 < share_out < 0.9, share_out
    pool_s, _ = draw_case_pool(df, 3, seed=424_271, ready_horizon=50.0)
    assert [(o.source_floor, o.dest_floor) for o in pool_s] == \
           [(o.source_floor, o.dest_floor) for o in pool_a], \
        "the sensitivity pool must be the same pool"
    r = [o.release_time for o in pool_s]
    assert min(r) == 0.0 and max(r) == 50.0 and len(set(r)) == 600
    print(f"  [OK] case loader: cleaning steps {rep}; eligible days "
          f"{[str(d) for d in days]}; deterministic draw of 600 loads; "
          f"outbound share {share_out:.2f}; ready-time sensitivity on the same pool")


if __name__ == "__main__":
    _selftest()
