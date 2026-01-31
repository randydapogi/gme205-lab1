import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------#
# Paths
# ----------------------------- 
DATA_PATH = "data/points.csv"
OUTPUT_DIR = "output"
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "summary.json")
PLOT_PATH = os.path.join(OUTPUT_DIR, "preview.png")

# -----------------------------
# A. Read the CSV file 
# -----------------------------
try: 
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"Error: Cannot find file at '{DATA_PATH}'.")
    print("Make sure you have: data/points.csv")
    raise 

print("=== DATA INSPECTION REPORT ===") 
# ----------------------------- 
# B. Print basic information 
# ----------------------------- 

num_rows, num_cols = df.shape
print("\nBasic Information")
print("-----------------")
print(f"Number of rows: {num_rows}")
print(f"Number of columns: {num_cols}")
print(f"Column names: {list(df.columns)}")

# ----------------------------- 
# C. Data quality checks
# -----------------------------
print("\nData Quality Checks")
print("-------------------")

missing_values = df.isna().sum()
print("Missing values per column:")
print(missing_values)

# Ensure required columns exist
required_cols = {"lon", "lat"}
if not required_cols.issubset(df.columns):
    missing = required_cols - set(df.columns)
    raise ValueError(f"Missing required column(s): {missing}. Required: lon, lat")

# Invalid coordinate checks (also catches missing lon/lat as invalid)
invalid_lon_mask = df["lon"].isna() | (df["lon"] < -180) | (df["lon"] > 180)
invalid_lat_mask = df["lat"].isna() | (df["lat"] < -90) | (df["lat"] > 90)

invalid_lon_count = int(invalid_lon_mask.sum())
invalid_lat_count = int(invalid_lat_mask.sum())
print(f"\nInvalid longitude values (missing or outside -180..180): {invalid_lon_count}")
print(f"Invalid latitude values (missing or outside -90..90): {invalid_lat_count}")

# -----------------------------
# D. Bounding box (valid coords only)
# -----------------------------
valid_mask = ~(invalid_lon_mask | invalid_lat_mask)
valid_df = df.loc[valid_mask].copy()
print("\nBounding Box")
print("------------")

if len(valid_df) == 0:
    bbox = None
    print("No valid coordinate rows found. Bounding box cannot be computed.")
else:
    min_lon = float(valid_df["lon"].min())
    max_lon = float(valid_df["lon"].max())
    min_lat = float(valid_df["lat"].min())
    max_lat = float(valid_df["lat"].max())
    
    bbox = { "min_lon": min_lon, "min_lat": min_lat, "max_lon": max_lon, "max_lat": max_lat }
    
    print(f"Min Longitude: {min_lon}")
    print(f"Min Latitude : {min_lat}")
    print(f"Max Longitude: {max_lon}")
    print(f"Max Latitude : {max_lat}")
    
# -----------------------------
# E. Save outputs 
# -----------------------------
# Create output folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True) 

# Build summary dictionary
summary = { "file": DATA_PATH, "rows": int(num_rows), "columns": int(num_cols), "column_names": list(df.columns), "missing_values_per_column": {k: int(v) for k, v in missing_values.items()}, "invalid_longitude_count": invalid_lon_count, "invalid_latitude_count": invalid_lat_count, "valid_coordinate_rows": int(len(valid_df)), "bbox": bbox } 

# Write summary.json
with open(SUMMARY_PATH, "w", encoding="utf-8") as f: json.dump(summary, f, indent=2)
print(f"\nSaved summary to: {SUMMARY_PATH}") 

# Save scatter plot (valid coords only)
plt.figure() 
if len(valid_df) == 0: 
    # Create an empty plot with message in title
    plt.title("Preview Plot (No valid coordinates to plot)")
else: 
    plt.scatter(valid_df["lon"], valid_df["lat"])
    plt.title("Point Preview (lon vs lat)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig(PLOT_PATH, dpi=150, bbox_inches="tight")
    plt.close()
    
print(f"Saved scatter plot to: {PLOT_PATH}")
print("\n=== END OF REPORT ===")