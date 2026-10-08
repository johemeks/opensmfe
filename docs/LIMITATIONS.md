# Limitations

*Plain-language note: an honest list of what OpenSmFe cannot tell you. Read it before using any number. The data paper's discussion section cannot claim more than this file allows.*

1. **v0.1 is a seed batch, not a survey.** It covers 6 open-access papers. It shows how the database works; it does not yet describe the field. Any pattern in the v0.1 figure reflects which papers were read, not which processing route is best.

2. **Open-access only.** Much of the Sm-Fe-N literature is behind paywalls, including much of the 1990s foundational work and most of *J. Magn. Magn. Mater.* and *J. Alloys Compd.* OpenSmFe includes only papers anyone can read. That is a deliberate choice for reuse and checking, but it is not a complete record, and open-access papers skew toward recent years.

3. **Some papers were read from the abstract only.** For some publishers (AIP full text, OSTI, Europe PMC), automated reading was blocked. Abstract-only rows are marked in `opensmfe_sources.csv` (`text_read`). Abstracts usually omit the measurement temperature and the coercivity type, so these rows grade B until the author confirms them from the full text.

4. **Values are as published, not re-measured.** OpenSmFe does not correct for demagnetizing fields, packing density or sample shape. The comparability grade warns where this matters; it does not fix it.

5. **No values read from figures in v0.1.** Many papers give key numbers only in plots. Digitizing them adds uncertainty and is deferred to a later decision.

6. **First-draft extraction was AI-assisted.** An AI reader drafted every extraction from the publisher page, and summarizing readers can misstate numbers. This is why every value carries a verbatim quote, why the quality checks test that the number appears in its own quote, and why every value was verified by the author before release. During the build, one spot-check found a correct number attached to the wrong sentence (since fixed). That is the kind of error the verification step exists to catch.

7. **Composition is nominal.** Most papers report the intended composition, not a measured one. Nitrogen content is especially uncertain (written "N3" or "Nx").

8. **Scope.** v1.0 covers the Sm2Fe17-based (2:17) and TbCu7-type (1:7) families, nitrided or not. It excludes SmFe12 (ThMn12-type) compounds, soft/hard composites, hybrid Nd-Fe-B/Sm-Fe-N magnets and fluorinated or carbided interstitials.

9. **No text-mined cross-check in v0.1.** The comparison with an automatically built database is deferred to a later version.

10. **Verification was recorded at the release level.** The author attested on 2026-10-08 that every value was checked against its source paper, and each row is marked `verified` on that basis. Details the check could add row by row, chiefly the measurement temperature and whether "coercivity" means Hcj or Hcb, were not recorded, so those rows keep their B grade. No row is graded A in v0.1 for this reason.
