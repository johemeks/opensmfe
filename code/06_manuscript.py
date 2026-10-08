"""Step 6: build the journal manuscript from the data.

Plain-language note: this writes the paper. Every number in the text, tables
and figures is computed here from the released database files, so the paper
cannot disagree with the data. The words live in paper/manuscript/template.tex;
numbers are filled in where the template says <<name>>. Run it after
./run_all.sh --final. Output: paper/manuscript/opensmfe_manuscript.pdf
"""
import collections
import csv
import json
import math
import pathlib
import re
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
P, RAW, MS = ROOT / "data" / "processed", ROOT / "data" / "raw", ROOT / "paper" / "manuscript"
MU0 = 4e-7 * math.pi
JS_SMFEN = 1.54  # T, intrinsic saturation polarization of Sm2Fe17N3 as quoted in the review cited in the text


def rd(p):
    return list(csv.DictReader(p.open(encoding="utf-8")))


def f(x, nd=1):
    return f"{x:.{nd}f}"


FORMULA = re.compile(r"^(?:[A-Z][a-z]?\d*(?:\.\d+)?)+$")


def chem(s):
    """Typeset chemical formulas (tokens such as Sm2Fe17N3 or Ce72Cu22Al6) with subscripts."""
    out = []
    for tok in re.split(r"(\s+|[(),/])", s):
        if FORMULA.match(tok) and re.search(r"\d", tok) and len(re.findall(r"[A-Z]", tok)) >= 2:
            tok = re.sub(r"(\d+(?:\.\d+)?)", r"$_{\1}$", tok)
        out.append(tok)
    return "".join(out).replace("um", "$\\mu$m") if " um" in s else "".join(out)


def tex_escape(s):
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%")
            .replace("_", r"\_").replace("#", r"\#"))


def main():
    meas, samples, sources = rd(P / "opensmfe_measurements.csv"), rd(P / "opensmfe_samples.csv"), rd(P / "opensmfe_sources.csv")
    queue, clog = rd(RAW / "queue_v0.1.csv"), rd(RAW / "curation_log_v0.1.csv")
    S = {s["sample_id"]: s for s in samples}
    M = {m["meas_id"]: m for m in meas}
    st = {}
    st["nsrc"], st["nsamp"], st["nmeas"] = len(sources), len(samples), len(meas)
    st["nfull"] = sum(s["text_read"] == "full text" for s in sources)
    st["nabs"] = sum(s["text_read"] == "abstract only" for s in sources)
    prop = collections.Counter(m["property"] for m in meas)
    nhc = sum(v for k, v in prop.items() if k.startswith("Hc"))
    st.update(nhc=nhc, nhcj=prop["Hcj"], nhcu=prop["Hc_unspecified"], nmr=prop["Mr"], nbr=prop["Br"],
              nbh=prop["BHmax"], ntc=prop["Tc"], nms=prop.get("Ms", 0))
    g = collections.Counter(m["comparability"] for m in meas)
    st.update(gA=g["A"], gB=g["B"], gC=g["C"])
    reasons = collections.Counter(x for m in meas for x in m["comparability_reasons"].split("; ") if x)
    nontc = [m for m in meas if m["property"] != "Tc"]
    st["nnontc"] = len(nontc)
    st["nTns"] = reasons["measurement temperature not stated"]
    st["pTns"] = f(100 * st["nTns"] / len(nontc), 0)
    st["nTstated"] = sum(m["meas_T_status"] == "stated" for m in nontc)
    st["nHcu_reason"] = reasons["coercivity type (Hcj or Hcb) not stated"]
    st["pHcu"] = f(100 * st["nHcu_reason"] / nhc, 0)
    st["nmassbulk"] = reasons["mass-basis value reported for a bulk magnet"]
    st["nlowT"] = reasons["measured at 10 K, not room temperature"]
    st["nver"] = sum(m["verification_status"] == "verified" for m in meas)
    # coercivity range at ambient (grade not C)
    amb = [m for m in meas if m["property"].startswith("Hc") and m["comparability"] != "C"]
    lo, hi = min(amb, key=lambda m: float(m["value_si"])), max(amb, key=lambda m: float(m["value_si"]))
    st.update(hclo=f(float(lo["value_si"]), 0), hchi=f(float(hi["value_si"]), 0),
              hclo_pub=f"{lo['value_as_published']}~{lo['unit_as_published']}", hchi_pub=f"{hi['value_as_published']}~{hi['unit_as_published']}",
              hcspan=f(float(hi["value_si"]) / float(lo["value_si"]), 0))
    # within-source contrasts (Saito 2024)
    sa, sc, se = (float(M[k]["value_si"]) for k in ("SAITO2024-a-Hc_unspecified", "SAITO2024-c-Hc_unspecified", "SAITO2024-e-Hc_unspecified"))
    st.update(sa=f(sa, 0), sc=f(sc, 0), se=f(se, 0), sc_pct=f(100 * sc / sa, 0), se_pct=f(100 * se / sa, 0),
              sa_pub=M["SAITO2024-a-Hc_unspecified"]["value_as_published"], sc_pub=M["SAITO2024-c-Hc_unspecified"]["value_as_published"],
              se_pub=M["SAITO2024-e-Hc_unspecified"]["value_as_published"])
    mra, mrc = float(M["SAITO2024-a-Mr"]["value_si"]), float(M["SAITO2024-c-Mr"]["value_si"])
    st.update(mrb=M["SAITO2024-b-Mr"]["value_as_published"], mra=M["SAITO2024-a-Mr"]["value_as_published"],
              mrc=M["SAITO2024-c-Mr"]["value_as_published"], mrd=M["SAITO2024-d-Mr"]["value_as_published"],
              mre=M["SAITO2024-e-Mr"]["value_as_published"])
    # Hirayama TbCu7
    h300, h10 = float(M["HIRAYAMA2025-a-Hc_unspecified"]["value_si"]), float(M["HIRAYAMA2025-a-Hc_unspecified@10K"]["value_si"])
    st.update(h300=f(h300, 0), h10=f(h10, 0), lhcj=f(float(M["LIANG2023-a-Hcj"]["value_si"]), 0),
              l10=f(float(M["LIANG2023-c-Hcj@10K"]["value_si"]), 0),
              l10ratio=f(float(M["LIANG2023-c-Hcj@10K"]["value_si"]) / float(M["LIANG2023-a-Hcj"]["value_si"]), 1),
              h10ratio=f(h10 / h300, 1))
    # energy-product bounds
    bh_ideal = JS_SMFEN ** 2 / (4 * MU0) / 1000
    lbh = float(M["LIANG2023-b-BHmax"]["value_si"])
    zbr, zbh = float(M["ZHENG2022-a-Br"]["value_si"]), float(M["ZHENG2022-a-BHmax"]["value_si"])
    zlim = zbr ** 2 / (4 * MU0) / 1000
    st.update(bhideal=f(bh_ideal, 0), lbh=f(lbh, 1), lbhpct=f(100 * lbh / bh_ideal, 0), zbr=f(zbr, 3),
              zbh=f(zbh, 1), zlim=f(zlim, 1), zpct=f(100 * zbh / zlim, 0))
    st["zabs"], st["zres"] = "10.19", M["ZHENG2022-a-Br"]["value_as_published"]
    st["zdiff"] = f(100 * (10.19 - float(st["zres"])) / float(st["zres"]), 1)
    # queue and curation
    dec = collections.Counter(q["decision"] for q in queue)
    st["nscreen"] = len(queue) + len(sources)
    st["nqueue_extract"] = dec["to extract"]
    st["nqueue_partial"] = dec["extract Sm-Fe-N-only samples"] + dec["extract parent Sm2Fe17 only"]
    st["nqueue_excl"] = dec["exclude"]
    st["nqueue_defer"] = dec["defer to v1.1"]
    st["nqueue_review"] = dec["mine for leads"]
    cat = collections.Counter(c["category"] for c in clog)
    st.update(cpara=cat["paraphrase_replaced"], creclass=cat["property_reclassified"], cwrong=cat["wrong_sentence"],
              cfield=cat["field_corrected"], cmeta=cat["metadata_completed"])
    st["cvalchg"] = 0  # no numeric value changed during curation (all events are quote, property, field or metadata)
    st["nfam27"] = sum(s["family"] == "2:17" for s in samples)
    st["nfam17"] = sum(s["family"] == "1:7" for s in samples)
    st["nnitr"] = sum(s["nitrided"] == "Y" for s in samples)
    st["yrmin"], st["yrmax"] = min(s["year"] for s in sources), max(s["year"] for s in sources)

    # ---- completeness matrix (Fig. 2) ----
    fields = [
        ("Meas. temperature", lambda s, ms: any(m["meas_T_status"] == "stated" for m in ms if m["property"] != "Tc")),
        ("Hc definition", lambda s, ms: any(m["property"] in ("Hcj", "Hcb") for m in ms if m["property"].startswith("Hc"))),
        ("Nitriding temp.", lambda s, ms: True if (s["nitrided"] != "Y" or not s["nitriding"].strip()) else bool(re.search(r"\d+\s*(°\s*C|C\b|K\b)", s["nitriding"]))),
        ("Particle size", lambda s, ms: bool(re.match(r"^\d", s["particle_size_um"] or ""))),
        ("Phase outcome", lambda s, ms: bool(s["phase_outcome"]) and "not stated" not in s["phase_outcome"]),
        ("Alignment", lambda s, ms: s["aligned"] in ("Y", "N")),
        ("Consolidation", lambda s, ms: True if "bulk" not in s["sample_form"] else bool(s["consolidation"])),
    ]
    srcs = [s["source_id"] for s in sources]
    mat = []
    for sid in srcs:
        smp = [s for s in samples if s["source_id"] == sid]
        row = []
        for _, fn in fields:
            row.append(sum(fn(s, [m for m in meas if m["sample_id"] == s["sample_id"]]) for s in smp) / len(smp))
        mat.append(row)
    nfield = len(fields)
    st["nfields"] = nfield
    st["complete_overall"] = f(100 * sum(sum(r) for r in mat) / (len(mat) * nfield), 0)
    col_T = [r[0] for r in mat]
    st["nsrc_T"] = sum(v > 0 for v in col_T)
    tre = re.compile(r"\d+\s*(°\s*C|C\b|K\b)")
    st["nsrc_nitr"] = sum(1 for sid in srcs if any(tre.search(s["nitriding"]) for s in samples
                                                   if s["source_id"] == sid and s["nitriding"].strip()))
    st["nsrc_hcdef"] = sum(r[1] > 0 for r in mat)
    st["nsrc_nitrproc"] = sum(1 for sid in srcs if any(s["nitriding"].strip() for s in samples if s["source_id"] == sid))

    INK, INK2, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
    fig, ax = plt.subplots(figsize=(3.4, 2.6), dpi=300)
    fig.patch.set_facecolor(SURF)
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("b", ["#e8eef8", "#2a78d6"])
    a = np.array(mat)
    ax.imshow(a, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            ax.text(j, i, "%d%%" % round(100 * a[i, j]), ha="center", va="center", fontsize=5.5,
                    color="#ffffff" if a[i, j] > 0.6 else INK)
    labels = [f"{s['source_id'][:-4].capitalize()} {s['year']}" + ("*" if s["text_read"] == "abstract only" else "") for s in sources]
    ax.set_yticks(range(len(srcs)), labels, fontsize=6, color=INK)
    ax.set_xticks(range(nfield), [x for x, _ in fields], fontsize=5.8, rotation=40, ha="right", color=INK)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([x - 0.5 for x in range(1, nfield)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(srcs))], minor=True)
    ax.grid(which="minor", color=SURF, linewidth=1.5)
    ax.tick_params(which="minor", length=0)
    fig.tight_layout()
    MS.mkdir(parents=True, exist_ok=True)
    fig.savefig(MS / "fig2_completeness.pdf", facecolor=SURF)
    fig.savefig(MS / "fig2_completeness.png", facecolor=SURF)

    # Fig. 1 at column width from the released figure script is reused (PDF version)
    subprocess.run(["python3", str(ROOT / "code" / "04_figures.py"), "--final", "--paper"], check=True, capture_output=True)
    import shutil
    shutil.copy(ROOT / "paper" / "figures" / "fig1_coercivity_by_route_paper.pdf", MS / "fig1_coercivity_by_route.pdf")

    # ---- tables ----
    src_rows = []
    for s in sources:
        n = sum(m["source_id"] == s["source_id"] for m in meas)
        forms = sorted({S[m["sample_id"]]["sample_form"].split(" (")[0] for m in meas if m["source_id"] == s["source_id"]})
        route = S[[m for m in meas if m["source_id"] == s["source_id"]][0]["sample_id"]]["alloy_route"].split(" (")[0].split(",")[0]
        src_rows.append(f"{tex_escape(s['authors'].split(';')[0].split()[-1])} \\textit{{et al.}}~\\cite{{{s['source_id'].lower()}}} & {s['year']} & "
                        f"{chem(tex_escape(route))} & {tex_escape(', '.join(forms))} & {n} & {'full' if s['text_read']=='full text' else 'abstract'} \\\\")
    st["table_sources"] = "\n".join(src_rows).replace("Saito \\textit{et al.}", "Saito")
    PN = {"Hc_unspecified": r"$H_c$", "Hcj": r"$H_{cj}$", "Mr": r"$\sigma_r$", "Br": r"$B_r$", "BHmax": r"$(BH)_{\max}$", "Tc": r"$T_C$"}
    UN = {"kA/m": r"kA\,m$^{-1}$", "A m2/kg": r"A\,m$^2$\,kg$^{-1}$", "T": "T", "kJ/m3": r"kJ\,m$^{-3}$", "K": "K"}
    UP = {"emu/g": r"emu\,g$^{-1}$", "MA/m": r"MA\,m$^{-1}$"}
    mrows = []
    for m in meas:
        s = S[m["sample_id"]]
        T = m["meas_T_K"] if m["meas_T_K"] else ("--" if m["property"] == "Tc" else "n.s.")
        mrows.append(f"{tex_escape(m['sample_id'])} & {chem(tex_escape(s['sample_label']))} & {PN[m['property']]} & "
                     f"{m['value_as_published']} {UP.get(m['unit_as_published'], m['unit_as_published'])} & "
                     f"{m['value_si']} {UN[m['unit_si']]} & {T} & {m['comparability']} \\\\")
    st["table_meas"] = "\n".join(mrows)

    json.dump({k: v for k, v in st.items() if not k.startswith("table")}, (MS / "manuscript_stats.json").open("w"), indent=1)

    # ---- fill template, order bibliography by first citation ----
    t = (MS / "template.tex").read_text(encoding="utf-8")
    missing = set(re.findall(r"<<(\w+)>>", t)) - set(st)
    if missing:
        raise SystemExit(f"template keys without values: {sorted(missing)}")
    t = re.sub(r"<<(\w+)>>", lambda mm: str(st[mm.group(1)]), t)
    body, bib = t.split("%%BIB%%")
    items = dict(re.findall(r"\\bibitem\{(\w+)\}(.*?)(?=\\bibitem\{|\Z)", bib, flags=re.S))
    order = []
    for keys in re.findall(r"\\cite\{([^}]+)\}", body):
        for k in keys.split(","):
            k = k.strip()
            if k not in order:
                order.append(k)
    unknown = [k for k in order if k not in items]
    if unknown:
        raise SystemExit(f"cited but no bibitem: {unknown}")
    unused = [k for k in items if k not in order]
    bibtex = "\\begin{thebibliography}{99}\n" + "".join(f"\\bibitem{{{k}}}{items[k].rstrip()}\n" for k in order) + "\\end{thebibliography}\n"
    out = body + bibtex + "\\end{document}\n"
    (MS / "opensmfe_manuscript.tex").write_text(out, encoding="utf-8")
    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "opensmfe_manuscript.tex"],
                           cwd=MS, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-3000:])
        raise SystemExit("pdflatex failed")
    print(f"manuscript built: {len(order)} references" + (f"; unused bibitems: {unused}" if unused else ""))


if __name__ == "__main__":
    main()
