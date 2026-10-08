# Next steps: v0.1 to v1.0 (April 2027)

*Plain-language note: what is left between this seed batch and the v1.0 release with a DOI, roughly in order.*

1. **Publish v0.1.0.** Done 2026-10-08: Zenodo DOI 10.5281/zenodo.23248499 (all versions), 10.5281/zenodo.23248500 (v0.1.0).
2. **Optional upgrade of v0.1 rows to grade A.** Record the measurement temperature and coercivity type from each paper's Methods section in the verification log.
3. **Choose a cross-check database** (later version). Then run `code/05_crosscheck.py` against its export.
4. **Open a full-text route.** Many publishers block automated reading, so the fastest path is: you download the PDFs of open-access papers in the queue (all free), drop them in a shared folder, and Claude extracts from the PDFs. The DOE public-access (OSTI) manuscripts are a U.S.-funded source worth prioritizing.
5. **Widen discovery.** Repeat the DOAJ query, then search arXiv (cond-mat.mtrl-sci), OSTI, J-STAGE (free-to-read Japanese journals, where much Sm-Fe-N work appears) and open-access articles in *J. Magn. Magn. Mater.* and *Acta Materialia*. Mine the two 2024 and 2025 reviews in the queue for primary references.
6. **Batch extraction and verification.** Work in batches of about 50 values. Realistic v1.0 size: 60 to 100 papers, 400 to 700 values, about 15 to 25 hours of your verification spread over five months.
7. **Maps.** Coercivity against particle size by route; remanence ratio against alignment; nitriding temperature and time against phase outcome (alpha-Fe present or not); and Tc against substitution.
8. **Data paper.** Build it from `paper/stats.json` at v1.0, then post it to arXiv and submit it to a data journal.
9. **Release.** Final build, publish gate, then GitHub release v1.0.0, then a Zenodo DOI.
