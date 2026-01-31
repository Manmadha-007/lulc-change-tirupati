import numpy as np
import rasterio
import joblib
from pathlib import Path

from config import PROCESSED_DIR
import warnings
warnings.filterwarnings(
    "ignore",
    message="X does not have valid feature names"
)

def infer_year(year):
    print(f"\nRunning inference for {year}...")

    # =========================
    # Paths
    # =========================
    landsat_path = PROCESSED_DIR / str(year) / f"landsat_{year}_tirupati.tif"
    model_path = Path("data/models/rf_lulc_model.pkl")

    out_dir = PROCESSED_DIR / "predictions"
    out_dir.mkdir(parents=True, exist_ok=True)

    lulc_out = out_dir / f"lulc_{year}.tif"
    conf_out = out_dir / f"confidence_{year}.tif"

    # =========================
    # Load model
    # =========================
    rf = joblib.load(model_path)

    # =========================
    # Open Landsat raster
    # =========================
    with rasterio.open(landsat_path) as src:
        meta = src.meta.copy()
        nodata = src.nodata

        # Output metadata
        meta.update(count=1, dtype="uint8", nodata=0)
        conf_meta = meta.copy()
        conf_meta.update(dtype="float32")

        with rasterio.open(lulc_out, "w", **meta) as lulc_dst, \
             rasterio.open(conf_out, "w", **conf_meta) as conf_dst:

            # =========================
            # Window-wise inference
            # =========================
            for _, window in src.block_windows(1):
                bands = src.read(window=window).astype(np.float32)
                rows, cols = bands.shape[1:]

                # -------------------------
                # Valid pixel mask
                # -------------------------
                valid = ~np.isnan(bands).any(axis=0)

                if nodata is not None:
                    valid &= (bands[0] != nodata)

                # Empty window → write zeros
                if not valid.any():
                    lulc_dst.write(
                        np.zeros((rows, cols), dtype=np.uint8),
                        1,
                        window=window
                    )
                    conf_dst.write(
                        np.zeros((rows, cols), dtype=np.float32),
                        1,
                        window=window
                    )
                    continue

                # -------------------------
                # Feature extraction
                # -------------------------
                blue, green, red, nir = bands
                ndvi = (nir - red) / (nir + red + 1e-6)

                X = np.stack(
                    [
                        blue[valid],
                        green[valid],
                        red[valid],
                        nir[valid],
                        ndvi[valid]
                    ],
                    axis=1
                )

                # -------------------------
                # Prediction
                # -------------------------
                probs = rf.predict_proba(X)
                preds = rf.classes_[np.argmax(probs, axis=1)]
                confs = np.max(probs, axis=1)

                # -------------------------
                # Write outputs
                # -------------------------
                lulc_block = np.zeros((rows, cols), dtype=np.uint8)
                conf_block = np.zeros((rows, cols), dtype=np.float32)

                lulc_block[valid] = preds.astype(np.uint8)
                conf_block[valid] = confs.astype(np.float32)

                lulc_dst.write(lulc_block, 1, window=window)
                conf_dst.write(conf_block, 1, window=window)

    print(f"Saved outputs for {year}:")
    print(f"  - {lulc_out}")
    print(f"  - {conf_out}")


if __name__ == "__main__":
    infer_year(2018)
    infer_year(2023)
