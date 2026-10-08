# OpenSmFe codebook

*Plain-language note: this lists every column in the database, what it means and where it comes from. Open it when you need to know what a column holds. It also lists the unit conversions and the comparability-grade rules you will rule on.*

## opensmfe_sources.csv (one row per paper)

| Column | Meaning |
|---|---|
| source_id | Short ID: first author surname plus year (or journal plus year when the authors are unconfirmed) |
| doi | Digital Object Identifier of the paper |
| title, authors, journal, year | Bibliographic details as shown on the publisher page |
| license | Reuse license of the paper (for example CC BY 3.0) |
| license_basis | Where the license was read (page metadata, or journal policy if not shown on the article) |
| oa_route | How the paper is open access |
| access_url, accessed | Page read and date read |
| text_read | `full text` or `abstract only` |
| status_note | Anything that limited extraction |

## opensmfe_samples.csv (one row per sample)

| Column | Meaning |
|---|---|
| sample_id | `SOURCE-letter`. One sample is one distinct material state in one paper. |
| sample_label | Short description in the paper's own terms |
| composition_nominal | Composition as written (nominal, not measured, unless the paper says otherwise) |
| family | `2:17` (Th2Zn17/Th2Ni17-type Sm2Fe17-based) or `1:7` (TbCu7-type disordered) |
| nitrided | Y or N |
| alloy_route | How the starting alloy or powder was made (arc melting, strip casting, reduction-diffusion, spray pyrolysis, plasma, commercial powder) |
| milling | Milling or grinding step and conditions |
| melt_spinning | Wheel speed and conditions, if melt-spun |
| anneal | Heat treatment before nitriding (temperature, time, atmosphere) |
| nitriding | Nitriding temperature, time and gas |
| consolidation | Bonding, sintering, hot pressing or alignment step, with conditions |
| phase_outcome | Phases reported (for example single-phase Sm2Fe17N3, or with alpha-Fe) |
| sample_form | powder; aligned powder; aligned powder in resin; sintered bulk; bonded bulk; ribbon; film |
| aligned | Y or N (magnetic alignment) |
| particle_size_um | Mean particle size in micrometres, if reported |

## opensmfe_measurements.csv (one row per value)

| Column | Meaning |
|---|---|
| meas_id | `sample_id-property`, plus `@T K` if measured away from room temperature |
| property | Hcj (intrinsic coercivity); Hcb (normal coercivity); Hc_unspecified (the paper says only "coercivity"); Br (remanence, volume units); Mr (remanent magnetization, mass units); Ms (saturation magnetization); BHmax; Tc (Curie temperature) |
| value_as_published, unit_as_published | Exactly as printed in the paper |
| value_si, unit_si | Converted value (rules below) |
| basis | For magnetization: `mass` (A m2/kg) or `volume` (T) |
| meas_T_K | Measurement temperature in kelvin, if known |
| meas_T_status | stated; assumed_RT (implied, awaiting confirmation); not_stated; n/a (Curie temperature) |
| method | Instrument or method, if stated (VSM, PPMS, hysteresisgraph, thermomagnetic) |
| evidence_quote | The shortest verbatim sentence or fragment containing the value |
| evidence_location | Abstract, section, table or figure caption |
| extraction_note | Anything unusual, such as an internal inconsistency in the paper |
| comparability | A, B or C (rules below) |
| comparability_reasons | Why the row is not A |
| verification_status | unverified; verified; corrected; rejected |
| verified_by, verified_on, verification_note | From the author's verification log |

## Unit conversions (code/units.py)

| Property | Published unit | Converted to | Factor |
|---|---|---|---|
| Coercivity | kOe | kA/m | × 79.5775 (= 1000/4π) |
| Coercivity | Oe | kA/m | × 0.0795775 |
| Coercivity | MA/m | kA/m | × 1000 |
| Coercivity | T (μ0Hc) | kA/m | × 795.775 |
| Magnetization | emu/g | A m2/kg | × 1 (numerically identical) |
| Remanence | kG | T | × 0.1 |
| (BH)max | MGOe | kJ/m3 | × 7.95775 |
| Curie temperature | °C | K | + 273.15 |

**Mass-basis values are never converted to tesla.** That conversion needs the sample's density, which most papers do not report for powders or bonded magnets.

## Comparability grade (code/02_build.py, function `grade`)

| Grade | Meaning | Rules (provisional; the author rules on these) |
|---|---|---|
| A | Directly comparable | Measured at 290 to 305 K (stated); coercivity type known; sample form stated; standard unit; no inconsistency |
| B | Comparable with care | Any one or more of: measurement temperature not stated or only implied; coercivity type not stated; mass-basis value for a bulk magnet; (BH)max of a loose powder (depends on assumed density); sample form unconfirmed; the paper reports the value inconsistently; a Curie temperature that is approximate or possibly quoted from literature |
| C | Not directly comparable | Measured away from room temperature (for example 10 K) |

Grades are recomputed on every build. When the author fills `confirmed_meas_T` or `confirmed_property` in the verification log, the affected rows re-grade automatically.

## What counts as a primary value

Only values a paper reports for its **own** samples. Values a paper quotes from earlier work, including all values in review articles, are not entered. Reviews go to the queue and are used to find primary papers.
