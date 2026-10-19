#!/usr/bin/env bash
# Download the public raw data used in this project into data/.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/raw
curl -sSL -o data/VBOHCAR.xlsx "https://raw.githubusercontent.com/INFORMSJoC/2020.1022/master/results/VBOHCAR.xlsx"
curl -sSL -A "Mozilla/5.0" -o data/raw/Virginia.csv "https://svi.cdc.gov/Documents/Data/2022/csv/states/Virginia.csv"
curl -sSL -o data/raw/tl_2022_51_tract.zip "https://www2.census.gov/geo/tiger/TIGER2022/TRACT/tl_2022_51_tract.zip"
echo "downloaded"
