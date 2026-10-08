# OpenSmFe build spec

*Plain-language note: this is the one-page plan the whole build follows. Each line says what is being built and how. You only need to read the "In plain terms" column; the right-hand side is for the build.*

| Field | In plain terms | Spec |
|---|---|---|
| PROJECT | An open database plus the paper that describes it | OpenSmFe. Archetypes: (1) open dataset, plus (8)/(9) a data-descriptor paper. Flagship 1. |
| QUESTION | For Sm-Fe(-N) magnets, which recipe and processing steps give which magnet performance, and how far can the published numbers be compared? | Harmonized composition, process, structure and property records, with a per-row comparability grade. |
| SOURCES | Free-to-read research papers, plus one robot-built database to check against | (a) Open-access primary literature (CC BY or equivalent; DOI, license and access date recorded per source). (b) Cross-check against a text-mined database: deferred to a later version by the author (2026-10-08). Candidates: NEMAD (Itani, Zhang, Zang, Nat. Commun. 2025, doi:10.1038/s41467-025-64458-z); Court and Cole 2018 (Sci. Data 5:180111). |
| UNIT | One row is one measured property of one sample in one paper | `measurements.csv`: (source, sample, property, temperature). `samples.csv`: one row per distinct sample. |
| MEASURES | The five properties, each kept exactly as published and also converted to standard units | Hcj, Hcb (kA/m); Br, Mr (T or A·m²/kg, basis kept); Ms (same); (BH)max (kJ/m³); Tc (K). Conversions in `code/units.py`. Mass-basis values are **not** converted to volume basis (needs a density). |
| COMPARABILITY | A grade on every row | A = room temperature (290 to 305 K, or stated as RT), sample form stated, coercivity type known, convertible unit. B = one soft gap (RT implied, Hc type unstated, or form ambiguous). C = non-ambient temperature, or a key field missing. Reasons listed per row. |
| OUTPUTS | The files you will publish | `data/processed/opensmfe_measurements.csv`, `opensmfe_samples.csv`, `opensmfe_sources.csv`, flat `opensmfe.csv`, `qa_report.txt`, `stats.json`, figures in `paper/figures/`. Later versions: cross-check report, data paper. |
| VENUES | Where it goes, in order | GitHub, then Zenodo (DOI, v1.0), then an arXiv preprint (cond-mat.mtrl-sci), then a data journal. |
| AUTHOR CHECKS | Things only you can decide | Every value against its quote and source (status column). The comparability rules. Scope (1:12 family). Whether to digitize values from figures (v0.1: no). All settled for v0.1; see DECISIONS.md. |
| LICENSE | Who may reuse it | Data CC BY 4.0. Code MIT. Evidence quotes kept short (≤125 characters) for fair-use attribution. |
| ASSUMPTIONS | Going ahead without confirmation | Scope defaults (2:17 and 1:7 families, nitrided or not). Hcj is the headline coercivity. v0.1 uses text and table values only, with no figure digitizing. |

## How values enter the database

1. Find a paper and confirm it is open access, recording its license.
2. Extract every numeric value for the five properties, together with the exact short quote and its location (abstract, section, table or figure caption).
3. Enter it with `verification_status = unverified`.
4. Joshua opens the source, confirms the value, unit, sample and temperature, and sets the status to `verified` (or `corrected`/`rejected`, with a note).
5. Only `verified` and `corrected` rows enter release statistics. Draft statistics are labeled as including unverified rows.
