"""Step 1: register the raw inputs.

Plain-language note: this script checks that the raw files are present and
well-formed, and records a fingerprint (SHA-256) of each one in
data/raw/PROVENANCE.txt. If anyone changes a raw file, the fingerprint changes,
and that is visible. You do not need to open this file.

Values reach data/raw/extractions_*.csv by reading open-access papers. In v0.1,
an AI reader read each publisher page and a human (the author) verifies each
value against the paper. The per-source URL and access date are in
sources_*.csv. No automated download is possible from the build machine,
because publisher sites are not on its network allowlist.
"""
import csv
import hashlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
VERSION = "v0.1"

REQUIRED = {
    f"sources_{VERSION}.csv": ["source_id", "doi", "license", "access_url", "accessed"],
    f"extractions_{VERSION}.csv": ["sample_id", "source_id", "property", "value_as_published",
                                   "unit_as_published", "evidence_quote", "evidence_location"],
    f"queue_{VERSION}.csv": ["doi", "decision", "reason"],
}


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    lines = []
    for name, cols in REQUIRED.items():
        p = RAW / name
        if not p.exists():
            sys.exit(f"missing raw file: {p}")
        with p.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        missing = [c for c in cols if c not in rows[0]]
        if missing:
            sys.exit(f"{name}: missing columns {missing}")
        lines.append(f"{name} | {len(rows)} rows | {p.stat().st_size} bytes | sha256:{sha256(p)}")
    src_ids = {r["source_id"] for r in csv.DictReader((RAW / f"sources_{VERSION}.csv").open(encoding="utf-8"))}
    ext_ids = {r["source_id"] for r in csv.DictReader((RAW / f"extractions_{VERSION}.csv").open(encoding="utf-8"))}
    orphan = ext_ids - src_ids
    if orphan:
        sys.exit(f"extractions reference unknown sources: {orphan}")
    header = ("# OpenSmFe raw-input provenance. One line per raw file: name | rows | bytes | SHA-256.\n"
              "# Per-paper URLs and access dates are inside sources_*.csv.\n")
    (RAW / "PROVENANCE.txt").write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
