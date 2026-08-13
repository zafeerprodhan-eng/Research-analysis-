import os
import matplotlib.pyplot as plt
import numpy as np

import plotstyle as ps

HERE = os.path.dirname(os.path.abspath(__file__))
ps.setup()

# JR Central Integrated Report 2025, Tokyo-Osaka, per seat
RAIL_MJ, AIR_MJ = 90.0, 746.0
RAIL_CO2, AIR_CO2 = 4.2, 50.0
print("per seat: energy 1/%.1f, CO2 1/%.1f" % (AIR_MJ / RAIL_MJ, AIR_CO2 / RAIL_CO2))

names = ["Shinkansen", "Aircraft\n(B777-200)"]
colors = [ps.RAIL, ps.AIR]

fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(9.5, 3.4))

b = a1.bar(names, [RAIL_MJ, AIR_MJ], color=colors, width=0.55)
a1.bar_label(b, fmt="%.0f", padding=3)
a1.set_ylim(0, 880)
a1.set_ylabel("MJ per seat")
a1.set_title("(a)  Energy, Tokyo–Osaka")
a1.grid(axis="y", alpha=0.3)
a1.set_axisbelow(True)

b = a2.bar(names, [RAIL_CO2, AIR_CO2], color=colors, width=0.55)
a2.bar_label(b, fmt="%.1f", padding=3)
a2.set_ylim(0, 59)
a2.set_ylabel("kg CO$_2$ per seat")
a2.set_title("(b)  Carbon, Tokyo–Osaka")
a2.grid(axis="y", alpha=0.3)
a2.set_axisbelow(True)

rail_lf = np.linspace(0.35, 0.95, 100)
for air_lf, ls in [(0.65, ":"), (0.75, "-"), (0.85, "--")]:
    ratio = (AIR_CO2 / air_lf) / (RAIL_CO2 / rail_lf)
    a3.plot(rail_lf * 100, ratio, ls, color=ps.RAIL,
            label="aircraft %d%% full" % (air_lf * 100))

print("sweep gives %.1fx to %.1fx"
      % ((AIR_CO2 / 0.85) / (RAIL_CO2 / 0.35), (AIR_CO2 / 0.65) / (RAIL_CO2 / 0.95)))

a3.axhline(AIR_CO2 / RAIL_CO2, color="gray", ls="--", lw=1)
a3.text(36, 12.4, 'published "1/12"', fontsize=8, color="gray")
a3.set_xlabel("Shinkansen load factor (%)")
a3.set_ylabel("Times worse to fly, per passenger")
a3.set_ylim(4, 19)
a3.set_title("(c)  Per passenger, not per seat")
a3.legend(loc="lower right")
a3.grid(alpha=0.3)
a3.set_axisbelow(True)

fig.tight_layout()
ps.save(fig, "fig05_energy", os.path.join(HERE, "..", "figures"))
