import rasterio
import numpy as np
from config import PROCESSED_DIR


def compute_transition_map():
    pred_dir = PROCESSED_DIR / "predictions"
    out_dir = PROCESSED_DIR / "change"
    out_dir.mkdir(parents=True, exist_ok=True)

    lulc_2018 = pred_dir / "lulc_2018.tif"
    lulc_2023 = pred_dir / "lulc_2023.tif"
    out_path = out_dir / "change_map.tif"

    with rasterio.open(lulc_2018) as src18, rasterio.open(lulc_2023) as src23:
        a = src18.read(1)
        b = src23.read(1)

        meta = src18.meta.copy()
        meta.update(dtype="uint8", count=1, nodata=0)

        # Encode transition: i*10 + j
        transition = np.zeros_like(a, dtype=np.uint8)
        valid = (a > 0) & (b > 0)
        transition[valid] = (a[valid] * 10 + b[valid]).astype(np.uint8)

        with rasterio.open(out_path, "w", **meta) as dst:
            dst.write(transition, 1)

    print("Transition-encoded change map saved:", out_path)


if __name__ == "__main__":
    compute_transition_map()
