#!/usr/bin/env bash
# Rebuild OpenSmFe from the raw files, in order. Add --final to remove DRAFT stamps (only after verification).
set -euo pipefail
cd "$(dirname "$0")"
python3 code/units.py
python3 code/01_register.py
python3 code/02_build.py
python3 code/03_qa.py
python3 code/04_figures.py "$@"
python3 code/05_crosscheck.py
