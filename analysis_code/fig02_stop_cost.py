import os
import matplotlib.pyplot as plt
import numpy as np

import plotstyle as ps
from journey_time_model import LINE_KM, V_MAX, SERVICES

HERE = os.path.dirname(os.path.abspath(__file__))
ps.setup()

FLOOR = LINE_KM / V_MAX * 60
(_, t1, n1, _), (_, t2, n2, _) = [s for s in SERVICES if s[3]]
SLOPE = (t2 - t1) / (n2 - n1)
INTER = t1 - SLOPE * n1
KIN = 2.0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.6))

# --- (a) -------------------------------------------------------------
x = np.array([0, 16])
ax1.plot(x, INTER + SLOPE * x, "k-", lw=1.2,
         label="line through both points")
ax1.axhline(FLOOR, color="gray", ls="--", lw=1,
            label="floor: 515.4 km at 285 km/h")

ax1.plot(n1, t1, "o", color=ps.NOZOMI, ms=8, label="Nozomi")
ax1.plot(n2, t2, "o", color=ps.KODAMA, ms=8, label="Kodama 836")

ax1.set_xlim(-1, 17)
ax1.set_ylim(90, 250)
ax1.set_xlabel("Number of intermediate stops")
ax1.set_ylabel("Scheduled journey time (min)")
ax1.set_title("(a)  Each stop costs about 8.5 min")
ax1.legend(loc="upper left")
ax1.grid(alpha=0.3)
ax1.set_axisbelow(True)

# --- (b) -------------------------------------------------------------
# only the first bar is calculated from first principles. the second is
# bounded by the kinematic model, the third is the remainder of the 234 min,
# so the last two carry the range instead of a single number.
KIN_LO, KIN_HI = 1.79, 2.08
brake_lo, brake_hi = 15 * KIN_LO, 15 * KIN_HI
stand_lo, stand_hi = 234 - FLOOR - brake_hi, 234 - FLOOR - brake_lo

labels = ["Running at\nline speed", "Braking and\nre-accelerating",
          "Standing: dwell +\nwaiting to be passed"]
mid = [FLOOR, (brake_lo + brake_hi) / 2, (stand_lo + stand_hi) / 2]
err = [0, (brake_hi - brake_lo) / 2, (stand_hi - stand_lo) / 2]
colors = [ps.NOZOMI, ps.HIKARI, ps.KODAMA]

bars = ax2.bar(labels, mid, yerr=err, color=colors, width=0.6,
               capsize=4, error_kw=dict(ecolor="0.3", lw=1))
for b, m, e in zip(bars, mid, err):
    txt = "%.0f min" % m if e == 0 else "%.0f-%.0f min" % (m - e, m + e)
    ax2.text(b.get_x() + b.get_width() / 2, m + e + 4, txt,
             ha="center", fontsize=9)
    ax2.text(b.get_x() + b.get_width() / 2, m / 2, "%.0f%%" % (100 * m / 234),
             ha="center", va="center", color="white", fontsize=9, weight="bold")

ax2.set_ylim(0, 135)
ax2.set_ylabel("Minutes")
ax2.set_title("(b)  How the 234 min divides")
ax2.grid(axis="y", alpha=0.3)
ax2.set_axisbelow(True)

fig.tight_layout()
ps.save(fig, "fig02_stop_cost", os.path.join(HERE, "..", "figures"))
