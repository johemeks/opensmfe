# Publish guide: OpenSmFe

*Plain-language note: the click-by-click steps to put OpenSmFe online and get its permanent citation number (DOI). Verification is done, so you can do this now. The build machine cannot reach GitHub or Zenodo to upload on your behalf, so these steps are yours. Total time is about 25 minutes.*

## Copy-ready text

**Title:** OpenSmFe: an open, processing-aware database of samarium-iron(-nitrogen) permanent magnet properties

**Short description (for GitHub, 350 characters max):** Open database of published Sm-Fe-N permanent magnet properties (Hc, Br, Ms, (BH)max, Tc), with composition, processing route, phase outcome, sample form, measurement temperature, a verbatim source quote and a comparability grade on every row.

**Keywords:** permanent magnets; Sm2Fe17N3; samarium iron nitride; rare-earth magnets; materials database; processing-structure-property; coercivity

**Author:** Joshua Chukwuemeka Ejeka, Independent Researcher (jejeka@uwyo.edu)

**Version:** v0.1.0 (seed release)

**License:** Data CC BY 4.0; code MIT

## Step 1. Put it on GitHub (10 min)

1. Go to https://github.com/new. Repository name: `opensmfe`. Choose **Public**. Leave "Add a README" **unticked**, because the project already has one. Click **Create repository**.
2. Unzip `opensmfe_v0.1.0.zip`. The project is already saved as a git repository, committed under your name and tagged `v0.1.0`. Open a terminal inside the `opensmfe` folder and paste these two lines, (already done by Claude on 2026-10-08):
   ```
   git remote add origin https://github.com/johemeks/opensmfe.git
   git push -u origin main --tags
   ```
   If GitHub asks for a password, use a personal access token instead (https://github.com/settings/tokens, tick "repo"), or install GitHub Desktop and use **Add existing repository**, then **Publish**.
   Refresh the GitHub page. You should see the README displayed below the file list.

## Step 2. Connect Zenodo before the release (3 min)

1. Log in at https://zenodo.org with your ORCID or GitHub account.
2. Click your name (top right), then **GitHub**. Find `opensmfe` in the list and flip its switch **On**. (If it is not listed, click **Sync now**.) The project includes a `.zenodo.json` file, so Zenodo fills in the title, your name, affiliation, license and keywords automatically.

## Step 3. Make the release, which mints the DOI (5 min)

1. On GitHub, open the repository, click **Releases** on the right, then **Draft a new release**.
2. Click **Choose a tag** and pick `v0.1.0` (it is already there). Type `v0.1.0` as the title.
3. In the description, paste: "Seed release of OpenSmFe: 21 values from 14 samples in 6 open-access papers, each verified by the author against its source. See README and docs/LIMITATIONS.md."
4. Click **Publish release**.
5. Within a few minutes, Zenodo shows a new record under **Upload** with a DOI that looks like `10.5281/zenodo.1234567`.

## Step 4. Record the DOI everywhere (5 min)

1. Add the DOI to `CITATION.cff` as a new line `doi: "10.5281/zenodo.NNNNNNN"` (your number), add `repository-code: "https://github.com/johemeks/opensmfe"`, and add the DOI to the README status line.
2. Commit and push the change (`git commit -am "Add DOI" && git push`).
3. Add a row to your evidence log: date, "OpenSmFe v0.1.0 dataset", the Zenodo DOI, the GitHub URL, and a saved PDF of the Zenodo page. Do it the same day. Publications not logged on the day they happen are the ones that go missing at petition time.

## Optional: add your ORCID

If you create an ORCID iD (https://orcid.org/register, 5 minutes), edit the Zenodo record, add it to your name, and click **Publish**. Then add it to `AUTHORS.json` and `CITATION.cff`. It links this DOI to you permanently, even if your name is spelled differently somewhere.

## Later: the data paper

At v1.0, Claude builds the manuscript from `paper/stats.json` and prepares an arXiv kit (category cond-mat.mtrl-sci; first-time arXiv authors may need an endorsement). You submit it yourself, because submission is your personal attestation.
