
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

# Convert paddy yield values to numbers
master["paddy_yield_kg_per_ha"] = pd.to_numeric(
    master["paddy_yield_kg_per_ha"],
    errors="coerce"
)

# Treat suspicious zero yields as missing
# before calculating previous-season yield
master["paddy_yield_kg_per_ha"] = master[
    "paddy_yield_kg_per_ha"
].replace(0, float("nan"))

# Define chronological order of cultivation seasons
master["season_order"] = master["season"].map({
    "Yala": 0,
    "Maha": 1
})

# Sort records chronologically for each district
master = master.sort_values(
    ["district", "cultivation_year", "season_order"]
).reset_index(drop=True)

# Calculate previous-season paddy yield
master["previous_paddy_yield_kg_per_ha"] = (
    master.groupby("district")["paddy_yield_kg_per_ha"].shift(1)
)

# Calculate previous-season irrigation share
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
# Investigate Kegalle irrigation records

kegalle = irrigation[
    irrigation["district"] == "KEGALLE"
]

print(kegalle[
    [
        "cultivation_year",
        "season",
        "major_ha",
        "minor_ha",
        "rainfed_ha",
        "total_ha",
        "irrigation_share_pct"
    ]
].head(15).to_string(index=False))

# 9. INVESTIGATE MISSING TARGET VALUES

missing_yield = final_data[
    final_data["paddy_yield_kg_per_ha"].isna()
]

print("Missing yields by district:")
print(missing_yield.groupby("district").size())

print("Missing yields by season:")
print(missing_yield.groupby("season").size())

print(
    "Zero yield records:",
    (final_data["paddy_yield_kg_per_ha"] == 0).sum()
)

# Check records where paddy yield is zero

zero_yield = final_data[
    final_data["paddy_yield_kg_per_ha"] == 0
]

print(zero_yield[
    ["district", "cultivation_year", "season",
     "paddy_yield_kg_per_ha"]
].to_string(index=False))


# Compare zero yields with harvested extent

irrigation = pd.read_csv(
    "Data/processed/irrigation_dataset.csv"
)

zero_yields = final_data[
    final_data["paddy_yield_kg_per_ha"] == 0
]

comparison = zero_yields.merge(
    irrigation[
        ["district", "cultivation_year", "season", "total_ha"]
    ],
    on=["district", "cultivation_year", "season"],
    how="left"
)

print(comparison[
    ["district", "cultivation_year", "season", "total_ha"]
].to_string(index=False))

print(
    "Zero previous yields:",
    (final_data["previous_paddy_yield_kg_per_ha"] == 0).sum()
)

# 10. CHECK ML DATASET COMPLETENESS

# Records with a valid target
valid_target = final_data.dropna(
    subset=["paddy_yield_kg_per_ha"]
)

# Records with all features and target available
complete_records = final_data.dropna()

print("Records with valid target:", len(valid_target))
print("Fully complete records:", len(complete_records))
print(
    "Complete records by season:"
)
print(complete_records.groupby("season").size())

# 11. CHECK COMPLETE RECORDS BY DISTRICT

print("\nComplete records by district:")

print(
    complete_records.groupby("district")
    .size()
    .reindex(sorted(final_data["district"].unique()), fill_value=0)
    .to_string()
)

# 12. INVESTIGATE DISTRICTS WITH LOW COVERAGE

districts = ["JAFFNA", "KEGALLE", "GALLE", "COLOMBO"]

columns = [
    "paddy_yield_kg_per_ha",
    "previous_paddy_yield_kg_per_ha",
    "previous_irrigation_share_pct",
    "temperature_c",
    "solar_radiation_daily_mean"
]

selected = final_data[
    final_data["district"].isin(districts)
]

print("\nMissing values by district and feature:")

print(
    selected.groupby("district")[columns]
    .agg(lambda x: x.isna().sum())
    .to_string()
)