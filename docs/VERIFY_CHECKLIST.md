# Verification record: OpenSmFe v0.1.0

*Plain-language note: the record of how this release was checked before publication.*

## Author verification

On 2026-10-08, Joshua Chukwuemeka Ejeka stated that he had verified every value against its source paper and approved publication. All 21 rows in `data/verification/verification_log.csv` are marked `verified` on the basis of that attestation.

Row-level details were not returned: the measurement temperature as stated in each paper's Methods, and whether each "coercivity" is Hcj or Hcb. Rows therefore keep the grades the build assigned (19 B, 2 C). To upgrade rows to A in a later version, fill `confirmed_meas_T` and `confirmed_property` in the log and re-run `./run_all.sh --final`.

## Checks completed during the build

- **Reproducibility.** A clean copy rebuilt from the raw files produced an identical `opensmfe.csv`.
- **Quote check.** Each of the 21 values appears in its own verbatim evidence quote. The three Liang et al. 2023 quotes were replaced with verbatim abstract text, which also showed that the paper reports intrinsic coercivity (iHc), so those rows are entered as Hcj.
- **Independent spot check of Saito 2024** against the publisher page. The values 12.4 kOe and 107 emu/g were confirmed. The 740 K Curie temperature was re-sourced to the sentence that reports the measurement.
- **Physics checks.** All values are within physical ranges for Sm-Fe-N. (BH)max does not exceed the Br²/4μ0 limit.
- **Licenses.** These were read from the page metadata (MDPI) or from the DOAJ journal record (AIP Advances: CC BY 4.0). The JMRT article-level license is not confirmed; only facts and a one-sentence quote are reused.
- **Publish gate.** `code/tools/publish_gate.py` passes, with no draft stamps, placeholders or secrets.

## Decisions

See `docs/DECISIONS.md`.
