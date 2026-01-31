from pathlib import Path
import numpy as np
import rasterio

from config import RAW_LANDSAT_DIR, PROCESSED_DIR

# Bits to mask in QA_PIXEL (Landsat Collection 2)
CLOUD_SHADOW_BIT = 4
CLOUD_BIT = 3
CIRRUS_BIT = 2

def mask_clouds(qa_array):
    cloud_shadow = (qa_array & (1 << CLOUD_SHADOW_BIT)) != 0
    clouds = (qa_array & (1 << CLOUD_BIT)) != 0
    cirrus = (qa_array & (1 << CIRRUS_BIT)) != 0
    return cloud_shadow | clouds | cirrus

def find_band(scene_dir, keyword):
    files = list(scene_dir.glob("*.TIF")) + list(scene_dir.glob("*.tif"))
    for f in files:
        if keyword.lower() in f.name.lower():
            return f
    return None


def process_scene(scene_dir, year):
    print(f"Processing scene: {scene_dir.name}")

    bands = {}
    meta = None

    for band in ["B2", "B3", "B4", "B5"]:
        band_file = find_band(scene_dir, band)
        if band_file is None:
            raise FileNotFoundError(
                f"Missing band {band} in scene {scene_dir.name}\n"
                f"Available files: {[f.name for f in scene_dir.iterdir()]}"
            )

        with rasterio.open(band_file) as src:
            bands[band] = src.read(1).astype(np.float32)
            meta = src.meta

    qa_file = find_band(scene_dir, "QA_PIXEL")
    if qa_file is None:
        raise FileNotFoundError(
            f"Missing QA_PIXEL in scene {scene_dir.name}\n"
            f"Available files: {[f.name for f in scene_dir.iterdir()]}"
        )

    with rasterio.open(qa_file) as qa_src:
        qa = qa_src.read(1)

    mask = mask_clouds(qa)

    for band in bands:
        bands[band][mask] = np.nan

    stacked = np.stack([
        bands["B2"],
        bands["B3"],
        bands["B4"],
        bands["B5"]
    ])

    # 🔒 CRITICAL FIX:
    # Mask pixels where ALL bands are zero (outside scene footprint)
    valid_mask = np.any(stacked != 0, axis=0)

    stacked[:, ~valid_mask] = np.nan


    out_dir = PROCESSED_DIR / str(year) / "cloud_masked"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{scene_dir.name}_masked.tif"

    meta.update({
        "count": 4,
        "dtype": "float32",
        "nodata": np.nan
    })

    with rasterio.open(out_path, "w", **meta) as dst:
        dst.write(stacked)

    print(f"  Saved masked scene to {out_path.name}")

def process_year(year):
    year_dir = RAW_LANDSAT_DIR / str(year)
    for scene in year_dir.iterdir():
        if scene.is_dir():
            process_scene(scene, year)

if __name__ == "__main__":
    process_year(2018)
    process_year(2023)
