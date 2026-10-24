
# ==================================================
# LankaHarvest - Final Dataset Construction
# ==================================================
# Purpose:
# Combine paddy yield, climate and irrigation data
# into one dataset for machine learning.
# ==================================================


# 1. IMPORT LIBRARIES

import pandas as pd
from pathlib import Path


# 2. READ THE THREE DATASETS

data_folder = Path("Data/processed")

paddy = pd.read_csv(data_folder / "master_dataset.csv")

climate = pd.read_csv(data_folder / "climate_dataset.csv")

irrigation = pd.read_csv(data_folder / "irrigation_dataset.csv")


# 3. STANDARDIZE THE MERGE COLUMNS

merge_columns = ["district", "cultivation_year", "season"]

for df in [paddy, climate, irrigation]:

    # Standardize district names
    df["district"] = df["district"].str.strip().str.upper()

    df["district"] = df["district"].replace(
        "KILLINOCHCHI", "KILINOCHCHI"
    )

    # Standardize year and season
    df["cultivation_year"] = df["cultivation_year"].astype(int)
    df["season"] = df["season"].str.strip().str.title()

    df["district"] = df["district"].replace({
    "MONERAGALA": "MONARAGALA",
    "MULLATIVU": "MULLAITIVU"
})

# 4. VALIDATE DATASET KEYS

for name, df in [
    ("Paddy", paddy),
    ("Climate", climate),
    ("Irrigation", irrigation)
]:

    if df.duplicated(subset=merge_columns).any():
        raise ValueError(f"{name} dataset contains duplicate records")


# 5. MERGE THE THREE DATASETS

# Keep all paddy records, even without climate data
master = pd.merge(
    paddy,
    climate,
    on=merge_columns,
    how="left",
    validate="one_to_one",
    indicator="climate_match"
)

# Add irrigation share from the same season
master = pd.merge(
    master,
    irrigation[merge_columns + ["irrigation_share_pct"]],
    on=merge_columns,
    how="left",
    validate="one_to_one",
    indicator="irrigation_match"
)


# 6. CALCULATE PREVIOUS-SEASON FEATURES

# Convert yield values to numbers.
# Missing markers such as '-' become NaN.
master["paddy_yield_kg_per_ha"] = pd.to_numeric(
    master["paddy_yield_kg_per_ha"],
    errors="coerce"
)

# Within one calendar year, Yala comes before Maha
# when Maha is labelled by its starting year.
master["season_order"] = master["season"].map({
    "Yala": 0,
    "Maha": 1
})

# Arrange records chronologically for each district
master = master.sort_values(
    ["district", "cultivation_year", "season_order"]
).reset_index(drop=True)

# Previous completed cultivation season's yield
master["previous_paddy_yield_kg_per_ha"] = (
    master.groupby("district")["paddy_yield_kg_per_ha"].shift(1)
)

# Use previous-season irrigation share to avoid
# using current-season harvested-area information
master["previous_irrigation_share_pct"] = (
    master.groupby("district")["irrigation_share_pct"].shift(1)
)


# 7. SELECT FINAL DATASET COLUMNS

final_columns = [
    "district",
    "cultivation_year",
    "season",
    "temperature_c",
    "seasonal_rainfall_mm",
    "previous_paddy_yield_kg_per_ha",
    "previous_irrigation_share_pct",
    "solar_radiation_daily_mean",
    "relative_humidity_pct",
    "rainy_days",
    "paddy_yield_kg_per_ha"
]

final_data = master[final_columns]


# 8. VALIDATE AND SAVE FINAL CSV

print("Total rows:", len(final_data))

print("Unique districts:", final_data["district"].nunique())

print(
    "Duplicate records:",
    final_data.duplicated(subset=merge_columns).sum()
)

print(
    "Rows without matching climate data:",
    (master["climate_match"] == "left_only").sum()
)

print(
    "Rows without matching irrigation data:",
    (master["irrigation_match"] == "left_only").sum()
)

print("\nMissing values:")
print(final_data.isna().sum())

# Ensure no paddy records were accidentally removed
if len(final_data) != len(paddy):
    raise ValueError("Row count changed during merging")

if final_data.duplicated(subset=merge_columns).any():
    raise ValueError("Final dataset contains duplicate records")

# Export the final dataset
output_file = data_folder / "final_dataset.csv"

final_data.to_csv(output_file, index=False)

print("\nFinal dataset saved successfully!")
print(final_data.head(10))
