import rasterio
import numpy as np
import pandas as pd
from pathlib import Path

from config import PROCESSED_DIR


def extract_training_data():
    landsat_path = PROCESSED_DIR / "2018" / "landsat_2018_tirupati.tif"
    labels_path = PROCESSED_DIR / "labels" / "lulc_labels_tirupati.tif"
    out_path = PROCESSED_DIR / "training" / "training_pixels_2018.csv"

    with rasterio.open(landsat_path) as src:
        bands = src.read().astype(np.float32)

    with rasterio.open(labels_path) as lbl:
        labels = lbl.read(1)

    # Mask invalid pixels
    valid_mask = (
        ~np.isnan(bands).any(axis=0)
        & (labels > 0)
    )

    blue = bands[0][valid_mask]
    green = bands[1][valid_mask]
    red = bands[2][valid_mask]
    nir = bands[3][valid_mask]

    # NDVI
    ndvi = (nir - red) / (nir + red + 1e-6)

    y = labels[valid_mask]

    df = pd.DataFrame({
        "blue": blue,
        "green": green,
        "red": red,
        "nir": nir,
        "ndvi": ndvi,
        "label": y
    })

    df.to_csv(out_path, index=False)
    print("Training dataset saved:", out_path)
    print("Total samples:", len(df))


if __name__ == "__main__":
    extract_training_data()
