# LankaHarvest — Data Dictionary

This document describes the variables used in the LankaHarvest datasets.

**Updated:** 26 October 2026

## 1. Dataset Structure

Each record represents a unique combination of district, cultivation year and season.

**Cultivation year convention:**
- Maha 2024/2025 is represented as `2024`.
- Yala 2024 is represented as `2024`.
- Within a calendar year, Yala precedes the Maha season beginning that year.

Missing numerical values are represented as `NaN` during processing.

## 2. Paddy Yield Dataset

**File:** `Data/processed/master_dataset.csv`

| Column | Description |
|---|---|
| `district` | Sri Lankan administrative district |
| `cultivation_year` | Starting year of Maha or calendar year of Yala |
| `season` | Maha or Yala |
| `paddy_yield_kg_per_ha` | District-level average paddy yield in kg/ha |

**Records:** 2,375

**Source-quality observations:**
- 80 missing yield markers.
- 21 reported zero yields requiring further source verification.

The original values are preserved in the source and master datasets. The integrated dataset provisionally treats the 21 zeros as missing.

## 3. Irrigation Dataset

**File:** `Data/processed/irrigation_dataset.csv`

| Column | Description |
|---|---|
| `district` | District name |
| `cultivation_year` | Cultivation year |
| `season` | Maha or Yala |
| `major_ha` | Harvested area under major irrigation (ha) |
| `minor_ha` | Harvested area under minor irrigation (ha) |
| `rainfed_ha` | Rainfed harvested area (ha) |
| `total_ha` | Reported total harvested area (ha) |
| `irrigation_share_pct` | Percentage of harvested area under major and minor irrigation |

**Records:** 2,375

**Formula:**

`irrigation_share_pct = (major_ha + minor_ha) / total_ha × 100`

The calculation requires a positive reported total and available irrigation-area values.

**Missing irrigation shares:** 568

**Important notes:**
- This is an irrigated harvested-area share, not the percentage of land equipped with irrigation.
- 19 calculated shares slightly above 100% were capped at 100%, preserving original area measurements.
- 20 records have harvested-area component discrepancies exceeding 2 hectares.
- Missing source values have not been universally converted to zero.
- The final dataset uses the previous-season irrigation share.

## 4. Climate Dataset

**File:** `Data/processed/climate_dataset.csv`

**Records:** 2,250

**Coverage:** 1981–2025

| Column | Description |
|---|---|
| `district` | District name |
| `cultivation_year` | Cultivation year |
| `season` | Maha or Yala |
| `seasonal_rainfall_mm` | Total seasonal precipitation (mm) |
| `temperature_c` | Average seasonal temperature (°C) |
| `relative_humidity_pct` | Average seasonal relative humidity (%) |
| `solar_radiation_daily_mean` | Mean daily solar radiation during the season; unit to be verified |
| `rainy_days` | Number of days with precipitation ≥ 1 mm |

**Climate periods:**
- Maha: September–March
- Yala: April–August

**Known limitations:**
- 150 missing solar-radiation records during 1981–1983.
- One representative geographic location used per district.
- Climate windows are approximations of cultivation seasons.

## 5. Final Integrated Dataset

**File:** `Data/processed/final_dataset.csv`

**Records:** 2,375

**Total columns:** 11

| Column | Role | Description |
|---|---|---|
| `district` | Feature | Administrative district |
| `cultivation_year` | Feature | Cultivation year |
| `season` | Feature | Maha or Yala |
| `temperature_c` | Feature | Mean seasonal temperature |
| `seasonal_rainfall_mm` | Feature | Seasonal rainfall total |
| `previous_paddy_yield_kg_per_ha` | Feature | Paddy yield of the preceding cultivation season in the same district |
| `previous_irrigation_share_pct` | Feature | Irrigated harvested-area share of the preceding season |
| `solar_radiation_daily_mean` | Feature | Mean daily solar radiation during the season |
| `relative_humidity_pct` | Feature | Mean seasonal relative humidity |
| `rainy_days` | Feature | Count of rainy days |
| `paddy_yield_kg_per_ha` | Target | Average seasonal paddy yield (kg/ha) |

Previous-season features are calculated by sorting district records chronologically and applying a one-season lag.

Suspicious zero yields are converted to `NaN` before calculating the previous-yield feature.

## 6. Missing Values in Final Dataset

| Column | Missing records |
|---|---:|
| `district` | 0 |
| `cultivation_year` | 0 |
| `season` | 0 |
| `temperature_c` | 125 |
| `seasonal_rainfall_mm` | 125 |
| `previous_paddy_yield_kg_per_ha` | 126 |
| `previous_irrigation_share_pct` | 589 |
| `solar_radiation_daily_mean` | 275 |
| `relative_humidity_pct` | 125 |
| `rainy_days` | 125 |
| `paddy_yield_kg_per_ha` | 101 |

**Summary:**
- Total records: 2,375
- Valid target records: 2,274
- Fully complete records: 1,745
- Unique districts: 25
- Duplicate district-year-season records: 0

The fully complete subset excludes Jaffna and Kegalle, requiring appropriate missing-feature handling for nationwide prediction.

## 7. ML Preparation Notes

- The target variable is average yield in kg/ha.
- Rows with unavailable target yields cannot directly train a supervised regression model.
- Missing input features may be handled using training-only preprocessing.
- Chronological data splitting is preferred over random splitting.
- Current-season harvested extent must not be used as a predictor for pre-harvest forecasting.
- Future predictions require weather information available at prediction time, such as weather forecasts or expected seasonal conditions.
- Unresolved source discrepancies must remain documented.