import os
import matplotlib.pyplot as plt

NOZOMI = "tab:blue"
HIKARI = "tab:green"
KODAMA = "tab:orange"
LEGACY = "tab:gray"
RAIL = "tab:green"
AIR = "tab:gray"


def setup():
    plt.rcParams.update({
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "legend.fontsize": 8.5,
        "figure.autolayout": False,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


def save(fig, stem, outdir="../figures"):
    os.makedirs(outdir, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(outdir, stem + "." + ext))
    plt.close(fig)
    print("  " + stem)
