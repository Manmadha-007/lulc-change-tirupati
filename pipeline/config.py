from pathlib import Path

# =========================
# PROJECT ROOT
# =========================
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# =========================
# DATA PATHS
# =========================
DATA_DIR = PROJECT_ROOT / "data"

RAW_LANDSAT_DIR = DATA_DIR / "landsat_raw"
PROCESSED_DIR = DATA_DIR / "processed"
TILES_DIR = DATA_DIR / "tiles"

AOI_DIR = DATA_DIR / "aoi"
AOI_SHAPEFILE = AOI_DIR / "tirupati_boundary.shp"

# =========================
# TEMPORAL SETTINGS
# =========================
YEAR_T1 = 2018
YEAR_T2 = 2023

# =========================
# SPATIAL SETTINGS
# =========================
TARGET_CRS = "EPSG:32644"   # UTM Zone 44N (common for Andhra Pradesh)
TARGET_RESOLUTION = 30      # meters (Landsat)

# =========================
# LULC CLASSES (FIXED)
# =========================
LULC_CLASSES = {
    1: "Forest",
    2: "Water",
    3: "Agriculture",
    4: "Barren",
    5: "Built-up"
}

NUM_CLASSES = len(LULC_CLASSES)

# =========================
# MODEL SETTINGS
# =========================
RANDOM_FOREST_PARAMS = {
    "n_estimators": 100,
    "max_depth": 20,
    "min_samples_leaf": 50,
    "random_state": 42,
    "n_jobs": 4,
    "class_weight": {
        1: 1.0,
        2: 1.0,
        3: 1.0,
        4: 1.2,
        5: 2.0   # boost built-up
    }
}
