from pathlib import Path
import rasterio

from config import RAW_LANDSAT_DIR

REQUIRED_KEYWORDS = ["B2", "B3", "B4", "B5", "QA_PIXEL"]

def validate_scene(scene_dir):
    tif_files = list(scene_dir.glob("*.TIF")) + list(scene_dir.glob("*.tif"))
    if not tif_files:
        raise ValueError(f"No GeoTIFFs found in {scene_dir.name}")

    found = {k: False for k in REQUIRED_KEYWORDS}

    for f in tif_files:
        for k in REQUIRED_KEYWORDS:
            if k in f.name:
                found[k] = True

    for k, v in found.items():
        print(f"    {k}: {'FOUND' if v else 'MISSING'}")

    if not all(found.values()):
        raise ValueError(f"Missing required bands in {scene_dir.name}")

    # Open one band to check metadata
    with rasterio.open(tif_files[0]) as src:
        print(f"    CRS: {src.crs}")
        print(f"    Resolution: {src.res}")

def validate_year(year):
    year_dir = RAW_LANDSAT_DIR / str(year)
    print(f"\nValidating Landsat data for {year}...")

    if not year_dir.exists():
        raise FileNotFoundError(f"Missing directory: {year_dir}")

    scene_dirs = [d for d in year_dir.iterdir() if d.is_dir()]
    if not scene_dirs:
        raise ValueError("No scene folders found.")

    print(f"  Found {len(scene_dirs)} scenes.")

    for scene in scene_dirs:
        print(f"\n  Scene: {scene.name}")
        validate_scene(scene)

    print(f"\nValidation passed for {year}.")

if __name__ == "__main__":
    validate_year(2018)
    validate_year(2023)
