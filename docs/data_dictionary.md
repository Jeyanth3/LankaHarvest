# LankaHarvest — Data Dictionary

## Current Master Dataset

| Column | Data Type | Description |
|---|---|---|
| district | String | Sri Lankan administrative district |
| cultivation_year | Integer | Starting year of Maha, or calendar year of Yala |
| season | String | Maha or Yala |
| paddy_yield_kg_per_ha | Numeric | District-level average paddy yield in kilograms per hectare |

## Dataset Structure

Each record represents one district, one year, and one cultivation season.

**Current structural coverage:**
- Maha: 1,200 records
- Yala: 1,175 records
- Total: 2,375 records

## Cultivation Year Convention

- Maha 1978/1979 is represented as 1978.
- Yala 1979 is represented as 1979.

## Paddy Yield

The Total average yield from the source dataset is used. Major, Minor, and Rainfed yields are not summed.

## Data Quality

Missing yield values and zero values must be investigated before model training.