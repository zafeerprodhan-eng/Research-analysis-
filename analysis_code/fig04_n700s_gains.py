import os
import matplotlib.pyplot as plt

import plotstyle as ps

HERE = os.path.dirname(os.path.abspath(__file__))
ps.setup()

# (label, low%, high%, group)
ROWS = [
    ("Converter energy loss per phase\n(vs Si IGBT, N700A)", 30, 30, 0),
    ("Conversion system mass, Full-SiC\n(vs Si IGBT, N700A)", 30, 30, 0),
    ("Conversion system mass, Hybrid-SiC\n(vs Si IGBT, N700A)", 20, 20, 0),
    ("Conversion system width\n(vs Series N700)", 50, 50, 1),
    ("Traction motor mass per kW\n(6-pole vs 4-pole)", 20, 20, 1),
    ("Traction motor axial length\n(6-pole vs 4-pole)", 10, 10, 1),
    ("Whole traction system mass\n(vs Series N700)", 20, 20, 1),
    ("Emergency braking distance\n(vs N700A)", 5, 5, 2),
    ("Electricity used in service\n(vs N700A)", 6, 7, 2),
]

GROUPS = ["Semiconductor level", "Equipment level", "Whole-train level"]
COLORS = [ps.NOZOMI, ps.HIKARI, ps.KODAMA]

labels = [r[0] for r in ROWS]
highs = [r[2] for r in ROWS]
lows = [r[1] for r in ROWS]
groups = [r[3] for r in ROWS]
pos = range(len(ROWS))[::-1]          # first row at the top

fig, ax = plt.subplots(figsize=(7.5, 5))

ax.barh(list(pos), highs, color=[COLORS[g] for g in groups], height=0.65)

# the one row where two sources disagree
for p, lo, hi, g in zip(pos, lows, highs, groups):
    if lo != hi:
        ax.barh([p], [hi - lo], left=lo, height=0.65, color="white",
                edgecolor=COLORS[g], hatch="///")

for p, lo, hi in zip(pos, lows, highs):
    txt = "%d%%" % hi if lo == hi else "%d-%d%%" % (lo, hi)
    ax.text(hi + 1, p, txt, va="center", fontsize=9)

ax.set_yticks(list(pos))
ax.set_yticklabels(labels, fontsize=8.5)
ax.set_xlim(0, 58)
ax.set_xlabel("Reduction vs the stated baseline (%)")
ax.grid(axis="x", alpha=0.3)
ax.set_axisbelow(True)

handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in COLORS]
ax.legend(handles, GROUPS, loc="lower right")

fig.tight_layout()
ps.save(fig, "fig04_n700s_gains", os.path.join(HERE, "..", "figures"))
