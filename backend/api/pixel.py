from fastapi import APIRouter
import rasterio
from pathlib import Path
from pyproj import Transformer

router = APIRouter()

# Define paths to rasters
DATA_DIR = Path("data/processed")
CHANGE_DIR = DATA_DIR / "change" # Confidence files are here

LULC_2018_PATH = DATA_DIR / "predictions/lulc_2018.tif" # Validated path
LULC_2023_PATH = DATA_DIR / "predictions/lulc_2023.tif" # Validated path
CONFIDENCE_2018_PATH = CHANGE_DIR / "confidence_2018.tif"
CONFIDENCE_2023_PATH = CHANGE_DIR / "confidence_2023.tif"

LULC_CLASSES = {
    1: "Forest",
    2: "Water",
    3: "Agriculture",
    4: "Barren",
    5: "Built-up"
}

# Initialize Transformer
# EPSG:4326 (Lat/Lon) -> EPSG:32644 (Projected, used by Rasters)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32644", always_xy=True)

@router.get("/pixel")
def get_pixel_value(lat: float, lon: float):
    # Transform coordinates
    x, y = transformer.transform(lon, lat)
    
    result = {}
    
    # Query 2018
    try:
        with rasterio.open(LULC_2018_PATH) as src:
            for val in src.sample([(x, y)]):
                class_id = int(val[0])
                # Check for nodata
                if class_id == src.nodata:
                    result["2018"] = {"class_name": "No Data"}
                else:
                    result["2018"] = {
                        "class_id": class_id,
                        "class_name": LULC_CLASSES.get(class_id, "Unknown")
                    }
        
        # Get Confidence 2018
        if "class_id" in result.get("2018", {}):
            with rasterio.open(CONFIDENCE_2018_PATH) as src:
                for val in src.sample([(x, y)]):
                    result["2018"]["confidence"] = float(val[0])

    except Exception as e:
        if "2018" not in result: result["2018"] = {}
        result["2018"]["error"] = str(e)

    # Query 2023
    try:
        with rasterio.open(LULC_2023_PATH) as src:
            for val in src.sample([(x, y)]):
                class_id = int(val[0])
                if class_id == src.nodata:
                    result["2023"] = {"class_name": "No Data"}
                else:
                    result["2023"] = {
                        "class_id": class_id,
                        "class_name": LULC_CLASSES.get(class_id, "Unknown")
                    }
        
        # Get Confidence 2023
        if "class_id" in result.get("2023", {}):
            with rasterio.open(CONFIDENCE_2023_PATH) as src:
                for val in src.sample([(x, y)]):
                    result["2023"]["confidence"] = float(val[0])

    except Exception as e:
        if "2023" not in result: result["2023"] = {}
        result["2023"]["error"] = str(e)

    return result
