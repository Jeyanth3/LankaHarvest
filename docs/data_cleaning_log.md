# LankaHarvest — Data Cleaning Log

This document records data-quality issues identified during dataset collection, processing, integration and validation.

**Updated:** 26 October 2026

**Policy:** Preserve original source measurements and document all transformations. Do not introduce unverified corrections.

## DQ-001: Incorrect Cultivation Year — Paddy Yield

**Issue:** `2020/2021` was incorrectly recorded as `2000/2021` in the Maha dataset.

**Correction:** Corrected the year label in a separate Excel copy used for extraction. Original source preserved.

**Status:** Corrected for processing; original source confirmation pending.

## DQ-002: Inconsistent District Spelling

**Issue:** District names were inconsistent across datasets.

**Examples:**
- `KILLINOCHCHI` and `KILINOCHCHI`
- `MONERAGALA` and `MONARAGALA`
- `MULLATIVU` and `MULLAITIVU`

**Correction:** Standardized district names in Python.

**Result:** 25 unique districts, zero duplicate keys and 125 expected unmatched climate records.

**Status:** Resolved.

## DQ-003: Missing and Zero Paddy Yield Values

**Issue:** Identified 80 missing yield markers and 21 reported zero-yield values.

**Investigation:**
- 13 zero-yield records had positive harvested-area values.
- 8 zero-yield records had missing harvested-area information.
- The meaning of these zero values remains unconfirmed.

**Action:**
- Preserved original source values.
- Provisionally treated the 21 suspicious zeros as `NaN` in the final integrated dataset.
- Applied this transformation before calculating previous-season yield.

**Result:**
- Missing target yields: 101
- Missing previous yields: 126
- Remaining zero target yields: 0
- Remaining zero previous yields: 0

**Status:** Provisional ML cleaning completed; official source verification pending.

## DQ-004: Incorrect Cultivation Year — Irrigation

**Issue:** `2020/2021` was incorrectly recorded as `2000/2021` in the Maha harvested-extent workbook.

**Correction:** Corrected the label in a separate Excel copy used for processing.

**Result:** Irrigation dataset contains 2,375 records with zero duplicate keys.

**Status:** Corrected for processing.

## DQ-005: Irrigation Shares Above 100%

**Issue:** 19 records produced irrigation shares above 100%.

**Finding:** Major + Minor harvested area exceeded the reported total by exactly 1 hectare in each affected record.

**Action:** Capped the derived irrigation percentages at 100% while preserving original area measurements.

**Status:** Derived values adjusted; original discrepancies documented.

## DQ-006: Missing Irrigation Values

**Issue:** 568 records have missing current-season irrigation-share values.

**Validation results:**

| Review category | Records |
|---|---:|
| `INSUFFICIENT_DATA` | 392 |
| `NEAR_ZERO_VERIFY_SOURCE` | 175 |
| `CHECK_SOURCE_TOTAL` | 1 |
| **Total** | **568** |

**Investigation:**
- Some original Excel cells contain a dash (`-`).
- The original workbooks do not explicitly explain the dash notation.
- In some records, the reported total approximately equals the sum of the available harvested-area categories.
- 175 records may have a missing category representing zero or negligible area, but this is not confirmed.
- An alternative formula identified 216 possible candidates for recovering irrigation shares. These candidates overlap with other review categories and are not verified corrections.

**Action:**
- Kept missing values as `NaN`.
- Did not automatically convert dashes into zero.
- Generated `Data/interim/irrigation_validation_report.csv`.

**Result:** 589 missing previous-season irrigation-share values in the final dataset.

**Status:** Pending source review and ML missing-feature handling.

## DQ-007: Missing Solar Radiation and Historical Climate Coverage

**Dataset:** NASA POWER Climate Dataset

**Issue:** 150 seasonal solar-radiation values are missing.

**Distribution:**
- 1981: 50 records
- 1982: 50 records
- 1983: 50 records

**Additional finding:** Climate data starts in 1981, leaving 125 earlier paddy-yield records without matching climate features.

**Action:** Retained unavailable values as `NaN`. No artificial climate data was introduced.

**Result:**
- Missing solar-radiation values in integrated dataset: 275
- Missing temperature values: 125
- Missing rainfall values: 125
- Missing relative humidity values: 125
- Missing rainy-day values: 125

**Status:** Missing values quantified. ML handling and solar-radiation unit verification pending.

## DQ-008: Inconsistent Harvested Extent Totals

**Issue:** Some records have reported total harvested areas that do not match the sum of major, minor and rainfed harvested areas.

**Validation:**
- Complete harvested-area records checked: 1,558
- Records with discrepancies greater than 2 hectares: 20
- Records with irrigation-share formula differences greater than 1 percentage point: 12

**Confirmed examples:**

| District | Year | Season | Calculated total | Reported total | Difference |
|---|---:|---|---:|---:|---:|
| Batticaloa | 1984 | Maha | 99,678 ha | 37,678 ha | +62,000 ha |
| Puttalam | 1983 | Maha | 9,763 ha | 19,763 ha | −10,000 ha |

These discrepancies were visually verified in the original DCS Excel worksheet.

**Action:**
- Generated `Data/interim/harvested_area_discrepancies.csv`.
- Preserved original measurements.
- No automatic corrections or universal alternative-formula replacements applied.

**Status:** Flagged for future investigation. Affected irrigation-share values require caution during ML modeling.

## Final Dataset Validation Summary

| Validation check | Result |
|---|---:|
| Total records | 2,375 |
| Unique districts | 25 |
| Duplicate district-year-season records | 0 |
| Unmatched climate records | 125 |
| Unmatched irrigation records | 0 |
| Records with valid target | 2,274 |
| Fully complete records | 1,745 |
| Missing target yields | 101 |
| Missing previous yields | 126 |
| Missing previous irrigation shares | 589 |
| Missing solar-radiation values | 275 |

## Data Processing Notes

- Original and corrected source workbooks are maintained separately.
- Climate data uses one approximate reference location per district.
- Maha is initially represented by September–March, while Yala is represented by April–August.
- Previous-season features are calculated chronologically within each district.
- Suspicious zero target yields are converted to missing values before generating yield lags.
- Source inconsistencies are reported without inventing replacement values.
- Training-only missing-value preprocessing is required during Phase 2.

## Phase 1 Completion Status

**Completed:**
- Paddy yield dataset preparation
- Irrigation dataset preparation
- Climate dataset preparation
- Final dataset integration
- Initial automated dataset validation
- Documentation of known inconsistencies

**Pending / Continuing During Phase 2:**
- External dataset comparison
- Review of unresolved irrigation anomalies
- Missing-feature preprocessing
- Chronological ML evaluation
- Model performance testing across all 25 districts

**Overall status:** Phase 1 construction and initial validation complete. Dataset is suitable for beginning baseline ML experiments, with the documented limitations.