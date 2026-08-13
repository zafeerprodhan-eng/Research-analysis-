import csv
import os
import matplotlib.pyplot as plt

import plotstyle as ps

HERE = os.path.dirname(os.path.abspath(__file__))
ps.setup()

with open(os.path.join(HERE, "data", "tokaido_stations.csv")) as fh:
    rows = list(csv.DictReader(fh))

names = [r["station"] for r in rows]
km = [float(r["chainage_km"]) for r in rows]
assert abs(km[-1] - 515.4) < 0.05, km[-1]
print("17 stations, %.1f km" % km[-1])

patterns = [("Kodama (all stations)", "kodama_stop", ps.KODAMA, 3),
            ("Hikari (typical)", "hikari_typical_stop", ps.HIKARI, 2),
            ("Nozomi (fastest)", "nozomi_stop", ps.NOZOMI, 1)]

fig, ax = plt.subplots(figsize=(7.5, 3.4))

for label, key, color, y in patterns:
    ax.plot([0, km[-1]], [y, y], color=color, lw=2)
    stops = [k for k, r in zip(km, rows) if r[key] == "1"]
    ax.plot(stops, [y] * len(stops), "o", color=color, ms=6)
    ax.text(525, y, "%d stops" % len(stops), va="center", fontsize=8.5, color=color)

# station names above the top line
for k, n in zip(km, names):
    ax.plot([k, k], [3.15, 3.3], color="0.6", lw=0.6)
    ax.text(k, 3.4, n, rotation=90, ha="center", va="bottom", fontsize=7)

ax.annotate("", xy=(25.5, 0.5), xytext=(76.7, 0.5),
            arrowprops=dict(arrowstyle="<->", color="0.4", lw=0.8))
ax.text(51, 0.35, "51.2 km", ha="center", va="top", fontsize=8)
ax.annotate("", xy=(408.2, 0.5), xytext=(476.3, 0.5),
            arrowprops=dict(arrowstyle="<->", color="0.4", lw=0.8))
ax.text(442, 0.35, "68.1 km (longest gap)", ha="center", va="top", fontsize=8)

ax.set_yticks([1, 2, 3])
ax.set_yticklabels(["Nozomi\n(fastest)", "Hikari\n(typical)", "Kodama\n(all stations)"])
ax.set_ylim(0, 7.2)
ax.set_xlim(-15, 590)
ax.set_xlabel("Distance from Tokyo (km)")
ax.grid(axis="x", alpha=0.3)
ax.set_axisbelow(True)

ps.save(fig, "fig01_route", os.path.join(HERE, "..", "figures"))
