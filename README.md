# OpenSmFe

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23248499.svg)](https://doi.org/10.5281/zenodo.23248499)

**Status: v0.1.0 seed release, 2026-10-08.** Archived on Zenodo: [10.5281/zenodo.23248499](https://doi.org/10.5281/zenodo.23248499) (all versions); v0.1.0 specifically: [10.5281/zenodo.23248500](https://doi.org/10.5281/zenodo.23248500). Every value has been verified by the author against its source paper. This release is a seed batch that demonstrates the schema and method; the planned v1.0 will cover the wider open-access literature.

## What this is, in plain language

OpenSmFe is a free, public table of published measurements on samarium-iron-nitride (Sm-Fe-N) permanent magnets. Sm-Fe-N is a leading alternative to the neodymium magnets used in electric-vehicle motors and wind turbines.

Each row records four things:

- what the magnet was made of
- how it was made (milling, melt spinning, annealing, nitriding, sintering)
- which crystal phases resulted
- what was measured, and at what temperature: coercivity, remanence, saturation magnetization, maximum energy product, Curie temperature

Every number links to the exact sentence of the open-access paper it came from. Every row carries an **A/B/C comparability grade**, so a reader knows whether two numbers can fairly be compared.

The project is built openly so that U.S. research groups and magnet makers can reuse the composition, processing and property maps without asking.

*New to this project? Read [docs/START_HERE.md](docs/START_HERE.md) first. Terms are defined in [docs/GLOSSARY.md](docs/GLOSSARY.md).*

## Files

| File | What it holds |
|---|---|
| `data/processed/opensmfe.csv` | Everything in one flat table (easiest for Excel) |
| `data/processed/opensmfe_measurements.csv` | One row per published value: original and SI units, temperature, evidence quote, grade, verification status |
| `data/processed/opensmfe_samples.csv` | One row per sample: composition, processing route, phase outcome, sample form |
| `data/processed/opensmfe_sources.csv` | One row per paper: DOI, license, access date |
| `data/processed/qa_report.txt` | Quality checks and current counts |
| `paper/figures/` | Composition, processing and property maps |
| `paper/manuscript/` | Preprint manuscript (PDF and LaTeX), built from the data by `code/06_manuscript.py` |
| `data/verification/verification_log.csv` | The author's value-by-value verification record |
| `docs/CODEBOOK.md` | Every column defined, plus unit conversions and grading rules |
| `docs/LIMITATIONS.md` | What this database cannot tell you |
| `docs/DECISIONS.md` | The judgment calls behind v0.1 and who made them |

## How to rebuild it

You need Python 3.9 or later and matplotlib (`pip install matplotlib`). From this folder, run:

```
./run_all.sh --final    # released figures
./run_all.sh            # same, with a draft watermark on figures (for work in progress)
```

The scripts run in order:

1. `code/01_register.py` fingerprints the raw files.
2. `code/02_build.py` harmonizes units, grades rows and applies verification.
3. `code/03_qa.py` runs the checks and writes `paper/stats.json`.
4. `code/04_figures.py` draws the figures.
5. `code/05_crosscheck.py` compares against a text-mined database (not run in v0.1).
6. `code/06_manuscript.py` rebuilds the preprint; every number in it is computed from the released files (needs pdflatex).

## How values get in

1. An open-access paper is found and its license is recorded (`data/raw/sources_*.csv`).
2. Each value is entered with a short verbatim quote and its location in the paper (`data/raw/extractions_*.csv`).
3. The author opens the paper and confirms the value, its unit, the sample and the measurement temperature in `data/verification/verification_log.csv`.
4. Only verified or corrected values count toward release statistics.

Candidate papers not yet extracted, and papers excluded with a reason, are listed in `data/raw/queue_*.csv`.

## Sources

Primary data comes from open-access papers. Each paper's DOI, license and access date are in `data/processed/opensmfe_sources.csv`.

A cross-check against a text-mined magnetic-materials database is planned for a later version. `code/05_crosscheck.py` is included but not run in v0.1.

## License and citation

- Code: MIT.
- Data and documentation: CC BY 4.0.
- To cite the database: Ejeka, J. C. (2026). *OpenSmFe: an open, processing-aware database of samarium-iron(-nitrogen) permanent magnet properties* (v0.1.0). Zenodo. https://doi.org/10.5281/zenodo.23248500. Use the all-versions DOI 10.5281/zenodo.23248499 to cite the project in general. Please also cite the original papers for any values you use.

## Maintainer

Joshua Chukwuemeka Ejeka, Independent Researcher (jejeka@uwyo.edu).

Built with AI assistance (Claude) for literature search, first-draft extraction and code. The author verified every value against its source paper and approved every analytic decision. See `docs/LIMITATIONS.md` and `docs/DECISIONS.md`.
