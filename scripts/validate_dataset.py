"""LankaHarvest: audit the final dataset and investigate missing irrigation values.

Run from the project root:
    python scripts/validate_dataset.py

This script only reads datasets and writes a review report. It does NOT fill
missing values or change existing datasets.
"""

# 1. IMPORTS AND FILE PATHS
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_ROOT / "Data" / "processed"
REPORT_PATH = PROJECT_ROOT / "Data" / "interim" / "irrigation_validation_report.csv"
KEYS = ["district", "cultivation_year", "season"]
AREAS = ["major_ha", "minor_ha", "rainfed_ha"]


# 2. LOAD AND CHECK OUR DATASETS
final = pd.read_csv(PROCESSED / "final_dataset.csv")
irrigation = pd.read_csv(PROCESSED / "irrigation_dataset.csv")

for name, df in [("Final", final), ("Irrigation", irrigation)]:
    if df.duplicated(subset=KEYS).any():
        raise ValueError(f"{name} dataset contains duplicate district-year-season records")

print("\n=== FINAL DATASET CHECK ===")
print("Rows:", len(final))
print("Districts:", final["district"].nunique())
print("Records with known target:", final["paddy_yield_kg_per_ha"].notna().sum())
print("Fully complete records:", final.dropna().shape[0])
print("\nMissing values by column:")
print(final.isna().sum().to_string())


# 3. INVESTIGATE MISSING IRRIGATION SHARES
review = irrigation.loc[
    irrigation["irrigation_share_pct"].isna(),
    KEYS + AREAS + ["total_ha", "irrigation_share_pct"]
].copy()

review["missing_area_count"] = review[AREAS].isna().sum(axis=1)
review["missing_area_type"] = review[AREAS].isna().idxmax(axis=1).where(
    review["missing_area_count"] == 1
)
review["implied_missing_ha"] = float("nan")
review["review_status"] = "INSUFFICIENT_DATA"

# If exactly one irrigation-area category is missing, we can check what
# the reported total implies. This does NOT prove the missing value is zero.
can_check = (
    (review["missing_area_count"] == 1)
    & review["total_ha"].notna()
    & (review["total_ha"] > 0)
)

review.loc[can_check, "implied_missing_ha"] = (
    review.loc[can_check, "total_ha"]
    - review.loc[can_check, AREAS].sum(axis=1)
)

# Allow up to a 2-hectare difference for the purpose of FLAGGING records,
# not for automatically correcting them.
near_zero = can_check & review["implied_missing_ha"].abs().le(2)
review.loc[near_zero, "review_status"] = "NEAR_ZERO_VERIFY_SOURCE"
review.loc[can_check & ~near_zero, "review_status"] = "CHECK_SOURCE_TOTAL"

print("\n=== IRRIGATION REVIEW ===")
print("Missing irrigation-share records:", len(review))
print("\nReview categories:")
print(review["review_status"].value_counts().to_string())
print("\nMissing irrigation-share records by district:")
print(review.groupby("district").size().sort_values(ascending=False).to_string())


# 4. SHOW KEGALLE AS OUR FIRST CASE STUDY
print("\n=== KEGALLE: FIRST 15 MISSING-SHARE RECORDS ===")
cols = KEYS + AREAS + ["total_ha", "implied_missing_ha", "review_status"]
print(review.loc[review["district"] == "KEGALLE", cols].head(15).to_string(index=False))


# 5. SAVE A REVIEW REPORT WITHOUT CHANGING THE DATA
REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
review.to_csv(REPORT_PATH, index=False)
print(f"\nReview report saved to: {REPORT_PATH}")
print("No original data was modified.")
print("NEXT: Verify what a dash/blank means in the original DCS Excel file.")
