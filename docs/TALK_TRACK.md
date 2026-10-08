# Talking about OpenSmFe

*Plain-language note: what to say when someone asks about this project, such as an attorney, an officer, a colleague, or a LinkedIn post. The counts match `paper/stats.json` for v0.1.0. Say "seed release": it is honest, and it is the accurate description of 6 papers.*

## 60-second version

**The problem.** The United States depends on imported neodymium magnets for electric vehicles, wind turbines and defense systems. Samarium-iron-nitride is a leading alternative, but the published results are scattered across hundreds of papers in mixed units, measured on different kinds of samples. Nobody can fairly compare them without redoing the work by hand.

**What I built.** OpenSmFe is an open database of those results. Every number records how the magnet was made and how it was measured, and links to the exact sentence in the source paper. Every row has a grade saying whether it can fairly be compared with others. I personally verified every value. The first release, v0.1.0, is a seed batch of 21 values from 6 open-access papers that establishes the format; the full version is due in 2027.

**What it makes possible.** Researchers and manufacturers can see which processing routes give which magnet performance, with the comparability caveats attached. Even the seed batch caught a published paper reporting the same remanence two different ways.

**Where it is.** On GitHub (github.com/johemeks/opensmfe), archived on Zenodo with a permanent DOI: 10.5281/zenodo.23248499.

## Two-sentence version

I built OpenSmFe, an open and verified database linking how samarium-iron-nitride magnets are made to how they perform, with a comparability grade on every value. It gives U.S. researchers and manufacturers a reusable map of a leading rare-earth-lean alternative to imported neodymium magnets.

## Questions you may be asked

1. **Where does the data come from?** From open-access, peer-reviewed papers. Every value carries the paper's DOI and the exact sentence it came from. AI helped find papers and draft the extractions, and I checked every value against the paper myself.
2. **What are its limits?** Version 0.1 is a seed batch of six papers, so it shows the method rather than the whole field. It covers only open-access papers. It reports values as published rather than re-measuring them. Many papers do not state the measurement temperature, which is exactly what the comparability grade flags.
3. **Why does this matter for the United States?** Magnet supply is a recognized critical-materials risk. An open map of what works in Sm-Fe-N processing lowers the cost for every U.S. group and company working on alternatives, and nobody has to rebuild it privately.
