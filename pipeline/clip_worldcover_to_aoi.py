import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
from pathlib import Path

from config import AOI_SHAPEFILE, PROCESSED_DIR

def clip_worldcover():
    worldcover_path = Path("data/lulc_reference/worldcover.tif")
    out_dir = PROCESSED_DIR / "labels"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "worldcover_tirupati_raw.tif"

    # Load AOI
    aoi = gpd.read_file(AOI_SHAPEFILE)

    with rasterio.open(worldcover_path) as src:
        # Reproject AOI to raster CRS if understood
        if aoi.crs != src.crs:
            aoi = aoi.to_crs(src.crs)

        # Strict polygon clip (no bounding box)
        out_image, out_transform = mask(
            src,
            aoi.geometry,
            crop=True,
            nodata=0
        )

        out_meta = src.meta.copy()
        out_meta.update({
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "nodata": 0,
            "count": 1
        })

    with rasterio.open(out_path, "w", **out_meta) as dst:
        dst.write(out_image[0], 1)

    print("WorldCover clipped to Tirupati AOI:")
    print(out_path)

if __name__ == "__main__":
    clip_worldcover()
