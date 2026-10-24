# LankaHarvest — Data Sources

This document records the datasets used in the LankaHarvest Paddy Yield Prediction project.

## 1. Paddy Yield Dataset

**Source:** [Department of Census and Statistics, Sri Lanka](https://www.statistics.gov.lk/Agriculture/StaticalInformation/PaddyStatistics)

**Coverage:** 1978–2025 (Maha), 1979–2025 (Yala)

**Description:**
- District-level average paddy yield (kg/ha).
- Includes Maha and Yala cultivation seasons.
- Extracted and combined using Python and Pandas.
- 2,375 records generated in `master_dataset.csv`.

**Status:** Collected and processed — final validation pending.

## 2. Climate Dataset

**Source:** [NASA POWER](https://power.larc.nasa.gov/)

**Coverage:** 1981–March 2026 (daily data)

**Variables Collected:**
- Precipitation
- Temperature
- Relative humidity
- Solar radiation

**Description:**
- Downloaded using NASA POWER API and Python.
- Daily climate data collected for 25 districts using representative coordinates.
- A Python script has been prepared to calculate seasonal climate features, including rainy days.

**Status:** Daily data collected — seasonal processing and validation pending.

## 3. District Coordinates Dataset

**Source:** [Sri Lanka Districts GeoJSON — GitHub](https://github.com/Kavidu23/sri-lanka-districts-geo-json)

**Description:**
- Contains reference coordinates for 25 districts.
- Used for automated NASA POWER data collection.
- Coordinates are approximate district locations, not necessarily paddy-growing areas.

**Status:** Collected.

## 4. Irrigation Dataset

**Source:** [Department of Census and Statistics, Sri Lanka](https://www.statistics.gov.lk/Agriculture/StaticalInformation/PaddyStatistics)

**Coverage:** 1978–2025 (Maha), 1979–2025 (Yala)

**Description:**
- Contains harvested extent (ha) under Major, Minor, and Rainfed cultivation.
- Maha and Yala datasets extracted and combined using Python.
- 2,375 records generated in `irrigation_dataset.csv`.
- Irrigated harvested-area share calculated using Major and Minor harvested areas.

**Status:** Collected and processed — 568 missing irrigation-share values retained for further handling.

## 5. Next Steps

- Validate the seasonal climate dataset.
- Combine paddy yield, irrigation, and climate datasets.
- Handle missing and invalid values.
- Compare with existing published datasets.
- Prepare the final ML training dataset.