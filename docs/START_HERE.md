# Start Here: OpenSmFe

*Read this first. It explains your project in plain language. Words in bold are explained in [GLOSSARY.md](GLOSSARY.md).*

## What you are building

A free, public spreadsheet of every reliable published measurement of samarium-iron-nitride magnets. Each row also records how the sample was made and how the measurement was taken.

## Why it matters

Almost every motor in an electric car or wind turbine uses neodymium magnets, and the United States depends on imports for them. **Sm-Fe-N** magnets are a leading alternative. They are strong, they tolerate heat, and they use less rare earth.

The research results are scattered across hundreds of papers. Papers use different units and measure different kinds of samples, and many leave out key details. A coercivity of "12 kOe" on loose powder is not the same claim as "12 kOe" on a finished magnet. Right now, anyone who wants to know which **processing route** gives the best magnet has to rebuild that comparison by hand.

OpenSmFe does that work once, in the open. Each number is linked to the exact sentence or table it came from. Each row is graded on how safely it can be compared with others. It is like a consumer-reports table for magnet recipes: what went in, what was done to it, what came out, and how trustworthy the comparison is.

## Where the information comes from

All sources are free and public.

| Source | In plain terms | What one row looks like | Link |
|---|---|---|---|
| Open-access research papers | Published magnet studies anyone can read for free (AIP Advances, MDPI journals, Scientific Reports, arXiv and similar) | One sample: its recipe, its processing, and its measured magnet properties | Listed per row in the database |
| Text-mined magnetic database (cross-check, later version) | A database software built by reading papers automatically. A later version will compare against it. | One compound and one property value | To be chosen |

## What you will have at the end

- [ ] **The OpenSmFe database** (CSV plus a column guide), every value verified by you
- [ ] **A public project page** on GitHub, with the code that rebuilds the database from its sources
- [ ] **A permanent citation number (DOI)** from Zenodo, for v1.0
- [ ] **Composition-process-property maps**: charts showing which processing routes give which magnet performance
- [ ] **A short data paper** describing the database, posted as a preprint
- [ ] **A cross-check report** (later version) showing where a text-mined database agrees with the hand-checked values

## How it connects to your work

This is Flagship 1 of your plan. It produces the composition-process-structure-property maps your proposed endeavor lists as a core output. Because it is open, other U.S. research groups and magnet makers can reuse it directly, without asking.

## What you need to do

| Your task | When | Time |
|---|---|---|
| Create accounts (ORCID, GitHub, Zenodo) | Now | 15 min |
| Answer five setup questions | Now | 10 min |
| Verify values against the papers, in batches | As each batch is ready | About 2 min per value |
| Rule on the judgment calls (for example, comparability grades) | During verification | 30 min |
| Rewrite the summary in your own words and approve publishing | Before release | 30 min |
| Submit the data paper yourself, using the guide | After the DOI exists | 20 min |

**The verification step is the big one.** You said you will verify every value. At about 2 minutes per value, 500 values is roughly 17 hours. That is spread across batches, not done in one sitting.

## The steps ahead

1. **Papers collected.** Find open-access Sm-Fe-N papers and record where each came from.
2. **Values extracted and harmonized.** Pull every number with its exact quote, and convert all units.
3. **Quality checks.** Look for impossible values, duplicates and unit mistakes.
4. **First map.** A first chart of coercivity by processing route.
5. **Cross-check and draft paper.** Compare against the text-mined database, then write the data paper from the numbers.
6. **Ready for your check.** You verify, then we publish.

*You are here: v0.1.0 verified and ready to publish (docs/PUBLISH_GUIDE.md). Steps 1 to 5 then repeat in batches until v1.0.*
