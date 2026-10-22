
# ==================================================
# LankaHarvest - Irrigation Dataset Processing
# ==================================================

# 1. IMPORT LIBRARY

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

# Process Maha and Yala using the same extraction logic
for season, df in datasets.items():

    district = df.iloc[4:29, 1]

    # Each year occupies four columns
    for year_col in range(2, df.shape[1] - 3, 4):

        year = int(str(df.iloc[2, year_col]).split("/")[0])

        major = df.iloc[4:29, year_col]
        minor = df.iloc[4:29, year_col + 1]
        rainfed = df.iloc[4:29, year_col + 2]
        total = df.iloc[4:29, year_col + 3]

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


# 4. COMBINE ALL RECORDS

irrigation = pd.concat(all_data, ignore_index=True)


# 5. CONVERT AREA VALUES TO NUMBERS

area_columns = [
    "major_ha",
    "minor_ha",
    "rainfed_ha",
    "total_ha"
]

for column in area_columns:
    irrigation[column] = pd.to_numeric(
        irrigation[column].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )


# 6. CALCULATE IRRIGATION SHARE

irrigation["irrigation_share_pct"] = (
    (irrigation["major_ha"] + irrigation["minor_ha"])
    / irrigation["total_ha"]
) * 100

# Avoid percentages when total harvested area is zero
irrigation.loc[
    irrigation["total_ha"] <= 0,
    "irrigation_share_pct"
] = float("nan")


# 7. SAVE CSV

irrigation.to_csv(
    "Data/processed/irrigation_dataset.csv",
    index=False
)


# 8. VALIDATE OUTPUT

print("Total rows:", len(irrigation))
print("Unique districts:", irrigation["district"].nunique())
print("Maha rows:", len(irrigation[irrigation["season"] == "Maha"]))
print("Yala rows:", len(irrigation[irrigation["season"] == "Yala"]))

print(
    "Duplicate records:",
    irrigation.duplicated(
        subset=["district", "cultivation_year", "season"]
    ).sum()
)

print(
    "Irrigation shares above 100%:",
    (irrigation["irrigation_share_pct"] > 100).sum()
)

print(irrigation.head(10))

print(irrigation[
    irrigation.duplicated(
        subset=["district", "cultivation_year", "season"],
        keep=False
    )
][["district", "cultivation_year", "season"]].head(10))

print("Duplicate records:", irrigation.duplicated(
    subset=["district", "cultivation_year", "season"]
).sum())

print("Missing Maha years:",
      set(range(1978, 2026)) -
      set(irrigation[irrigation["season"] == "Maha"]["cultivation_year"]))
