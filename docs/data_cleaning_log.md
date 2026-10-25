# LankaHarvest — Data Cleaning Log

This document records data-quality issues identified during dataset processing.

## DQ-001: Incorrect Cultivation Year — Paddy Yield

**Issue:** `2020/2021` incorrectly recorded as `2000/2021` in the Maha dataset.

**Correction:** Corrected in a separate Excel copy.

**Status:** Corrected; original source confirmation pending.

## DQ-002: Inconsistent District Spelling

**Issue:** `KILLINOCHCHI` and `KILINOCHCHI` represented the same district.

**Correction:** Standardized to `KILINOCHCHI` using Python.

**Status:** Resolved.

## DQ-003: Missing and Zero Paddy Yield Values

**Issue:** Preliminary checks identified 80 missing markers and 21 zero-yield records.

**Action:** Retain values until their meanings are verified.

**Status:** Pending validation.

## DQ-004: Incorrect Cultivation Year — Irrigation

**Issue:** `2020/2021` incorrectly recorded as `2000/2021` in the Maha harvested-extent dataset.

**Correction:** Corrected in the Excel dataset.

**Status:** Resolved; zero duplicate records.

## DQ-005: Irrigation Shares Above 100%

**Issue:** 19 records produced irrigation shares above 100%.

**Finding:** Major + Minor exceeded Total harvested area by exactly 1 hectare in each affected record.

**Action:** Capped the calculated percentages at 100%, preserving original area measurements.

**Status:** Derived values adjusted; source discrepancies documented.

## DQ-006: Missing Irrigation Values

**Issue:** 568 records have missing irrigation-share values.

**Action:** Retained missing values as `NaN` for further preprocessing.

**Status:** Pending ML missing-data strategy.

## DQ-007: Missing Solar Radiation Data

**Dataset:** NASA POWER Climate Dataset

**Issue:** 150 seasonal solar-radiation values are missing.

**Distribution:**
- 1981: 50 records
- 1982: 50 records
- 1983: 50 records

**Finding:** All 150 missing records occur across the 25 districts and both cultivation seasons during 1981–1983.

**Action:** Retain missing values as `NaN`. No artificial values were introduced.

**Status:** Missing period verified; ML handling pending.

## Data Processing Notes

- Original and corrected source data are maintained separately where applicable.
- Climate data uses approximate district reference locations.
- Maha and Yala climate periods are initially defined as September–March and April–August.
- Data quality will be rechecked after merging all datasets.

## DQ-008: Inconsistent Harvested Extent Totals

**Issue:** Identified inconsistencies between reported total harvested area and the sum of major, minor and rainfed harvested areas.

**Examples:**
- Batticaloa, 1984 Maha: 62,000 ha discrepancy.
- Puttalam, 1983 Maha: 10,000 ha discrepancy.

**Action:** Verified that these discrepancies exist in the original DCS Excel source. Original values preserved.

**Status:** Source verification and correction pending.