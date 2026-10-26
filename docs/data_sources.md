# LankaHarvest — Data Sources

This document records the data sources used for the LankaHarvest Paddy Yield Prediction project.

**Updated:** 26 October 2026

## 1. Paddy Yield Dataset

**Source:** [Department of Census and Statistics, Sri Lanka](https://www.statistics.gov.lk/Agriculture/StaticalInformation/PaddyStatistics)

**Coverage:**
- Maha: 1978–2025 (starting-year convention)
- Yala: 1979–2025

**Description:**
- District-level average paddy yield in kg/ha.
- Covers 25 districts and two cultivation seasons.
- Uses the source workbook's Total yield column.
- Extracted and combined using Python and Pandas.

**Processed file:** `Data/processed/master_dataset.csv`

**Total records:** 2,375
- Maha: 1,200
- Yala: 1,175

**Data quality:**
- 80 missing yield markers.
- 21 suspicious zero-yield values.
- One incorrect Maha year label corrected in a separate Excel copy.
- District-name spelling standardized during processing.

**Status:** Collected and processed. Remaining source uncertainties documented.

## 2. Climate Dataset

**Source:** [NASA POWER](https://power.larc.nasa.gov/)

**API:** https://power.larc.nasa.gov/api/temporal/daily/point

**Daily data coverage:** 1 January 1981 – 31 March 2026

**Collected parameters:**

| Parameter | Description |
|---|---|
| `PRECTOTCORR` | Daily precipitation |
| `T2M` | Daily mean temperature |
| `RH2M` | Daily relative humidity |
| `ALLSKY_SFC_SW_DWN` | Daily solar radiation |

**Data collection:**
- Downloaded using Python and NASA POWER API.
- Data collected for 25 representative district coordinates.
- Stored as daily climate CSV files.
- Aggregated into seasonal climate features.

**Seasonal definitions:**
- Maha: September 1 – March 31 of the following year
- Yala: April 1 – August 31

**Processed file:** `Data/processed/climate_dataset.csv`

**Seasonal coverage:** 1981–2025

**Total seasonal records:** 2,250

**Generated features:**
- Seasonal rainfall (mm)
- Average temperature (°C)
- Average relative humidity (%)
- Average daily solar radiation
- Rainy days (rainfall ≥ 1 mm)

**Data quality:**
- 150 missing seasonal solar-radiation values across 1981–1983.
- No matching climate records for the 125 paddy observations before 1981.
- Solar-radiation units require verification from the API response metadata.

**Limitations:**
- Uses one approximate geographic coordinate per district.
- Does not calculate agricultural-area-weighted district averages.
- Fixed seasonal windows may not represent exact cultivation dates.

**Status:** Collected, aggregated and initially validated.

## 3. District Coordinates Dataset

**Source:** [Sri Lanka Districts GeoJSON — GitHub](https://github.com/Kavidu23/sri-lanka-districts-geo-json)

**Local file:** `Data/raw/Climate/district_locations.csv`

**Description:**
- Provides representative geographic locations for 25 districts.
- Used for NASA POWER API requests.
- Coordinates are not necessarily located within paddy-growing areas.

**Status:** Collected and used for climate data extraction.

## 4. Irrigation / Harvested Extent Dataset

**Source:** [Department of Census and Statistics, Sri Lanka](https://www.statistics.gov.lk/Agriculture/StaticalInformation/PaddyStatistics)

**Coverage:**
- Maha: 1978–2025
- Yala: 1979–2025

**Description:**
- Contains harvested paddy extent in hectares.
- Includes Major Irrigation, Minor Irrigation, Rainfed and Total harvested extent.
- Extracted from official Maha and Yala Excel workbooks.

**Processed file:** `Data/processed/irrigation_dataset.csv`

**Total records:** 2,375

**Derived feature:**

`irrigation_share_pct = ((major_ha + minor_ha) / total_ha) × 100`

This is the share of harvested paddy area under major and minor irrigation, not a direct measure of irrigation infrastructure coverage.

**Data quality:**
- 568 missing irrigation-share values.
- 19 shares slightly above 100% were capped at 100%, preserving the original area measurements.
- 20 records have harvested-area total discrepancies greater than 2 hectares.
- Original source files do not explicitly define every dash or missing value.

**Validation reports:**
- `Data/interim/irrigation_validation_report.csv`
- `Data/interim/harvested_area_discrepancies.csv`

**Status:** Collected and processed. Unresolved discrepancies flagged for review.

## 5. Final Integrated Dataset

**File:** `Data/processed/final_dataset.csv`

The final historical dataset combines paddy yield, climate and irrigation data using:

- `district`
- `cultivation_year`
- `season`

**Dataset statistics:**

| Metric | Result |
|---|---:|
| Total records | 2,375 |
| Districts | 25 |
| Features | 10 |
| Target variables | 1 |
| Duplicate records | 0 |
| Unmatched climate records | 125 |
| Unmatched irrigation records | 0 |
| Valid target records | 2,274 |
| Fully complete records | 1,745 |

The integrated dataset uses previous-season paddy yield and previous-season irrigation share as predictors.

Suspicious zero-yield values are provisionally treated as missing only in the integrated dataset. Original source values are preserved.

## 6. Remaining Validation and Modeling Tasks

- Compare historical yields against an independently published dataset.
- Investigate significant harvested-area discrepancies.
- Confirm solar-radiation measurement units.
- Develop suitable missing-feature handling.
- Avoid prediction-time data leakage.
- Evaluate the model using chronological train/validation/test splits.

**Overall status:** Phase 1 dataset integration and initial automated validation completed. Ready for initial Phase 2 modeling experiments.