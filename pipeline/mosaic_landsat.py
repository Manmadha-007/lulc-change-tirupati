from pathlib import Path
import rasterio
import numpy as np
from rasterio.merge import merge

from config import PROCESSED_DIR

def mosaic_year(year):
    input_dir = PROCESSED_DIR / str(year) / "cloud_masked"
    output_dir = PROCESSED_DIR / str(year)
    output_dir.mkdir(parents=True, exist_ok=True)

    raster_files = list(input_dir.glob("*.tif"))
    if not raster_files:
        raise ValueError(f"No cloud-masked rasters found for {year}")

    print(f"\nSafely mosaicking {len(raster_files)} scenes for {year}...")

    src_files = []
    for fp in raster_files:
        src = rasterio.open(fp)
        src_files.append(src)

    # IMPORTANT:
    # - nodata is explicitly NaN
    # - method='first' ensures valid pixels are preserved
    mosaic, transform = merge(
        src_files,
        nodata=np.nan,
        method="first"
    )

    meta = src_files[0].meta.copy()
    meta.update({
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": transform,
        "count": mosaic.shape[0],
        "nodata": np.nan,
        "dtype": "float32"
    })

    out_path = output_dir / f"landsat_{year}_mosaic.tif"

    with rasterio.open(out_path, "w", **meta) as dst:
        dst.write(mosaic.astype(np.float32))

    for src in src_files:
        src.close()

    print(f"Saved SAFE mosaic: {out_path.name}")

def main():
    mosaic_year(2018)
    mosaic_year(2023)

if __name__ == "__main__":
    main()
