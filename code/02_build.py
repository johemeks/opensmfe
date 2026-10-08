"""Step 2: harmonize units, grade comparability, apply the author's verification.

Plain-language note: this turns the raw extraction table into the published
database files. It converts units, gives every row an A/B/C comparability grade
with written reasons, and applies your verification decisions from
data/verification/verification_log.csv. You do not need to open this file; the
grading rules are listed in docs/CODEBOOK.md, and you rule on them during
verification.

Outputs (data/processed/):
  opensmfe_sources.csv       one row per paper
  opensmfe_samples.csv       one row per sample (composition, processing, phase, form)
  opensmfe_measurements.csv  one row per measured value
  opensmfe.csv               flat join of the three, for spreadsheet users
"""
import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from units import to_si, parse_temperature_K, COERCIVITY, MAGNETIZATION  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
VER = ROOT / "data" / "verification"
VERSION = "v0.1"
RT = (290.0, 305.0)

SAMPLE_COLS = ["sample_id", "source_id", "sample_label", "composition_nominal", "family", "nitrided",
               "alloy_route", "milling", "melt_spinning", "anneal", "nitriding", "consolidation",
               "phase_outcome", "sample_form", "aligned", "particle_size_um"]
MEAS_COLS = ["meas_id", "sample_id", "source_id", "property", "value_as_published", "unit_as_published",
             "value_si", "unit_si", "basis", "meas_T_K", "meas_T_status", "method",
             "evidence_quote", "evidence_location", "extraction_note",
             "comparability", "comparability_reasons",
             "verification_status", "verified_by", "verified_on", "verification_note"]


def read(p):
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(p, rows, cols):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def meas_id(r, T):
    tag = f"@{int(round(T))}K" if T is not None and not (RT[0] <= T <= RT[1]) else ""
    return f"{r['sample_id']}-{r['property']}{tag}"


def grade(r, sample):
    """Return (grade, reasons). C beats B beats A."""
    hard, soft = [], []
    prop = r["property"]
    note = (r.get("extraction_note") or "").lower()
    method = (r.get("method") or "").lower()
    form = sample.get("sample_form", "")
    if prop == "Tc":
        if "verify" in method or "literature" in note:
            soft.append("Tc may be quoted from literature rather than measured on this sample")
        if "approximate" in note:
            soft.append("Tc given as approximate")
    else:
        T, status = r["_T"], r["_Tstatus"]
        if status == "stated" and not (RT[0] <= T <= RT[1]):
            hard.append(f"measured at {T:g} K, not room temperature")
        elif status == "assumed_RT":
            soft.append("room temperature implied but not confirmed")
        elif status == "not_stated":
            soft.append("measurement temperature not stated")
        if prop == "Hc_unspecified":
            soft.append("coercivity type (Hcj or Hcb) not stated")
        if prop in MAGNETIZATION and r["_basis"] == "mass" and "bulk" in form:
            soft.append("mass-basis value reported for a bulk magnet")
        if prop == "BHmax" and "powder" in form and "resin" not in form:
            soft.append("(BH)max of a powder depends on an assumed packing density")
    if not form or "verify" in form.lower():
        soft.append("sample form not confirmed")
    if "inconsistency" in note:
        soft.append("paper reports this value inconsistently")
    g = "C" if hard else ("B" if soft else "A")
    return g, "; ".join(hard + soft)


def main():
    sources = read(RAW / f"sources_{VERSION}.csv")
    ext = read(RAW / f"extractions_{VERSION}.csv")
    vlog_path = VER / "verification_log.csv"
    vlog = {r["meas_id"]: r for r in read(vlog_path)} if vlog_path.exists() else {}

    samples, meas = {}, []
    for r in ext:
        samples.setdefault(r["sample_id"], {c: r[c] for c in SAMPLE_COLS})
        T, Ts = parse_temperature_K(r["meas_T_raw"])
        mid = meas_id(r, T)  # id is fixed by the extraction, before any correction
        v = vlog.get(mid, {})
        status = (v.get("status") or "unverified").strip().lower()
        # details the author confirmed from the paper's methods section re-grade the row
        if v.get("confirmed_meas_T"):
            T, Ts = parse_temperature_K(v["confirmed_meas_T"])
        if v.get("confirmed_property"):
            r = dict(r, property=v["confirmed_property"].strip())
        v_si, u_si, basis = to_si(r["property"], r["value_as_published"], r["unit_as_published"])
        r = dict(r, _T=T, _Tstatus=Ts, _basis=basis)
        g, why = grade(r, samples[r["sample_id"]])
        row = {
            "meas_id": mid, "sample_id": r["sample_id"], "source_id": r["source_id"],
            "property": r["property"], "value_as_published": r["value_as_published"],
            "unit_as_published": r["unit_as_published"],
            "value_si": f"{v_si:.4g}", "unit_si": u_si, "basis": basis,
            "meas_T_K": "" if T is None else f"{T:g}", "meas_T_status": Ts,
            "method": r["method"], "evidence_quote": r["evidence_quote"],
            "evidence_location": r["evidence_location"], "extraction_note": r["extraction_note"],
            "comparability": g, "comparability_reasons": why,
            "verification_status": status, "verified_by": v.get("verified_by", ""),
            "verified_on": v.get("verified_on", ""), "verification_note": v.get("note", ""),
        }
        if status == "corrected":
            # the author's corrected value replaces the extracted one; the original stays in the note
            cv, cu = v.get("corrected_value", ""), v.get("corrected_unit", "") or r["unit_as_published"]
            row["verification_note"] = (f"extracted {r['value_as_published']} {r['unit_as_published']}; "
                                        + row["verification_note"]).strip("; ")
            row["value_as_published"], row["unit_as_published"] = cv, cu
            v_si, u_si, basis = to_si(r["property"], cv, cu)
            row["value_si"], row["unit_si"], row["basis"] = f"{v_si:.4g}", u_si, basis
        meas.append(row)

    ids = [m["meas_id"] for m in meas]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        sys.exit(f"duplicate meas_id: {sorted(dup)}")

    write(OUT / "opensmfe_sources.csv", sources, list(sources[0].keys()))
    write(OUT / "opensmfe_samples.csv", list(samples.values()), SAMPLE_COLS)
    write(OUT / "opensmfe_measurements.csv", meas, MEAS_COLS)
    src = {s["source_id"]: s for s in sources}
    flat = [{**samples[m["sample_id"]], **m, "doi": src[m["source_id"]]["doi"],
             "year": src[m["source_id"]]["year"], "source_license": src[m["source_id"]]["license"]}
            for m in meas]
    write(OUT / "opensmfe.csv", flat, MEAS_COLS[:1] + ["doi", "year"] + SAMPLE_COLS[1:]
          + MEAS_COLS[3:] + ["source_license"])

    # verification worksheet: one line per value, pre-filled, for the author
    VER.mkdir(parents=True, exist_ok=True)
    sheet = VER / "verification_log.csv"
    if not sheet.exists():
        write(sheet, [{"meas_id": m["meas_id"], "doi": src[m["source_id"]]["doi"],
                       "what_to_check": f"{m['property']} = {m['value_as_published']} {m['unit_as_published']}"
                                        f" | {samples[m['sample_id']]['sample_label']} | at {m['evidence_location']}",
                       "status": "", "corrected_value": "", "corrected_unit": "",
                       "confirmed_meas_T": "", "confirmed_property": "", "verified_by": "", "verified_on": "", "note": ""} for m in meas],
              ["meas_id", "doi", "what_to_check", "status", "corrected_value", "corrected_unit",
               "confirmed_meas_T", "confirmed_property", "verified_by", "verified_on", "note"])
    print(f"{len(sources)} sources, {len(samples)} samples, {len(meas)} measurements")


if __name__ == "__main__":
    main()
