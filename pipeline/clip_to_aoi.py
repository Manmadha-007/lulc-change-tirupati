import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np

from config import PROCESSED_DIR, AOI_SHAPEFILE

def clip_raster(year):
    print(f"\nClipping mosaic for {year} to Tirupati AOI...")

    raster_path = PROCESSED_DIR / str(year) / f"landsat_{year}_mosaic.tif"
    if not raster_path.exists():
        raise FileNotFoundError(raster_path)

    aoi = gpd.read_file(AOI_SHAPEFILE)

    with rasterio.open(raster_path) as src:
        # Reproject AOI to raster CRS if needed
        if aoi.crs != src.crs:
            aoi = aoi.to_crs(src.crs)

        out_image, out_transform = mask(
            src,
            aoi.geometry,
            crop=True,
            nodata=np.nan
        )

        out_meta = src.meta.copy()
        out_meta.update({
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "nodata": np.nan,
            "dtype": "float32"
        })

    out_path = PROCESSED_DIR / str(year) / f"landsat_{year}_tirupati.tif"

    with rasterio.open(out_path, "w", **out_meta) as dest:
        dest.write(out_image.astype("float32"))

    print(f"Saved clipped raster: {out_path.name}")

def main():
    clip_raster(2018)
    clip_raster(2023)

if __name__ == "__main__":
    main()
