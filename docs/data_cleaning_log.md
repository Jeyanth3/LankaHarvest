# LankaHarvest — Data Cleaning Log

## DQ-001: Incorrect Cultivation Year

**Dataset:** Maha Paddy Yield

**Issue:** The year 2020/2021 was incorrectly recorded as 2000/2021.

**Detection:** Python validation identified 50 records for 2000 and no records for 2020.

**Correction:** The year was manually corrected in a separate Excel copy.

**Validation:** 48 unique Maha cultivation years and 1,200 records.

**Status:** Corrected; original source confirmation to be documented.

## DQ-002: Inconsistent District Spelling

**Issue:** Kilinochchi was represented as KILLINOCHCHI and KILINOCHCHI.

**Correction:** Standardized the district name as KILINOCHCHI.

**Status:** Corrected in processing script.

## DQ-003: Missing and Zero Yield Values

**Issue:** Preliminary validation detected missing markers and zero yield entries.

**Action:** Investigate whether these represent missing data or seasons without recorded production.

**Status:** Pending investigation.