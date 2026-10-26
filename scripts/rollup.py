# rollup.py - aggregate sequence counts per taxonomic rank
import csv
from collections import defaultdict

RANKS = ["species", "genus", "family", "order", "class",
         "phylum", "kingdom", "superkingdom"]

# Load taxid -> sequence count
counts = {}
with open("taxid_counts.tsv") as f:
    for line in f:
        t, n = line.rstrip("\n").split("\t")
        counts[t] = int(n)

# rankedlineage.dmp columns: taxid, name, species, genus, ..., superkingdom
agg = {r: defaultdict(int) for r in RANKS}
with open("rankedlineage.dmp") as f:
    for line in f:
        p = [x.strip() for x in line.split("|")]
        taxid, fields = p[0], p[2:10]
        n = counts.get(taxid)
        if not n:
            continue
        for rank, name in zip(RANKS, fields):
            if name:  # skip empty ranks
                agg[rank][name] += n

# Write one table per rank, sorted by count
for rank in RANKS:
    with open(f"counts_{rank}.tsv", "w", newline="") as out:
        w = csv.writer(out, delimiter="\t")
        w.writerow([rank, "n_sequences"])
        for name, n in sorted(agg[rank].items(), key=lambda x: -x[1]):
            w.writerow([name, n])
    print(rank, len(agg[rank]), "taxa")
