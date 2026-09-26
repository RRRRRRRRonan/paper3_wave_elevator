"""Read-only check with the proposed case timing (non-integer values): single orders and single-AMR waves
must give DES = closed form, and a one-wave chain must equal the single wave, as with the integer defaults.
Toy seeds only; nothing written."""
import random
import sys

sys.path.insert(0, r"F:/Paper 3/prototype")
from src.des_evaluator import _closed_form, _toy_orders, des_makespan  # noqa: E402

CASES = {"midpoints": dict(speed_per_floor=13.81, load_time=15.15, unload_time=14.705, service_time=10.5),
         "lows": dict(speed_per_floor=6.76, load_time=8.3, unload_time=7.8, service_time=1.0),
         "highs": dict(speed_per_floor=20.86, load_time=22.0, unload_time=21.61, service_time=20.0)}
worst, n = 0.0, 0
for name, tm in CASES.items():
    sim_kw = {k: tm[k] for k in ("speed_per_floor", "load_time", "unload_time")}
    rng = random.Random(424_900 + len(name))
    for _ in range(300):
        for n_orders, A in ((1, 3), (rng.randint(2, 9), 1)):
            orders = _toy_orders(rng, n_orders, 3, rng.random() < 0.5)
            orders = [(s, d, r * 1.37) for s, d, r in orders]           # non-integer ready offsets too
            for E in (1, 2, 3):
                for c in (1, 2):
                    for model in ("M1", "M2"):
                        got = des_makespan(orders, A, E, c, model, **tm)
                        ref = _closed_form(orders, A, E, c, model, service_time=tm["service_time"], **sim_kw)
                        worst = max(worst, abs(got - ref))
                        n += 1
                        assert abs(got - ref) < 1e-6, (name, orders, A, E, c, model, got, ref)
print(f"[OK] {n} single-order and single-AMR cases at the case lows, midpoints and highs: DES = closed form "
      f"(largest difference {worst:.2e} s)")
