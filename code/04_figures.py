"""Step 4: figures. Writes paper/figures/fig1_coercivity_by_route.png (and .svg).

Plain-language note: this draws the first composition-process-property map.
Each dot is one published coercivity, placed by processing route and colored by
what kind of sample was measured. Figures carry a DRAFT stamp until you approve;
run with --final to remove it. You do not need to open this file.
"""
import argparse
import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / "data" / "processed"
F = ROOT / "paper" / "figures"

# reference categorical palette, slots 1-3 (validated all-pairs for scatter forms)
FORM_COLOR = {"powder": "#2a78d6", "aligned powder": "#eb6834", "bulk magnet": "#1baf7a"}
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"


def form_group(f):
    f = f.lower()
    if "bulk" in f:
        return "bulk magnet"
    if "aligned" in f:
        return "aligned powder"
    return "powder"


def route(s):
    r = s["alloy_route"].lower()
    if "plasma" in r:
        return "Thermal plasma (TbCu7)"
    if "spray pyrolysis" in r:
        return "Spray pyrolysis + R-D"
    if "strip" in r:
        return "Strip cast + milling"
    if "commercial" in r and s["consolidation"]:
        return "Commercial powder, hot-pressed"
    if "commercial" in r:
        return "Commercial powder + milling"
    if "reduction-diffusion" in r and s["consolidation"]:
        return "R-D powder, SPS-sintered"
    if "reduction-diffusion" in r:
        return "R-D powder"
    return "Other"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--final", action="store_true")
    a = ap.parse_args()
    samples = {r["sample_id"]: r for r in csv.DictReader((P / "opensmfe_samples.csv").open(encoding="utf-8"))}
    meas = [m for m in csv.DictReader((P / "opensmfe_measurements.csv").open(encoding="utf-8"))
            if m["property"].startswith("Hc")]
    rows = []
    for m in meas:
        s = samples[m["sample_id"]]
        rows.append((route(s), form_group(s["sample_form"]), float(m["value_si"]), m["comparability"], m["meas_T_K"]))
    order = sorted({r[0] for r in rows}, key=lambda k: max(x[2] for x in rows if x[0] == k))
    ypos = {k: i for i, k in enumerate(order)}

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    for rt, fg, v, g, T in rows:
        c = FORM_COLOR[fg]
        hollow = g == "C"
        ax.scatter(v, ypos[rt], s=70, facecolor=SURF if hollow else c, edgecolor=c if hollow else SURF,
                   linewidth=1.8 if hollow else 1.5, zorder=3)
        if hollow:
            ax.annotate(f"{T} K", (v, ypos[rt]), xytext=(7, 0), textcoords="offset points",
                        va="center", fontsize=8, color=INK2)
    ax.set_xscale("log")
    ax.set_xlim(30, 5000)
    ax.set_xticks([50, 100, 200, 500, 1000, 2000, 5000], ["50", "100", "200", "500", "1000", "2000", "5000"])
    ax.minorticks_off()
    ax.set_yticks(range(len(order)), order, color=INK)
    ax.set_xlabel("Coercivity (kA/m, log scale)", color=INK)
    ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, length=0)
    handles = [plt.Line2D([], [], marker="o", ls="", markersize=8, markerfacecolor=c, markeredgecolor=SURF, label=k)
               for k, c in FORM_COLOR.items()]
    handles.append(plt.Line2D([], [], marker="o", ls="", markersize=8, markerfacecolor=SURF,
                              markeredgecolor=INK2, markeredgewidth=1.6, label="grade C (not room temp.)"))
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=8, labelcolor=INK2)
    fig.suptitle("Published Sm-Fe-N coercivity by processing route", x=0.01, ha="left", fontsize=11, color=INK)
    ax.set_title(f"OpenSmFe v0.1 seed batch, {len(rows)} values", loc="left", fontsize=8.5, color=INK2)
    fig.text(0.01, 0.01, f"Sources: {len({m['source_id'] for m in meas})} open-access papers; each value verified by the author against its source. 1 kOe = 79.58 kA/m.",
             fontsize=7.5, color=INK2)
    if not a.final:
        fig.text(0.5, 0.5, "DRAFT", fontsize=70, color="#d0cfca", alpha=0.35, ha="center", va="center",
                 rotation=20, zorder=0)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    F.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg"):
        fig.savefig(F / f"fig1_coercivity_by_route.{ext}", facecolor=SURF)
    print("wrote", F / "fig1_coercivity_by_route.png")


if __name__ == "__main__":
    main()
