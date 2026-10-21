# ============================================================
# LankaHarvest - Download Daily Climate Data from NASA POWER
# ============================================================
# Each district uses ONE representative location for now.
# These are point estimates, not district-wide averages.

# 1. Import libraries
import time
from pathlib import Path

import pandas as pd
import requests


# 2. Set up the NASA POWER API
API_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
START_DATE = "19810101"
END_DATE = "20260331"  

PARAMETERS = [
    "PRECTOTCORR",        # Daily precipitation
    "T2M",               # Daily mean temperature
    "RH2M",              # Daily relative humidity
    "ALLSKY_SFC_SW_DWN", # Daily solar radiation
]

# Start with Jaffna. Change to False to download all 25 districts.
TEST_ONLY = False


# 3. Read the district coordinates CSV
locations = pd.read_csv("Data/raw/Climate/district_locations.csv")

# Create a folder for the downloaded CSV files
output_folder = Path("Data/raw/Climate/nasa_daily")
output_folder.mkdir(parents=True, exist_ok=True)


# 4. Download daily climate data for each district
for _, location in locations.iterrows():
    district = location["district"]
    latitude = location["latitude"]
    longitude = location["longitude"]

    if TEST_ONLY and district != "Jaffna":
        continue

    output_file = output_folder / f"{district.replace(' ', '_')}.csv"

    # Skip files already downloaded successfully
    if output_file.exists():
        print(f"Already downloaded: {district}")
        continue

    print(f"Downloading: {district}")

    # Values sent to NASA POWER with the HTTP request
    api_parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "start": START_DATE,
        "end": END_DATE,
        "community": "AG",
        "parameters": ",".join(PARAMETERS),
        "format": "JSON",
        "time-standard": "UTC",
    }

    try:
        response = requests.get(API_URL, params=api_parameters, timeout=180)
        response.raise_for_status()
        weather = response.json()["properties"]["parameter"]

        # 5. Convert the API data into a CSV table
        data = pd.DataFrame(weather)
        if data.empty:
            raise ValueError("NASA returned no daily records")

        data.index.name = "date"
        data = data.reset_index()
        data["date"] = pd.to_datetime(data["date"], format="%Y%m%d")

        # Convert numeric data and replace NASA's -999 missing-value marker
        for name in PARAMETERS:
            data[name] = pd.to_numeric(data[name], errors="coerce")
            data[name] = data[name].replace(-999, float("nan"))

        data.insert(0, "district", district)
        data["latitude"] = latitude
        data["longitude"] = longitude

        data.to_csv(output_file, index=False)
        print(f"Saved {len(data)} days to {output_file}")

    except (requests.RequestException, ValueError, KeyError) as error:
        print(f"Failed for {district}: {error}")

    # Avoid sending many API requests back-to-back
    time.sleep(1)

print("Finished.")
