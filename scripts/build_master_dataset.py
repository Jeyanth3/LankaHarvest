# 1. IMPORT REQUIRED LIBRARIES
import pandas as pd

# 2. LOAD THE RAW DATASETS
maha = pd.read_excel("Data/interim/Average_Yeild-Maha_Season-1979-2025_Corrected.xlsx",header = None)

yala = pd.read_excel("Data/raw/Paddy yield/Average_Yeild-Yala_Season-1979-2025.xlsx",header=None
)

# 3. EXTRACT MAHA SEASON DATA
all_years = []

district = maha.iloc[4:29, 1]

for year_col in range(2, maha.shape[1] - 3, 4):
    year = maha.iloc[2, year_col]
    year = int(str(year).split("/")[0])

    yield_data = maha.iloc[4:29, year_col + 3]

    data = pd.DataFrame({
        "district": district,
        "cultivation_year": year,
        "season": "Maha",
        "paddy_yield_kg_per_ha": yield_data
    })

    all_years.append(data)

final_data = pd.concat(all_years, ignore_index=True)

# 4. EXTRACT YALA SEASON DATA
yala_years = []

district = yala.iloc[4:29, 1]

for year_col in range(2, yala.shape[1] - 3, 4):
    year = int(str(yala.iloc[2, year_col]).split("/")[0])
    yield_data = yala.iloc[4:29, year_col + 3]

    data = pd.DataFrame({
        "district": district,
        "cultivation_year": year,
        "season": "Yala",
        "paddy_yield_kg_per_ha": yield_data
    })

    yala_years.append(data)

yala_final = pd.concat(yala_years, ignore_index=True)

# 5. COMBINE MAHA AND YALA DATASETS
master = pd.concat([final_data, yala_final], ignore_index=True)

# 6. STANDARDIZE DISTRICT NAMES
master["district"] = master["district"].replace(
    "KILLINOCHCHI", "KILINOCHCHI"
)

# 7. EXPORT THE MASTER DATASET
master.to_csv("Data/processed/master_dataset.csv", index=False)
