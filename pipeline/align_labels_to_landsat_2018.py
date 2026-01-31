import rasterio
from rasterio.warp import reproject, Resampling
import numpy as np

from .config import PROCESSED_DIR
from .lulc_class_mapping import WORLD_COVER_MAPPING


def align_labels():
    # Paths
    ref_path = PROCESSED_DIR / "2018" / "landsat_2018_tirupati.tif"
    label_src_path = PROCESSED_DIR / "labels" / "worldcover_tirupati_raw.tif"
    out_path = PROCESSED_DIR / "labels" / "lulc_labels_tirupati.tif"

    # Load reference raster (Landsat 2018)
    with rasterio.open(ref_path) as ref:
        ref_meta = ref.meta.copy()
        ref_crs = ref.crs
        ref_transform = ref.transform
        ref_height = ref.height
        ref_width = ref.width

    # Load WorldCover labels
    with rasterio.open(label_src_path) as src:
        src_data = src.read(1)

        # Destination array aligned to Landsat grid
        aligned = np.zeros((ref_height, ref_width), dtype=np.uint8)

        reproject(
            source=src_data
            ,
            destination=aligned,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=ref_transform,
            dst_crs=ref_crs,
            resampling=Resampling.nearest
        )

    # Remap WorldCover classes → Project LULC classes
    remapped = np.zeros_like(aligned, dtype=np.uint8)
    for wc_class, proj_class in WORLD_COVER_MAPPING.items():
        remapped[aligned == wc_class] = proj_class

    # Output metadata
    out_meta = ref_meta.copy()
    out_meta.update({
        "count": 1,
        "dtype": "uint8",
        "nodata": 0
    })

    with rasterio.open(out_path, "w", **out_meta) as dst:
        dst.write(remapped, 1)

    print("Aligned LULC labels saved to:")
    print(out_path)


if __name__ == "__main__":
    align_labels()
