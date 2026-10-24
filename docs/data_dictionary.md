# LankaHarvest — Data Dictionary

This document describes the variables used in the LankaHarvest datasets.

## 1. Paddy Yield Dataset

| Column | Description |
|---|---|
| district | Sri Lankan administrative district |
| cultivation_year | Starting year of Maha or calendar year of Yala |
| season | Maha or Yala |
| paddy_yield_kg_per_ha | Average paddy yield (kg/ha) — target variable |

**Records:** 2,375

## 2. Irrigation Dataset

| Column | Description |
|---|---|
| district | District name |
| cultivation_year | Cultivation year |
| season | Maha or Yala |
| major_ha | Harvested area under major irrigation |
| minor_ha | Harvested area under minor irrigation |
| rainfed_ha | Rainfed harvested area |
| total_ha | Total harvested paddy area |
| irrigation_share_pct | Percentage of harvested area under major and minor irrigation |

**Records:** 2,375

**Missing irrigation shares:** 568

**Formula:**

`irrigation_share_pct = (major_ha + minor_ha) / total_ha × 100`

Current-season harvested-area shares are historical measurements. A previous-season or otherwise pre-harvest-available measure will be considered for forecasting.

## 3. Climate Dataset

The following variables are planned in the seasonal climate CSV.

| Column | Description |
|---|---|
| district | District name |
| cultivation_year | Cultivation year |
| season | Maha or Yala |
| seasonal_rainfall_mm | Total seasonal rainfall (mm) |
| temperature_c | Average seasonal temperature (°C) |
| relative_humidity_pct | Average seasonal relative humidity (%) |
| solar_radiation_daily_mean | Mean daily solar radiation during the season; unit to be verified |
| rainy_days | Days with precipitation ≥ 1 mm |

**Source:** NASA POWER

**Status:** Seasonal processing script prepared; output validation pending.

## 4. Dataset Conventions

- Each row represents one district, cultivation year, and season.
- Maha 1978/1979 is represented by 1978.
- Yala 1979 is represented by 1979.
- Missing values are represented as `NaN` during processing.
- The final ML dataset will include previous paddy yield as an additional input feature.