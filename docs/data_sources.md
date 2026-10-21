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

**Status:** Collected — validation pending.

## 2. Climate Dataset

**Source:** [NASA POWER](https://power.larc.nasa.gov/)

**Coverage:** 1981–2026 (daily data)

**Variables Collected:**
- Precipitation
- Temperature
- Relative humidity
- Solar radiation

**Description:**
- Downloaded using NASA POWER API and Python.
- Data collected for 25 districts using representative coordinates.
- Rainy days will be calculated from daily precipitation.
- Missing values and accuracy will be evaluated during preprocessing.

**Status:** Collected — preprocessing pending.

## 3. District Coordinates Dataset

**Source:** [Sri Lanka Districts GeoJSON — GitHub](https://github.com/Kavidu23/sri-lanka-districts-geo-json)

**Description:**
- Contains latitude and longitude reference coordinates for 25 districts.
- Used to automate climate data collection through NASA POWER.
- Coordinates are approximate district reference locations, not necessarily paddy-growing locations.

**Status:** Collected.

## 4. Irrigation Dataset

**Source:** [Department of Census and Statistics, Sri Lanka](https://www.statistics.gov.lk/Agriculture/StaticalInformation/PaddyStatistics)

**Description:**
- Harvested area under Major, Minor and Rainfed cultivation.
- Intended for developing an irrigation-related feature.

**Status:** Maha dataset collected; Yala dataset pending.

## 5. Next Steps

- Complete irrigation data collection.
- Combine the collected datasets.
- Clean and validate the final CSV.
- Compare with existing published datasets.