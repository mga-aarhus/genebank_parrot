# plot_ranks.py - top-N taxa per rank, log scale
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RES = os.path.expanduser("~/results")
RANKS = ["superkingdom", "kingdom", "phylum", "class",
         "order", "family", "genus", "species"]
TOP = 15

fig, axes = plt.subplots(4, 2, figsize=(14, 18))
for ax, rank in zip(axes.flat, RANKS):
    df = pd.read_csv(f"{RES}/counts_{rank}.tsv", sep="\t").head(TOP)
    ax.barh(df[rank][::-1], df["n_sequences"][::-1])
    ax.set_xscale("log")
    ax.set_title(f"{rank} (top {TOP})")
plt.tight_layout()
plt.savefig(f"{RES}/rank_representation.png", dpi=150)
