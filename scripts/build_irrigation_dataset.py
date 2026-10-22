
# ==================================================
# LankaHarvest - Irrigation Dataset Processing
# ==================================================
# Purpose:
# Extract Maha and Yala harvested extent data,
# calculate irrigation share, and generate a CSV.
# ==================================================


# 1. IMPORT LIBRARIES

import pandas as pd


# 2. READ EXCEL FILES

datasets = {
    "Maha": pd.read_excel(
        "Data/interim/Harvested_Extent-Maha_Seasons-1979-2025_Corrected.xlsx",
        header=None
    ),

    "Yala": pd.read_excel(
        "Data/raw/Irrigation/Harvested_Extent-Yala_Seasons-1979-2025.xlsx",
        header=None
    )
}


# 3. EXTRACT DATA FROM BOTH SEASONS

all_data = []

for season, df in datasets.items():

    # Extract district names (25 districts)
    district = df.iloc[4:29, 1]

    # Each year contains Major, Minor, Rainfed and Total
    for year_col in range(2, df.shape[1] - 3, 4):

        # Extract cultivation starting year
        year = int(str(df.iloc[2, year_col]).split("/")[0])

        # Extract harvested extent (hectares)
        major = df.iloc[4:29, year_col]
        minor = df.iloc[4:29, year_col + 1]
        rainfed = df.iloc[4:29, year_col + 2]
        total = df.iloc[4:29, year_col + 3]

        # Create a DataFrame for the current year
        data = pd.DataFrame({
            "district": district,
            "cultivation_year": year,
            "season": season,
            "major_ha": major,
            "minor_ha": minor,
            "rainfed_ha": rainfed,
            "total_ha": total
        })

        all_data.append(data)


# 4. COMBINE AND STANDARDIZE DATA

irrigation = pd.concat(all_data, ignore_index=True)

# Standardize district names
irrigation["district"] = (
    irrigation["district"].str.strip().str.upper()
)

irrigation["district"] = irrigation["district"].replace(
    "KILLINOCHCHI", "KILINOCHCHI"
)


# 5. CONVERT AREA VALUES TO NUMBERS

area_columns = [
    "major_ha",
    "minor_ha",
    "rainfed_ha",
    "total_ha"
]

for column in area_columns:

    # Convert values to numbers; '-' becomes NaN
    irrigation[column] = pd.to_numeric(
        irrigation[column].astype(str).str.replace(
            ",", "", regex=False
        ),
        errors="coerce"
    )


# 6. CALCULATE IRRIGATION SHARE

# Percentage of harvested paddy area under irrigation
irrigation["irrigation_share_pct"] = (
    (irrigation["major_ha"] + irrigation["minor_ha"])
    / irrigation["total_ha"]
) * 100

# Handle zero or invalid total harvested areas
irrigation.loc[
    irrigation["total_ha"] <= 0,
    "irrigation_share_pct"
] = float("nan")


# 7. HANDLE MINOR AREA INCONSISTENCIES

# Check whether Major + Minor exceeds Total
difference = (
    irrigation["major_ha"]
    + irrigation["minor_ha"]
    - irrigation["total_ha"]
)

# Identify the observed 1-hectare discrepancies
rounding_issue = (
    (difference == 1)
    & (irrigation["irrigation_share_pct"] > 100)
)

# Cap affected percentages at 100%
# Original harvested-area values remain unchanged
irrigation.loc[
    rounding_issue, "irrigation_share_pct"
] = 100.0


# 8. VALIDATE AND SAVE DATASET

print("Total rows:", len(irrigation))

print(
    "Unique districts:",
    irrigation["district"].nunique()
)

print(
    "Maha rows:",
    (irrigation["season"] == "Maha").sum()
)

print(
    "Yala rows:",
    (irrigation["season"] == "Yala").sum()
)

print(
    "Duplicate records:",
    irrigation.duplicated(
        subset=["district", "cultivation_year", "season"]
    ).sum()
)

print(
    "Missing Maha years:",
    set(range(1978, 2026)) -
    set(
        irrigation.loc[
            irrigation["season"] == "Maha",
            "cultivation_year"
        ]
    )
)

print(
    "Adjusted irrigation shares:",
    rounding_issue.sum()
)

print(
    "Irrigation shares above 100%:",
    (irrigation["irrigation_share_pct"] > 100).sum()
)

print(
    "Missing irrigation shares:",
    irrigation["irrigation_share_pct"].isna().sum()
)

# Export the processed irrigation dataset
irrigation.to_csv(
    "Data/processed/irrigation_dataset.csv",
    index=False
)

print("Irrigation dataset saved successfully.")
