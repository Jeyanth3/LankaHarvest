# LankaHarvest

**Sri Lanka District-Level Paddy Yield Prediction Using Machine Learning**

LankaHarvest aims to predict average paddy yield (kg/ha) for Sri Lankan districts using historical agricultural and climate data.

The model predicts **yield per hectare**, not total district production or individual farm yield.

## Project Objective

Develop a machine learning system that estimates seasonal paddy yield based on district, cultivation year, season, rainfall, temperature, humidity, solar radiation, rainy days, previous yield, and historical irrigation conditions.

## Development Status

**Phase 1: Data Collection and Preprocessing — Completed for initial ML experiments**

- Historical datasets collected and processed.
- Paddy yield, climate, and irrigation datasets integrated.
- Missing values and inconsistencies investigated.
- Automated validation reports generated.
- Remaining data-quality limitations documented.

**Next: Phase 2 — Machine Learning Model Development**

## Dataset Summary

| Description | Value |
|---|---:|
| Total records | 2,375 |
| Districts | 25 |
| Historical coverage | 1978–2025 |
| Total columns | 11 |
| Input features | 10 |
| Target variable | 1 |
| Records with valid target | 2,274 |
| Fully complete records | 1,745 |
| Missing target values | 101 |
| Duplicate records | 0 |

## Input Features

1. District
2. Cultivation year
3. Season (Maha/Yala)
4. Seasonal rainfall (mm)
5. Average seasonal temperature (°C)
6. Previous-season paddy yield (kg/ha)
7. Previous-season irrigated harvested-area share (%)
8. Mean daily solar radiation
9. Average seasonal relative humidity (%)
10. Number of rainy days

**Target:** `paddy_yield_kg_per_ha`

## Data Sources

- Department of Census and Statistics, Sri Lanka — Paddy yield
- Department of Census and Statistics, Sri Lanka — Harvested extent and irrigation
- NASA POWER — Historical climate data
- Sri Lanka Districts GeoJSON — District coordinates

See `docs/data_sources.md` for details.

## Cultivation Season Definitions

| Season | Approximate climate period |
|---|---|
| Maha | September–March |
| Yala | April–August |

Maha is labeled using its starting calendar year. For example, Maha 2024/2025 is represented as `2024`.

These are fixed seasonal windows for initial model development. Actual cultivation dates may vary by district.

## Project Structure

| File | Purpose |
|---|---|
| `scripts/build_master_dataset.py` | Build paddy yield dataset |
| `scripts/build_irrigation_dataset.py` | Build irrigation dataset |
| `scripts/climate/download_climate_data.py` | Download daily NASA POWER climate data |
| `scripts/climate/build_climate_dataset.py` | Prepare seasonal climate dataset |
| `scripts/build_final_dataset.py` | Merge datasets and calculate previous-season features |
| `scripts/validate_dataset.py` | Validate missing values and irrigation inconsistencies |
| `Data/processed/final_dataset.csv` | Integrated historical dataset |
| `docs/data_sources.md` | Dataset sources |
| `docs/data_dictionary.md` | Dataset variables |
| `docs/data_cleaning_log.md` | Data-quality findings |

Run Python scripts from the project root.

## Data Quality

The integrated dataset contains:

- 101 missing target-yield values, including 21 suspicious reported zeros provisionally treated as missing.
- 126 missing previous-yield values.
- 589 missing previous-irrigation-share values.
- 275 missing solar-radiation values.
- 125 unmatched early historical climate records.
- 20 harvested-area records with component-versus-total discrepancies greater than 2 hectares.

These issues have been documented, and original source measurements are preserved.

Only 23 districts appear in the fully complete subset. Jaffna and Kegalle require a missing-feature strategy during ML development.

## Phase 2 — Machine Learning Development

1. Compare the reconstructed dataset with independently published data.
2. Prepare the ML training and evaluation datasets.
3. Handle missing features appropriately.
4. Split training, validation, and testing data chronologically.
5. Train a baseline regression model.
6. Experiment with Random Forest, XGBoost, or other suitable algorithms.
7. Evaluate predictions using MAE, RMSE, and R².
8. Assess prediction quality across different districts and seasons.

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- NASA POWER API
- Git and GitHub

## Important Limitations

- Climate observations represent one approximate coordinate per district.
- Irrigation share is based on harvested area, not physical irrigation-infrastructure coverage.
- Historical observed weather cannot be used as though it were already known for a future season.
- A sufficiently accurate nationwide prediction model has not yet been established.

**Current milestone:** Phase 1 dataset construction and initial validation completed. Ready to begin baseline ML experiments.