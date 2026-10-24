# LankaHarvest — Data Cleaning Log

This document records data-quality issues identified during dataset processing.

## DQ-001: Incorrect Cultivation Year — Paddy Yield

**Dataset:** Maha Paddy Yield

**Issue:** `2020/2021` incorrectly recorded as `2000/2021`.

**Detection:** Duplicate records for 2000 and missing records for 2020.

**Correction:** Manually corrected in a separate Excel copy.

**Status:** Corrected. Original source confirmation pending.

## DQ-002: Inconsistent District Spelling

**Issue:** Kilinochchi appeared as `KILLINOCHCHI` and `KILINOCHCHI`.

**Correction:** Standardized to `KILINOCHCHI` using Python.

**Status:** Corrected.

## DQ-003: Missing and Zero Paddy Yield Values

**Dataset:** Paddy Yield

**Issue:** Preliminary checks identified 80 missing-value markers (`-`) and 21 zero-yield records.

**Action:** Retain values pending investigation of their meanings.

**Status:** Pending validation.

## DQ-004: Incorrect Cultivation Year — Irrigation

**Dataset:** Maha Harvested Extent

**Issue:** `2020/2021` incorrectly recorded as `2000/2021`.

**Detection:** 25 duplicate district-year-season records and missing Maha 2020 records.

**Correction:** Corrected the year in the Excel dataset.

**Status:** Resolved; duplicate records reduced to zero.

## DQ-005: Irrigation Shares Above 100%

**Dataset:** Irrigation

**Issue:** 19 records produced irrigation percentages slightly above 100%.

**Finding:** Major + Minor exceeded Total harvested area by exactly 1 hectare in each affected record.

**Correction:** Capped the 19 calculated percentages at 100%, preserving original area measurements.

**Status:** Resolved for derived percentages. Source discrepancies remain documented.

## DQ-006: Missing Irrigation Values

**Dataset:** Irrigation

**Issue:** 568 records have unavailable irrigation-share values.

**Finding:** Missing values are concentrated in earlier years, with some gaps in later years.

**Action:** Retain records with `NaN` values for future preprocessing.

**Status:** Pending missing-data strategy.

## DQ-007: Missing Climate Observations

**Dataset:** NASA POWER

**Issue:** Some daily climate measurements may be unavailable and represented by `-999`.

**Action:** Convert these markers to `NaN` and apply completeness checks during seasonal aggregation.

**Status:** Processing implemented; seasonal validation pending.