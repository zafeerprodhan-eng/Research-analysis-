import csv
import os
import matplotlib.pyplot as plt

import plotstyle as ps

HERE = os.path.dirname(os.path.abspath(__file__))
ps.setup()

with open(os.path.join(HERE, "data", "speed_and_time_history.csv")) as fh:
    rows = list(csv.DictReader(fh))

year = [float(r["year"]) for r in rows]
speed = [float(r["max_speed_kmh"]) for r in rows]
best = [float(r["fastest_tokyo_osaka_min"]) for r in rows]
shk = [r["era"] == "shinkansen" for r in rows]

END = 2026.6
cut = shk.index(True)


def draw(ax, vals):
    """step plot, grey before the Shinkansen opened and blue after"""
    x = year + [END]
    ax.step(x[:cut + 1], vals[:cut] + [vals[cut - 1]], where="post",
            color=ps.LEGACY, lw=2)
    ax.step(x[cut:], vals[cut:] + [vals[-1]], where="post",
            color=ps.NOZOMI, lw=2)
    ax.plot(year[:cut], vals[:cut], "o", color=ps.LEGACY, ms=5)
    ax.plot(year[cut:], vals[cut:], "o", color=ps.NOZOMI, ms=5)


def changed(vals):
    return [i == 0 or v != vals[i - 1] for i, v in enumerate(vals)]


fig, (top, bot) = plt.subplots(2, 1, figsize=(7.5, 6), sharex=True)

draw(top, speed)
for y, v, new in zip(year, speed, changed(speed)):
    if new:
        # 200 and 210 are one year apart, so 200 goes below its point
        dx, dy = {200: (-34, -13), 210: (2, 7)}.get(v, (4, 6))
        top.annotate("%.0f" % v, (y, v), textcoords="offset points",
                     xytext=(dx, dy), fontsize=9)
top.annotate("opened at 200 km/h,\nraised to 210 in Nov 1965",
             xy=(1964.8, 200), xytext=(1978, 150), fontsize=8.5,
             arrowprops=dict(arrowstyle="->", color="gray"))
top.set_ylim(80, 330)
top.set_ylabel("Maximum speed (km/h)")
top.set_title("(a)  What the track allows")
top.grid(alpha=0.3)
top.set_axisbelow(True)

draw(bot, best)
for y, v, new in zip(year, best, changed(best)):
    if new:
        dx, dy = (-34, 6) if v == 142 else (4, 6)
        bot.annotate("%dh%02dm" % (v // 60, v % 60), (y, v),
                     textcoords="offset points", xytext=(dx, dy), fontsize=9)

bot.axhline(234, color=ps.KODAMA, ls="--", lw=1.2)
bot.plot(2026.5, 234, "o", color=ps.KODAMA, ms=8)
bot.annotate("Kodama 836 (this study): 3h54m\nsame track, same trains, 15 more stops",
             xy=(2026, 234), xytext=(1988, 300), fontsize=8.5, color=ps.KODAMA,
             arrowprops=dict(arrowstyle="->", color=ps.KODAMA))

bot.set_ylim(90, 450)
bot.set_yticks([120, 180, 240, 300, 360, 420])
bot.set_yticklabels(["2h", "3h", "4h", "5h", "6h", "7h"])
bot.set_ylabel("Fastest Tokyo–Osaka time")
bot.set_xlim(1955, 2032)
bot.set_xlabel("Year")
bot.set_title("(b)  What the passenger gets")
bot.grid(alpha=0.3)
bot.set_axisbelow(True)

fig.tight_layout()
ps.save(fig, "fig03_speed_history", os.path.join(HERE, "..", "figures"))
