"""
Section 3 schematic (Fig. 1 of the manuscript), pictorial version.

  (a) A wave W of n orders is released at t_W. Each order is a load that an AMR
      moves from its source floor to its destination floor; AMRs change floors
      only by riding one of the E shared elevators, and a car carries up to c
      AMRs travelling between the same pair of floors. All AMRs and cars start on
      floor f^0 (floor 1 in the sketch). Steps 1 to 4 trace order o_1.
  (b) Timeline of one order under the co-occupancy evaluator M2 (Eqs. 18-30),
      in plain words, with the model's time symbols under each key moment.

Version history:
  v2 (2026-09-25 morning): drawn at printed size, 7 pt minimum, Arial + STIX.
  v3 (2026-09-25): pictorial redesign for non-specialist readers; Times New Roman
      throughout (math letters in Times New Roman, missing symbols from STIX);
      stacked panels at 15.0 cm width; same palette; built-in layout check.
  v4 (2026-09-25 evening): "car" made explicit for non-specialist readers: the car in
      shaft 2 is labeled "elevator car", the roof label reads "(one car each)", and the
      sharing note says "one elevator car". Everything else as in v3.

Stylized durations only; no experimental values.

Run:  python -m src.figure_section3_schematic [output_dir]
      (default output_dir: prototype/results/figures)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import _mathtext
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

FIG_DIR = Path(__file__).resolve().parents[1] / "results" / "figures"
BASENAME = "fig1_section3_setting"

# ---------------------------------------------------------------- page geometry
FIG_W_CM, FIG_H_CM = 15.0, 10.2
FIG_W_IN, FIG_H_IN = FIG_W_CM / 2.54, FIG_H_CM / 2.54
W, H = FIG_W_IN * 72.0, FIG_H_IN * 72.0          # drawing units = points at printed size

FS = 7.5            # labels (7 pt is the floor)
FS_HEAD = 8.0       # headings
FS_PANEL = 10.0     # panel letters


# matplotlib 3.9 reads the PCLT xHeight of Times New Roman as if it were in
# 26.6 fixed-point units, which doubles the offsets of sub- and superscripts.
# Use the height of the glyph "x" instead (matplotlib's own fallback for fonts
# without a PCLT table) and the STIX spacing constants (a Times design).
def _glyph_xheight(self, fontname, fontsize, dpi):
    metrics = self.get_metrics(fontname, plt.rcParams["mathtext.default"], "x", fontsize, dpi)
    return metrics.iceberg


_mathtext.TruetypeFonts.get_xheight = _glyph_xheight
_mathtext._font_constant_mapping["Times New Roman"] = _mathtext.STIXFontConstants

plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": FS,
    "mathtext.fontset": "custom",
    "mathtext.rm": "Times New Roman",
    "mathtext.it": "Times New Roman:italic",
    "mathtext.bf": "Times New Roman:bold",
    "mathtext.fallback": "stix",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

# ---------------------------------------------------------------- palette (author's version)
INK = "#24313d"
C_SRC = "#396d6f"          # teal: step markers
C_DST = "#ad723f"          # orange: order loads, drop-off points, sharing
C_AMR = "#3b6992"          # AMR body
C_CAR = "#75818b"          # elevator car
C_SHAFT = "#e9edf1"
C_WALL = "#8e9aa6"
C_SLAB = "#c7d0d8"
C_INSIDE = "#f7f9fb"
C_RACK = "#8a96a2"
C_RACK_FILL = "#eef1f4"
C_BOX = "#d9ccb8"          # other stock / orders not selected
C_IDLE = "#d0d7dd"
C_TRIP = "#f3f5f7"
C_TRIP_HATCH = "#b9c6d2"
C_SERV = "#bedcd8"
C_RIDE = "#e7ecf0"
C_WAIT = "#cdd4da"
C_REPO = "#d6e6f0"
C_LOAD = "#e8d6b7"
C_TRAV = "#b0cadd"
C_UNLD = "#f1e7d5"
C_SOFT = "#5b6874"         # secondary text

TEXTS = []          # (artist, tag, container bbox or None)
OBSTACLES = []      # (bbox, allowed tags)


# ---------------------------------------------------------------- primitives
def text(ax, x, y, s, tag, container=None, **kw):
    kw.setdefault("color", INK)
    kw.setdefault("fontsize", FS)
    kw.setdefault("zorder", 12)
    t = ax.text(x, y, s, **kw)
    TEXTS.append((t, tag, container))
    return t


def obstacle(x0, y0, x1, y1, allowed=()):
    OBSTACLES.append(((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)), set(allowed)))


def arrow(ax, x0, y0, x1, y1, color=INK, dashed=False, lw=0.9, allowed=()):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=(0, (2.4, 1.6)) if dashed else "-",
                                shrinkA=0, shrinkB=0, mutation_scale=6.5), zorder=8)
    obstacle(min(x0, x1) - 1.8, min(y0, y1) - 1.8, max(x0, x1) + 1.8, max(y0, y1) + 1.8, allowed)


def robot(ax, x, y, w=12.0, load=False):
    """AMR icon standing on a surface at height y; x is its left end."""
    r = 1.45
    body_y = y + 1.9
    ax.add_patch(FancyBboxPatch((x, body_y), w, 5.6, boxstyle="round,pad=0,rounding_size=1.3",
                                facecolor=C_AMR, edgecolor=INK, linewidth=0.45, zorder=9))
    ax.add_patch(Rectangle((x + w - 3.4, body_y + 2.3), 2.2, 1.9, facecolor="#cfe0ee",
                           edgecolor="none", zorder=10))
    for cx in (x + 2.6, x + w - 2.6):
        ax.add_patch(Circle((cx, y + r), r, facecolor=INK, edgecolor="none", zorder=10))
    top = body_y + 5.6
    if load:
        top = parcel(ax, x + w / 2 - 3.2, top, register=False)
    obstacle(x, y, x + w, top)
    return top


def parcel(ax, x, y, w=6.4, h=5.2, color=C_DST, register=True):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor=INK, linewidth=0.4, zorder=10))
    ax.plot([x + w / 2, x + w / 2], [y, y + h], color="#f4e3cf" if color == C_DST else "#efe6d8",
            lw=0.7, zorder=11, solid_capstyle="butt")
    if register:
        obstacle(x, y, x + w, y + h)
    return y + h


def flag(ax, x, y):
    """Drop-off point on a floor at height y, centred at x."""
    ax.add_patch(Rectangle((x - 8.0, y + 0.3), 16.0, 2.4, facecolor="none", edgecolor=C_DST,
                           linewidth=0.6, linestyle=(0, (1.6, 1.0)), zorder=6))
    ax.plot([x, x], [y + 0.3, y + 13.0], color=INK, lw=0.7, zorder=7)
    ax.add_patch(Polygon([(x, y + 13.0), (x + 8.0, y + 10.8), (x, y + 8.6)], closed=True,
                         facecolor=C_DST, edgecolor=INK, linewidth=0.4, zorder=8))
    obstacle(x - 8.0, y, x + 8.2, y + 13.2)


def rack(ax, x0, y0, loads=(), boxes=(), w=34.0, h=17.0):
    """Storage rack on a floor at height y0; loads = [(level, x offset)] are order loads."""
    ax.add_patch(Rectangle((x0, y0), w, h, facecolor=C_RACK_FILL, edgecolor=C_RACK,
                           linewidth=0.6, zorder=4))
    for lv in (1, 2):
        ax.plot([x0, x0 + w], [y0 + lv * h / 3] * 2, color=C_RACK, lw=0.6, zorder=4)
    for lv, dx in boxes:
        ax.add_patch(Rectangle((x0 + dx, y0 + lv * h / 3 + 0.4), 5.0, 4.2, facecolor=C_BOX,
                               edgecolor="#a99b86", linewidth=0.35, zorder=5))
    for lv, dx in loads:
        parcel(ax, x0 + dx, y0 + lv * h / 3 + 0.4, register=False)
    obstacle(x0, y0, x0 + w, y0 + h)


def step(ax, x, y, n):
    ax.add_patch(Circle((x, y), 4.4, facecolor=C_SRC, edgecolor="white", linewidth=0.5, zorder=13))
    text(ax, x, y - 0.25, str(n), "step", color="white", fontsize=7.0, fontweight="bold",
         ha="center", va="center", zorder=14, container=(x - 4.4, y - 4.4, x + 4.4, y + 4.4))
    obstacle(x - 4.4, y - 4.4, x + 4.4, y + 4.4, allowed={"step"})


def car_icon(ax, x, y, w=11.0, h=15.0):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=C_SHAFT, edgecolor=C_WALL, linewidth=0.6, zorder=4))
    ax.add_patch(Rectangle((x + 1.3, y + 1.3), w - 2.6, h - 4.2, facecolor=C_CAR, edgecolor=INK,
                           linewidth=0.4, zorder=5))
    ax.plot([x + w / 2] * 2, [y + 1.3, y + h - 2.9], color="white", lw=0.5, zorder=6)
    ax.plot([x + w / 2] * 2, [y + h - 2.9, y + h], color=C_WALL, lw=0.5, zorder=5)
    obstacle(x, y, x + w, y + h)


# ---------------------------------------------------------------- panel (a)
def panel_warehouse(ax) -> None:
    text(ax, 2.0, H - 1.5, "(a)", "panel", fontsize=FS_PANEL, fontweight="bold", ha="left", va="top")

    # ---- left column: order pool -> wave -> decision
    text(ax, 58.0, H - 9.0, "Order pool", "head", fontsize=FS_HEAD, fontweight="bold",
         ha="center", va="center")
    picked = {(0, 2), (1, 0), (1, 5)}                 # the n orders that form W
    for row, yb in enumerate((260.5, 252.5)):
        for col in range(7):
            parcel(ax, 23.0 + 10.0 * col, yb, w=6.6, h=5.4,
                   color=C_DST if (row, col) in picked else C_BOX)
    arrow(ax, 18.0, 251.0, 18.0, 240.5)
    text(ax, 24.0, 245.5, "select $n$ orders", "left", ha="left", va="center")
    tk = (6.0, 164.0, 106.0, 236.0)
    ax.add_patch(FancyBboxPatch((tk[0], tk[1]), tk[2] - tk[0], tk[3] - tk[1],
                                boxstyle="round,pad=0,rounding_size=2.0", facecolor="white",
                                edgecolor=INK, linewidth=0.7, zorder=3))
    ax.add_patch(FancyBboxPatch((46.0, 233.0), 20.0, 5.5, boxstyle="round,pad=0,rounding_size=1.2",
                                facecolor=C_CAR, edgecolor=INK, linewidth=0.5, zorder=4))
    obstacle(tk[0], tk[1], tk[2], tk[3] + 2.5, allowed={"ticket"})
    text(ax, 56.0, 223.0, "Wave $W$", "ticket", fontsize=FS_HEAD, fontweight="bold",
         ha="center", va="center", container=tk)
    rows = [("$o_1$", "floor 1", "floor 3"), ("$o_2$", "floor $F$", "floor 2"),
            ("$o_3$", "floor 2", "floor 2")]
    for i, (o, a, b) in enumerate(rows):
        text(ax, 12.0, 210.0 - 11.0 * i, f"{o}: {a} $\\rightarrow$ {b}", "ticket",
             ha="left", va="center", container=tk)
    text(ax, 56.0, 174.0, "released together at $t_W$", "ticket", style="italic",
         ha="center", va="center", container=tk)
    text(ax, 56.0, 155.0, "Decision: which orders enter $W$?", "left", fontweight="bold",
         ha="center", va="center")

    # ---- building cross-section
    xl, xr = 116.0, 394.0
    fl = [150.0, 181.0, 212.0, 243.0]                 # floor surfaces: 1, 2, 3, F
    roof = 274.0
    ax.add_patch(Rectangle((xl, fl[0]), xr - xl, roof - fl[0], facecolor=C_INSIDE,
                           edgecolor="none", zorder=0))
    for y in fl[1:] + [roof]:
        ax.add_patch(Rectangle((xl, y - 2.6), xr - xl, 2.6, facecolor=C_SLAB, edgecolor=C_WALL,
                               linewidth=0.4, zorder=2))
        obstacle(xl, y - 2.6, xr, y)
    ax.add_patch(Rectangle((xl - 3.0, fl[0] - 3.0), xr - xl + 6.0, 3.0, facecolor=C_WALL,
                           edgecolor="none", zorder=2))
    obstacle(xl - 3.0, fl[0] - 3.0, xr + 3.0, fl[0])
    for x in (xl, xr):
        ax.plot([x, x], [fl[0], roof], color=C_WALL, lw=1.0, zorder=2)
        obstacle(x - 0.6, fl[0], x + 0.6, roof)
    for y, nm in zip(fl, ["Floor 1", "Floor 2", "Floor 3", "Floor $F$"]):
        text(ax, xr + 3.0, y + 12.0, nm, "floor", ha="left", va="center")

    # elevators: two shafts, both cars on floor 1 at t_W
    shafts = [(124.0, 140.0), (144.0, 160.0)]
    for sx0, sx1 in shafts:
        ax.add_patch(Rectangle((sx0, fl[0]), sx1 - sx0, roof - 2.6 - fl[0], facecolor=C_SHAFT,
                               edgecolor=C_WALL, linewidth=0.6, zorder=3))
        cx0, cx1 = sx0 + 1.6, sx1 - 1.6
        ax.add_patch(Rectangle((cx0, fl[0] + 0.8), cx1 - cx0, 17.0, facecolor=C_CAR,
                               edgecolor=INK, linewidth=0.5, zorder=5))
        ax.plot([(cx0 + cx1) / 2] * 2, [fl[0] + 0.8, fl[0] + 17.8], color="white", lw=0.6, zorder=6)
        ax.plot([(cx0 + cx1) / 2] * 2, [fl[0] + 17.8, roof - 2.6], color=C_WALL, lw=0.5, zorder=4)
        obstacle(sx0, fl[0], sx1, roof - 2.6)
    text(ax, xl + 2.0, roof + 5.2, "$E$ shared elevators (one car each)", "roof",
         ha="left", va="center")
    # name the cabin itself: the car of elevator 2, parked on floor 1
    ax.plot([163.0, 156.5], [172.0, 164.5], color=INK, lw=0.5, zorder=9)
    text(ax, 164.0, fl[0] + 23.5, "elevator car", "carlabel", ha="left", va="center")

    # racks with other stock; order loads in orange
    rack(ax, 236.0, fl[0], loads=[(0, 13.0)], boxes=((1, 4), (2, 20), (1, 24)))
    text(ax, 253.0, fl[0] + 22.0, "$o_1$", "order", color=C_DST, ha="center", va="center")
    rack(ax, 290.0, fl[1], loads=[(1, 14.0)], boxes=((0, 4), (2, 22), (0, 24)))
    text(ax, 307.0, fl[1] + 22.0, "$o_3$", "order", color=C_DST, ha="center", va="center")
    rack(ax, 290.0, fl[2], boxes=((0, 6), (1, 18), (2, 4), (2, 24)))
    rack(ax, 290.0, fl[3], loads=[(2, 12.0)], boxes=((0, 4), (1, 22)))
    text(ax, 307.0, fl[3] + 22.0, "$o_2$", "order", color=C_DST, ha="center", va="center")

    # drop-off points
    for x, f, o in ((236.0, 2, "$o_1$"), (214.0, 1, "$o_2$"), (368.0, 1, "$o_3$")):
        flag(ax, x, fl[f])
        text(ax, x + 11.0, fl[f] + 8.5, o, "order", color=C_DST, ha="left", va="center")

    # AMR fleet on floor 1 at t_W
    for x in (322.0, 339.0, 356.0):
        robot(ax, x, fl[0])
    text(ax, 345.0, fl[0] + 15.5, "AMRs at $t_W$", "amr", color=C_AMR, ha="center", va="center")

    # trip of o_1: 1 go to the load, 2 pick it up, 3 ride up, 4 drop it off
    arrow(ax, 320.0, fl[0] + 5.0, 272.5, fl[0] + 5.0, dashed=True)
    step(ax, 296.0, fl[0] + 13.0, 1)
    text(ax, 296.0, fl[0] + 22.5, "go to the load", "stepl", ha="center", va="center")
    step(ax, 226.0, fl[0] + 13.0, 2)
    text(ax, 219.5, fl[0] + 13.0, "pick it up", "stepl", ha="right", va="center")
    arrow(ax, 234.0, fl[0] + 5.0, 161.0, fl[0] + 5.0, dashed=True)
    xs = (shafts[1][0] + shafts[1][1]) / 2
    arrow(ax, xs, fl[0] + 19.0, xs, fl[2] + 0.2, lw=1.1)
    gx0, gx1 = shafts[1][0] + 1.6, shafts[1][1] - 1.6     # the same car later, on floor 3
    ax.add_patch(Rectangle((gx0, fl[2] + 0.8), gx1 - gx0, 17.0, facecolor=C_SHAFT, edgecolor=INK,
                           linewidth=0.5, linestyle=(0, (1.6, 1.0)), zorder=7))
    robot(ax, gx0 + 1.4, fl[2] + 1.2, w=10.0, load=True)
    step(ax, 170.0, fl[1] + 14.0, 3)
    text(ax, 176.5, fl[1] + 14.0, "ride up", "stepl", ha="left", va="center")
    arrow(ax, 161.0, fl[2] + 5.0, 227.0, fl[2] + 5.0, dashed=True)
    step(ax, 186.0, fl[2] + 15.5, 4)
    text(ax, 192.5, fl[2] + 15.5, "drop it off", "stepl", ha="left", va="center")

    # o_3 stays on its floor; o_2 needs a ride down (not traced)
    arrow(ax, 325.0, fl[1] + 5.0, 359.5, fl[1] + 5.0, dashed=True)
    text(ax, 327.0, fl[1] + 19.5, "stays on floor 2", "note", color=C_SOFT, ha="left", va="center")

    # sharing rule, next to the shafts
    text(ax, 170.0, fl[3] + 15.0, "one elevator car carries up to $c$ AMRs\nthat go between the same floors",
         "note", color=C_SOFT, ha="left", va="center", linespacing=1.15)

    # ---- legend strip
    yl = 138.0
    robot(ax, 4.0, yl - 4.2)
    text(ax, 19.5, yl, "AMR (autonomous mobile robot)", "legend", ha="left", va="center")
    parcel(ax, 128.0, yl - 2.6)
    text(ax, 138.0, yl, "load of an order in $W$", "legend", ha="left", va="center")
    flag(ax, 219.0, yl - 6.5)
    text(ax, 231.0, yl, "drop-off point", "legend", ha="left", va="center")
    arrow(ax, 281.0, yl, 299.0, yl, dashed=True)
    text(ax, 303.0, yl, "moves on a floor", "legend", ha="left", va="center")
    arrow(ax, 361.0, yl, 379.0, yl, lw=1.1)
    text(ax, 383.0, yl, "elevator ride", "legend", ha="left", va="center")


# ---------------------------------------------------------------- panel (b)
def panel_timeline(ax) -> None:
    text(ax, 2.0, 126.0, "(b)", "panel", fontsize=FS_PANEL, fontweight="bold", ha="left", va="top")
    x0 = 58.0
    t = {"free": 0, "ready": 53, "atS": 119, "P": 145, "B": 189, "R": 247, "L": 273, "V": 302,
         "D": 335, "C": 360}
    X = {k: x0 + v for k, v in t.items()}
    amr = (80.0, 99.0)
    car = (29.0, 48.0)

    # lane headers with icons
    robot(ax, 3.0, amr[0] + 5.5)
    text(ax, 18.5, (amr[0] + amr[1]) / 2, "AMR", "lanehead", fontsize=FS_HEAD, fontweight="bold",
         ha="left", va="center")
    car_icon(ax, 3.5, car[0] + 2.0)
    text(ax, 18.5, (car[0] + car[1]) / 2, "elevator\ncar", "lanehead", fontsize=FS_HEAD,
         fontweight="bold", ha="left", va="center", linespacing=1.05)

    def seg(lane, a, b, color, label, hatch=None):
        xa, xb = X[a], X[b]
        if hatch:
            ax.add_patch(Rectangle((xa, lane[0]), xb - xa, lane[1] - lane[0], facecolor=color,
                                   edgecolor=C_TRIP_HATCH, hatch=hatch, linewidth=0, zorder=2))
            ax.add_patch(Rectangle((xa, lane[0]), xb - xa, lane[1] - lane[0], facecolor="none",
                                   edgecolor=INK, linewidth=0.6, zorder=3))
        else:
            ax.add_patch(Rectangle((xa, lane[0]), xb - xa, lane[1] - lane[0], facecolor=color,
                                   edgecolor=INK, linewidth=0.6, zorder=2))
        extra = {"bbox": dict(facecolor=color, edgecolor="none", pad=0.4)} if hatch else {}
        text(ax, (xa + xb) / 2, (lane[0] + lane[1]) / 2, label, "seg", ha="center", va="center",
             linespacing=1.05, container=(xa, lane[0], xb, lane[1]), **extra)

    # AMR lane
    seg(amr, "free", "ready", C_IDLE, "waits for\nthe order")
    seg(amr, "ready", "atS", C_TRIP, "rides to the pickup\nfloor (if elsewhere)", hatch="////")
    seg(amr, "atS", "P", C_SERV, "picks\nup")
    seg(amr, "P", "D", C_RIDE, "waits for a car, then rides with the load")
    seg(amr, "D", "C", C_SERV, "drops\noff")
    obstacle(X["free"], amr[0], X["C"], amr[1], allowed={"seg"})
    # elevator lane: the car that serves the loaded ride
    seg(car, "P", "B", C_WAIT, "finishes\nearlier trips")
    seg(car, "B", "R", C_REPO, "moves empty to\nthe pickup floor")
    seg(car, "R", "L", C_LOAD, "loads")
    seg(car, "L", "V", C_TRAV, "travels")
    seg(car, "V", "D", C_UNLD, "unloads")
    obstacle(X["P"], car[0], X["D"], car[1], allowed={"seg"})

    # key moments: plain words, then the model symbol
    def mark_top(key, words, sym, ha="center"):
        ax.plot([X[key]] * 2, [amr[1], amr[1] + 3.5], color=INK, lw=0.6)
        text(ax, X[key], amr[1] + 4.0, f"{words}\n{sym}", "mark", ha=ha, va="bottom",
             linespacing=1.1, multialignment=ha)

    def mark_bot(key, words, sym):
        ax.plot([X[key]] * 2, [car[0] - 3.5, car[0]], color=INK, lw=0.6)
        text(ax, X[key], car[0] - 4.0, f"{words}\n{sym}", "mark", ha="center", va="top",
             linespacing=1.1, multialignment="center")

    mark_top("free", "AMR free", "$H_{a_j}^{j-1}$", ha="left")
    mark_top("ready", "order ready", "$t_j^0=t_W+r_o$")
    mark_top("P", "load picked up", "$t_j^P$")
    mark_top("C", "delivered", "$t_j^C$", ha="right")
    mark_bot("P", "car called", "$t=t_j^P$")
    mark_bot("B", "car free", "$B_e$")
    mark_bot("L", "doors close", "$L_e$")
    mark_bot("D", "trip ends", "$D_e=t_j^D$")

    # the AMR calls a car; the car returns it to the AMR lane at the end of the trip
    arrow(ax, X["P"], amr[0], X["P"], car[1])
    arrow(ax, X["D"], car[1], X["D"], amr[0])

    # time direction
    ym = (car[1] + amr[0]) / 2
    arrow(ax, x0 + 4.0, ym, X["P"] - 30.0, ym, color=C_SOFT, lw=0.7)
    text(ax, X["P"] - 27.0, ym, "time", "axis", color=C_SOFT, ha="left", va="center")

    # another AMR joins the trip while the doors are open
    xj = (X["R"] + X["L"]) / 2
    robot(ax, xj - 6.0, car[1] + 1.5, load=True)
    text(ax, xj - 10.0, ym, "another AMR going between\nthe same floors can still board\nuntil the doors close",
         "note", color=C_DST, ha="right", va="center", linespacing=1.1, multialignment="right")


# ---------------------------------------------------------------- layout check
def _bbox_pt(artist, renderer, fig):
    bb = artist.get_window_extent(renderer)
    s = 72.0 / fig.dpi
    return (bb.x0 * s, bb.y0 * s, bb.x1 * s, bb.y1 * s)


def _overlap(a, b, tol=0.0):
    return min(a[2], b[2]) - max(a[0], b[0]) > tol and min(a[3], b[3]) - max(a[1], b[1]) > tol


def check_layout(fig) -> list:
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    problems = []
    items = [(t, tag, cont, _bbox_pt(t, renderer, fig)) for t, tag, cont in TEXTS]
    for t, tag, cont, bb in items:
        name = t.get_text().replace("\n", " / ")
        if bb[0] < 0.5 or bb[1] < 0.5 or bb[2] > W - 0.5 or bb[3] > H - 0.5:
            problems.append(f"outside canvas: {name}")
        if cont is not None:
            pad = 0.6 if tag == "step" else 1.2
            if (bb[0] < cont[0] + pad or bb[2] > cont[2] - pad
                    or bb[1] < cont[1] + 0.5 or bb[3] > cont[3] - 0.5):
                problems.append(f"touches its box border: {name}")
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if _overlap(items[i][3], items[j][3], tol=0.2):
                problems.append(f"labels overlap: {items[i][0].get_text()!r} and {items[j][0].get_text()!r}")
    for ob, allowed in OBSTACLES:
        for t, tag, cont, bb in items:
            if tag not in allowed and cont is None and _overlap(bb, ob, tol=0.3):
                problems.append(f"label crosses a drawn element: {t.get_text()!r} at "
                                f"{tuple(round(v) for v in ob)}")
    return problems


def main(argv=None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    outdir = Path(argv[0]) if argv else FIG_DIR
    outdir.mkdir(parents=True, exist_ok=True)
    TEXTS.clear()
    OBSTACLES.clear()
    fig = plt.figure(figsize=(FIG_W_IN, FIG_H_IN))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    panel_warehouse(ax)
    panel_timeline(ax)
    problems = check_layout(fig)
    smallest = min(t.get_fontsize() for t, *_ in TEXTS)
    fonts = sorted({t.get_fontname() for t, *_ in TEXTS})
    print(f"  size {FIG_W_CM:.1f} x {FIG_H_CM:.1f} cm; smallest label {smallest:.1f} pt; "
          f"{len(TEXTS)} labels checked; fonts {fonts}")
    if problems:
        for p in problems:
            print("  LAYOUT PROBLEM:", p)
        preview = outdir / f"{BASENAME}_preview_FAILED.png"
        fig.savefig(preview, dpi=300)
        raise SystemExit(f"{len(problems)} layout problem(s); preview written to {preview}")
    for ext, dpi in (("pdf", None), ("png", 600)):
        out = outdir / f"{BASENAME}.{ext}"
        fig.savefig(out, dpi=dpi)
        print(f"  wrote {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
