
# ==================================================
# LankaHarvest - Climate Dataset Processing
# ==================================================
# Purpose:
# Convert daily NASA POWER climate data into seasonal
# climate features for Maha and Yala cultivation.
# ==================================================


# 1. IMPORT LIBRARIES

import pandas as pd
from pathlib import Path


# 2. SET UP FILE PATHS AND YEARS

input_folder = Path("Data/raw/Climate/nasa_daily")

output_file = Path("Data/processed/climate_dataset.csv")

START_YEAR = 1981
END_YEAR = 2025

parameters = [
    "PRECTOTCORR",
    "T2M",
    "RH2M",
    "ALLSKY_SFC_SW_DWN"
]


# 3. FUNCTION TO HANDLE MISSING VALUES

def calculate_average(values, expected_days):

    # Require at least 90% of daily values
    if values.count() >= expected_days * 0.90:
        return values.mean()

    return float("nan")


# 4. READ ALL DISTRICT CSV FILES

all_data = []

files = sorted(input_folder.glob("*.csv"))

if not files:
    raise FileNotFoundError("No NASA climate CSV files found")

for file in files:

    # Read the daily climate data
    daily = pd.read_csv(file)

    # Extract district name from the filename
    district = file.stem.replace("_", " ").upper()

    # Standardize district name
    if district == "KILLINOCHCHI":
        district = "KILINOCHCHI"

    # Convert the date column to datetime
    daily["date"] = pd.to_datetime(daily["date"])

    # Convert climate columns to numbers
    for parameter in parameters:
        daily[parameter] = pd.to_numeric(
            daily[parameter], errors="coerce"
        ).replace(-999, float("nan"))


    # 5. EXTRACT MAHA AND YALA SEASONS

    for year in range(START_YEAR, END_YEAR + 1):

        for season in ["Maha", "Yala"]:

            if season == "Maha":
                start = pd.Timestamp(year, 9, 1)
                end = pd.Timestamp(year + 1, 3, 31)

            else:
                start = pd.Timestamp(year, 4, 1)
                end = pd.Timestamp(year, 8, 31)

            # Extract records belonging to the season
            seasonal_data = daily[
                (daily["date"] >= start)
                & (daily["date"] <= end)
            ]

            expected_days = (end - start).days + 1

            # Skip incomplete seasonal date ranges
            if (
                len(seasonal_data) != expected_days
                or seasonal_data["date"].nunique() != expected_days
            ):
                continue


            # 6. CALCULATE SEASONAL CLIMATE FEATURES

            rainfall = seasonal_data["PRECTOTCORR"]

            # Rainfall totals require all daily values
            if rainfall.count() == expected_days:
                seasonal_rainfall = rainfall.sum()
                rainy_days = int((rainfall >= 1).sum())
            else:
                seasonal_rainfall = float("nan")
                rainy_days = float("nan")

            temperature = calculate_average(
                seasonal_data["T2M"], expected_days
            )

            humidity = calculate_average(
                seasonal_data["RH2M"], expected_days
            )

            solar = calculate_average(
                seasonal_data["ALLSKY_SFC_SW_DWN"],
                expected_days
            )

            # Store the calculated seasonal data
            data = {
                "district": district,
                "cultivation_year": year,
                "season": season,
                "seasonal_rainfall_mm": seasonal_rainfall,
                "temperature_c": temperature,
                "relative_humidity_pct": humidity,
                "solar_radiation_daily_mean": solar,
                "rainy_days": rainy_days
            }

            all_data.append(data)

    print("Processed:", district)


# 7. COMBINE AND SAVE THE DATASET

climate = pd.DataFrame(all_data)

climate = climate.sort_values(
    ["district", "cultivation_year", "season"]
)

climate.to_csv(output_file, index=False)


# 8. VALIDATE THE FINAL DATASET

print("Total rows:", len(climate))

print("Unique districts:", climate["district"].nunique())

print(
    "Duplicate records:",
    climate.duplicated(
        subset=["district", "cultivation_year", "season"]
    ).sum()
)

print("Missing values:")
print(climate.isna().sum())

print(climate.head(10))

print("Climate dataset saved successfully.")


missing_solar = climate[
    climate["solar_radiation_daily_mean"].isna()
]

print(
    missing_solar.groupby("cultivation_year").size()
)