# Disability and the Labor Market

This repository contains code used to build and analyze datasets from the **Encuesta Nacional de Ocupación y Empleo (ENOE)**. The original microdata can be downloaded from the [Open Science Framework](https://osf.io/89ftb/). After downloading, place the CSV files inside the folder `data/raw/` so that the scripts can locate them.

## Repository structure

- `scripts/python/` – Python scripts for cleaning, merging and analyzing the data.
- `scripts/stata/` – Stata do-files with equivalent operations.
- `scripts/R/` – R code used for regressions.
- `docs/` – Documentation and papers.
- `data/` – Folder expected to contain two subfolders:
  - `raw/` for the original CSV files from ENOE.
  - `processed/` where cleaned datasets will be written by the scripts.

## Usage

1. Download the ENOE data from [OSF](https://osf.io/89ftb/) and place the files `trabajos.csv`, `ingresos.csv` and `poblacion.csv` into `data/raw/`.
2. Run `python scripts/python/Base_creation.py` (or `base_creation_rev.py`) to build the merged dataset. Output files will be written to `data/processed/`.
3. Additional analyses such as regressions or summary statistics can be executed using the remaining scripts in `scripts/python`.

All paths in the Python files are now relative to the repository root, which makes the code portable across systems.
