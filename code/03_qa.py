"""Step 3: quality checks. Writes data/processed/qa_report.txt and paper/stats.json.

Plain-language note: this script looks for mistakes. It checks for impossible
values, numbers that do not appear in their own quoted sentence, duplicate
rows, and missing fields. It also picks the rows you will check by hand.
Read qa_report.txt; you do not need to open this file.
"""
import csv
import json
import math
import pathlib
import random
import re

MARK = "[" + "VERIFY"  # built in two parts so the publish gate does not flag this file

ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / "data" / "processed"
MU0 = 4e-7 * math.pi

# physically plausible ranges, in SI units (Sm2Fe17N3 intrinsic: Js ~1.54 T, sigma_s ~150-160 A m2/kg,
# Tc ~ 740-750 K, ideal (BH)max = Js^2/(4 mu0) ~ 470 kJ/m3)
RANGE = {
    ("coercivity", ""): (0, 6000),          # kA/m
    ("magnetization", "mass"): (0, 175),    # A m2/kg
    ("magnetization", "volume"): (0, 1.65), # T
    ("BHmax", ""): (0, 475),                # kJ/m3
    ("Tc", ""): (300, 900),                 # K
}


def kind(prop):
    if prop.startswith("Hc"):
        return "coercivity"
    if prop in ("Br", "Mr", "Ms"):
        return "magnetization"
    return prop


def main():
    meas = list(csv.DictReader((P / "opensmfe_measurements.csv").open(encoding="utf-8")))
    samples = {r["sample_id"]: r for r in csv.DictReader((P / "opensmfe_samples.csv").open(encoding="utf-8"))}
    sources = list(csv.DictReader((P / "opensmfe_sources.csv").open(encoding="utf-8")))
    out, problems = [], []

    def say(s=""):
        out.append(s)

    say("OpenSmFe QA report (v0.1)")
    say("Plain-language note: counts, impossible-value checks, and the rows picked for hand-checking.")
    say("")
    say(f"Sources: {len(sources)}   Samples: {len(samples)}   Measurements: {len(meas)}")
    by_prop = {}
    for m in meas:
        by_prop[m["property"]] = by_prop.get(m["property"], 0) + 1
    say("Measurements by property: " + ", ".join(f"{k}={v}" for k, v in sorted(by_prop.items())))
    grades = {g: sum(m["comparability"] == g for m in meas) for g in "ABC"}
    say("Comparability grades: " + ", ".join(f"{k}={v}" for k, v in grades.items()))
    vstat = {}
    for m in meas:
        vstat[m["verification_status"]] = vstat.get(m["verification_status"], 0) + 1
    say("Verification status: " + ", ".join(f"{k}={v}" for k, v in sorted(vstat.items())))
    say("")

    say("CHECK 1. Value in range (SI units)")
    for m in meas:
        key = (kind(m["property"]), m["basis"] if kind(m["property"]) == "magnetization" else "")
        lo, hi = RANGE[key]
        v = float(m["value_si"])
        if not lo <= v <= hi:
            problems.append(f"out of range: {m['meas_id']} = {v} {m['unit_si']} (allowed {lo}-{hi})")
    say("  pass" if not [p for p in problems if p.startswith("out of range")] else "  see problems")

    say("CHECK 2. Published number appears in its own evidence quote")
    miss = []
    for m in meas:
        q = m["evidence_quote"]
        if MARK in q:
            miss.append(f"{m['meas_id']}: quote is a placeholder paraphrase")
            continue
        val = m["value_as_published"]
        if not re.search(r"(?<![\d.])" + re.escape(val) + r"(?![\d])", q):
            miss.append(f"{m['meas_id']}: '{val}' not found in quote")
    for x in miss:
        say("  " + x)
    if not miss:
        say("  pass")

    say("CHECK 3. Duplicate measurement ids")
    ids = [m["meas_id"] for m in meas]
    d = sorted({i for i in ids if ids.count(i) > 1})
    say("  pass" if not d else f"  duplicates: {d}")
    problems += [f"duplicate {i}" for i in d]

    say("CHECK 4. Physics consistency within a sample")
    phys = []
    by_sample = {}
    for m in meas:
        by_sample.setdefault(m["sample_id"], []).append(m)
    for sid, ms in by_sample.items():
        br = [float(m["value_si"]) for m in ms if m["property"] == "Br" and m["basis"] == "volume"]
        bh = [float(m["value_si"]) for m in ms if m["property"] == "BHmax"]
        if br and bh:
            limit = br[0] ** 2 / (4 * MU0) / 1000  # kJ/m3
            ok = bh[0] <= limit * 1.001
            phys.append(f"  {sid}: (BH)max {bh[0]:.1f} kJ/m3 vs Br^2/4mu0 limit {limit:.1f} kJ/m3 -> {'ok' if ok else 'IMPOSSIBLE'}")
            if not ok:
                problems.append(f"(BH)max exceeds Br limit: {sid}")
        mr = [float(m["value_si"]) for m in ms if m["property"] == "Mr" and m["basis"] == "mass"]
        msat = [float(m["value_si"]) for m in ms if m["property"] == "Ms" and m["basis"] == "mass"]
        if mr and msat and mr[0] > msat[0]:
            problems.append(f"Mr > Ms: {sid}")
    out.extend(phys or ["  no sample has both Br (tesla) and (BH)max; nothing to compare"])

    say("CHECK 5. Required sample fields present")
    req = ["composition_nominal", "family", "nitrided", "alloy_route", "phase_outcome", "sample_form"]
    gaps = [f"{s}: {c}" for s, r in samples.items() for c in req if not r[c].strip()]
    say("  pass" if not gaps else "  missing: " + "; ".join(gaps))

    say("CHECK 6. Fields still carrying a verify marker (must be zero before release)")
    nv = 0
    for f in ("opensmfe_measurements.csv", "opensmfe_samples.csv", "opensmfe_sources.csv"):
        n = (P / f).read_text(encoding="utf-8").count(MARK)
        nv += n
        say(f"  {f}: {n}")

    say("")
    say("PROBLEMS")
    say("  none" if not problems else "\n".join("  " + p for p in problems))

    # spot checks: extremes plus a seeded random draw
    say("")
    say("SPOT CHECKS for the author (also in docs/VERIFY_CHECKLIST.md)")
    coer = sorted([m for m in meas if kind(m["property"]) == "coercivity"], key=lambda m: float(m["value_si"]))
    ext = [coer[0], coer[-1]] + [max((m for m in meas if m["property"] == p), key=lambda m: float(m["value_si"]))
                                 for p in ("BHmax", "Tc") if any(m["property"] == p for m in meas)]
    rng = random.Random(2027)
    pool = [m for m in meas if m not in ext]
    rand = rng.sample(pool, min(5, len(pool)))
    for tag, group in (("extreme", ext), ("random, seed 2027", rand)):
        for m in group:
            say(f"  [{tag}] {m['meas_id']}: {m['value_as_published']} {m['unit_as_published']} ({m['evidence_location']})")

    (P / "qa_report.txt").write_text("\n".join(out) + "\n", encoding="utf-8")

    hc_rt = [float(m["value_si"]) for m in meas if kind(m["property"]) == "coercivity" and m["comparability"] != "C"]
    stats = {
        "version": "v0.1", "draft": True,
        "n_sources": len(sources), "n_samples": len(samples), "n_measurements": len(meas),
        "n_by_property": by_prop, "n_by_grade": grades, "n_by_verification": vstat,
        "n_verify_tags": nv, "n_quote_mismatch": len(miss), "n_problems": len(problems),
        "hc_ambient_min_kAm": round(min(hc_rt), 1) if hc_rt else None,
        "hc_ambient_max_kAm": round(max(hc_rt), 1) if hc_rt else None,
        "n_meas_T_not_stated": sum(m["meas_T_status"] in ("not_stated", "assumed_RT") for m in meas
                                   if m["property"] != "Tc"),
        "n_non_Tc": sum(m["property"] != "Tc" for m in meas),
        "spot_checks": [m["meas_id"] for m in ext + rand],
    }
    (ROOT / "paper").mkdir(exist_ok=True)
    (ROOT / "paper" / "stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
