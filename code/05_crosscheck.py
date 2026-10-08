"""Step 5: cross-check OpenSmFe against a text-mined magnetic database.

Plain-language note: a text-mined database is one that software built by
reading papers automatically. This script compares its numbers with ours,
paper by paper. Where both list the same paper and property, we report
whether the values agree. It answers "how often does automatic extraction get
Sm-Fe-N magnet values right?", which is a finding in itself. You do not need
to open this file.

STATUS (v0.1): not run. A text-mined reference database has not been chosen
for this release; the cross-check is planned for a later version. A candidate
is NEMAD (Itani, Zhang and Zang, Nat. Commun. 2025,
doi:10.1038/s41467-025-64458-z). To run it, place an export at
data/reference/reference_export.csv with these columns (rename as needed in
COLMAP):
    doi, compound, property, value, unit
The property names must map to Hc / Br / Ms / Tc (see PROPMAP).

Output: data/processed/crosscheck.csv and crosscheck_summary.txt
"""
import csv
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from units import to_si  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
REF = ROOT / "data" / "reference" / "reference_export.csv"
P = ROOT / "data" / "processed"
COLMAP = {"doi": "doi", "compound": "compound", "property": "property", "value": "value", "unit": "unit"}
PROPMAP = {"coercivity": "Hc", "remanence": "Br", "magnetization": "Ms", "saturation magnetization": "Ms",
           "curie": "Tc", "curie temperature": "Tc", "tc": "Tc", "hc": "Hc", "br": "Br", "ms": "Ms"}
TOL = 0.02  # relative agreement tolerance after unit conversion


def family(prop):
    return "Hc" if prop.startswith("Hc") else ("Br" if prop in ("Br", "Mr") else prop)


def ndoi(d):
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (d or "").strip().lower())


def main():
    if not REF.exists():
        msg = ("Cross-check not run: no reference export at data/reference/reference_export.csv.\n"
               "The cross-check is planned for a later version; it is not part of v0.1.\n")
        (P / "crosscheck_summary.txt").write_text(msg, encoding="utf-8")
        print(msg)
        return
    ours = list(csv.DictReader((P / "opensmfe.csv").open(encoding="utf-8")))
    ref = list(csv.DictReader(REF.open(encoding="utf-8")))
    idx = {}
    for r in ref:
        prop = PROPMAP.get(r[COLMAP["property"]].strip().lower())
        if prop:
            idx.setdefault((ndoi(r[COLMAP["doi"]]), prop), []).append(r)
    rows, tally = [], {"agree": 0, "disagree": 0, "not_in_reference": 0, "unit_unparsed": 0}
    for o in ours:
        fam = family(o["property"])
        cands = idx.get((ndoi(o["doi"]), fam), [])
        if not cands:
            tally["not_in_reference"] += 1
            rows.append({**o, "ref_value": "", "ref_unit": "", "outcome": "not_in_reference"})
            continue
        best, outcome = None, "disagree"
        for c in cands:
            try:
                v, u, _ = to_si(o["property"] if fam != "Br" else o["property"], c[COLMAP["value"]], c[COLMAP["unit"]])
            except ValueError:
                outcome = "unit_unparsed"
                continue
            ours_v = float(o["value_si"])
            if u == o["unit_si"] and abs(v - ours_v) <= TOL * max(abs(ours_v), 1e-9):
                best, outcome = c, "agree"
                break
            best = c
        tally[outcome] += 1
        rows.append({**o, "ref_value": best[COLMAP["value"]] if best else "",
                     "ref_unit": best[COLMAP["unit"]] if best else "", "outcome": outcome})
    cols = ["meas_id", "doi", "property", "value_as_published", "unit_as_published", "ref_value", "ref_unit", "outcome"]
    with (P / "crosscheck.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    s = "Cross-check summary\n" + "\n".join(f"{k}: {v}" for k, v in tally.items()) + "\n"
    (P / "crosscheck_summary.txt").write_text(s, encoding="utf-8")
    print(s)


if __name__ == "__main__":
    main()
